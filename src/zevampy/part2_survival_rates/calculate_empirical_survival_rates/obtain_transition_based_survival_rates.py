"""Calculate transition-based empirical vehicle survival rates from consecutive stock snapshots."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import (
    age_dim,
    country_dim,
    methodology_dim,
    new_registrations_dim,
    number_registered_vehicles_dim,
    powertrain_dim,
    registration_based_method_label,
    stock_year_dim,
    survival_rate_dim,
    time_dim,
    transition_based_method_label,
    transition_factor_dim,
)


def _cumulative_product_until_missing(values: pd.Series) -> pd.Series:
    """Return a cumulative product and keep all values after the first missing value missing."""
    result = []
    cumulative = 1.0
    valid = True

    for value in values:
        if not valid or pd.isna(value):
            valid = False
            result.append(np.nan)
            continue

        cumulative *= float(value)
        result.append(cumulative)

    return pd.Series(result, index=values.index, dtype=float)


def obtain_transition_based_survival_rates(stock, registrations, survival_grouping):
    """Calculate empirical CSPs from year-to-year stock transitions.

    For each survival group and stock year ``t``, the first empirical CSP point
    is calculated from stock divided by registrations for the corresponding
    registration cohort. Subsequent points are obtained recursively from the
    transition of the same cohort between two consecutive stock snapshots::

        S_t(a_min) = N_t(a_min) / R_(t-a_min)
        q_t(a)     = N_t(a) / N_(t-1)(a-1)
        S_t(a)     = S_t(a-1) * q_t(a)

    A transition-based curve is only retained when a stock snapshot for
    ``t - 1`` is available for the same non-year survival group.

    Parameters:
        stock (pandas.DataFrame):
            Age-resolved vehicle stock containing ``stock year``.
        registrations (pandas.DataFrame):
            Historical vehicle registrations containing ``time``.
        survival_grouping (list[str]):
            Dimensions defining a CSP group, normally country, powertrain and
            stock year.

    Returns:
        pandas.DataFrame:
            Transition-based empirical survival rates with the annual
            transition factor and methodology identifier.
    """
    stock = stock.copy()
    registrations = registrations.copy()

    if stock_year_dim not in survival_grouping:
        raise ValueError(
            "Transition-based survival rates require 'stock year' in survival_grouping."
        )

    group_without_year = [dim for dim in survival_grouping if dim != stock_year_dim]

    # Aggregate registration data consistently with the requested grouping.
    registration_grouping = [dim for dim in group_without_year if dim in registrations.columns]
    if country_dim not in registration_grouping and country_dim in registrations.columns:
        registration_grouping.insert(0, country_dim)

    registrations_agg = (
        registrations
        .groupby(registration_grouping + [time_dim], as_index=False)[new_registrations_dim]
        .sum()
    )

    # The initial point of every curve is stock / registrations of the cohort.
    min_age = (
        stock
        .groupby(survival_grouping, as_index=False)[age_dim]
        .min()
        .rename(columns={age_dim: "_minimum_age"})
    )
    transition = stock.merge(min_age, on=survival_grouping, how="left")
    transition["_registration_year"] = transition[stock_year_dim] - transition[age_dim]

    registrations_agg = registrations_agg.rename(columns={time_dim: "_registration_year"})
    registration_join_cols = registration_grouping + ["_registration_year"]
    transition = transition.merge(
        registrations_agg,
        on=registration_join_cols,
        how="left",
        validate="many_to_one",
    )

    # Build a lookup table for the previous year's same cohort:
    # current (t, age a) <-> previous (t-1, age a-1).
    previous_stock = stock[
        group_without_year + [stock_year_dim, age_dim, number_registered_vehicles_dim]
    ].copy()
    previous_stock[stock_year_dim] = previous_stock[stock_year_dim] + 1
    previous_stock[age_dim] = previous_stock[age_dim] + 1
    previous_stock = previous_stock.rename(
        columns={number_registered_vehicles_dim: "_previous_stock"}
    )

    transition = transition.merge(
        previous_stock,
        on=group_without_year + [stock_year_dim, age_dim],
        how="left",
        validate="many_to_one",
    )

    is_first_age = transition[age_dim] == transition["_minimum_age"]

    initial_factor = np.divide(
        transition[number_registered_vehicles_dim],
        transition[new_registrations_dim],
        out=np.full(len(transition), np.nan, dtype=float),
        where=transition[new_registrations_dim].notna()
        & (transition[new_registrations_dim] != 0),
    )

    stock_transition_factor = np.divide(
        transition[number_registered_vehicles_dim],
        transition["_previous_stock"],
        out=np.full(len(transition), np.nan, dtype=float),
        where=transition["_previous_stock"].notna()
        & (transition["_previous_stock"] != 0),
    )

    transition[transition_factor_dim] = np.where(
        is_first_age,
        initial_factor,
        stock_transition_factor,
    )

    # A valid transition curve needs a previous stock snapshot. The first age
    # itself does not use previous stock, so explicitly test availability via
    # the remaining ages of each group.
    has_previous_snapshot = (
        transition.loc[~is_first_age]
        .groupby(survival_grouping)["_previous_stock"]
        .transform(lambda s: s.notna().any())
    )
    transition.loc[~is_first_age, "_has_previous_snapshot"] = has_previous_snapshot
    transition["_has_previous_snapshot"] = (
        transition
        .groupby(survival_grouping)["_has_previous_snapshot"]
        .transform("max")
        .eq(True)
    )
    transition = transition[transition["_has_previous_snapshot"]].copy()

    transition = transition.sort_values(survival_grouping + [age_dim])
    transition[survival_rate_dim] = (
        transition
        .groupby(survival_grouping, group_keys=False)[transition_factor_dim]
        .apply(_cumulative_product_until_missing)
    )

    # The transition method is only empirically defined up to the first
    # unavailable/zero denominator. Do not impute the missing tail: remove it
    # so the fitted distribution can be estimated from the valid continuous
    # age sequence and extrapolated afterwards.
    transition = transition[
        transition[transition_factor_dim].notna()
        & transition[survival_rate_dim].notna()
    ].copy()
    transition = transition[
        np.isfinite(transition[transition_factor_dim])
        & np.isfinite(transition[survival_rate_dim])
    ].copy()

    transition[methodology_dim] = transition_based_method_label

    output_cols = survival_grouping + [age_dim, transition_factor_dim, survival_rate_dim, methodology_dim]
    return transition[output_cols].reset_index(drop=True)
