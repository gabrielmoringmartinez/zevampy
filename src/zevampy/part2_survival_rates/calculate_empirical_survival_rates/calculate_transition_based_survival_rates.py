"""Calculate transition-based empirical vehicle survival rates."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import (
    age_dim,
    country_dim,
    new_registrations_dim,
    number_registered_vehicles_dim,
    stock_year_dim,
    survival_rate_dim,
    time_dim,
)
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import (
    filter_vehicle_age,
)


ANNUAL_TRANSITION_FACTOR_DIM = "annual transition factor"


def calculate_transition_based_survival_rates(
    stock,
    registrations,
    countries_to_keep,
    output_path,
    survival_grouping,
):
    """Estimate empirical survival rates from consecutive stock snapshots.

    The method follows the transition-based approach documented in the project
    example spreadsheet. For a stock snapshot in year ``t`` the first survival
    point is anchored to new registrations from ``t - 1``. Older ages are then
    obtained recursively from the ratio between the stock of age ``a`` in year
    ``t`` and the stock of age ``a - 1`` in year ``t - 1``.

    With ZEVAMPY's current age convention (minimum vehicle age = 1):

        S_t(1) = N_t(1) / R_(t-1)
        q_t(a) = N_t(a) / N_(t-1)(a-1),  a > 1
        S_t(a) = S_t(a-1) * q_t(a)

    Transition factors are intentionally not clipped to one. Values above one
    can contain information about imports, re-registrations, or inconsistencies
    in the underlying stock data.

    A curve can only be calculated for stock year ``t`` when the previous stock
    snapshot ``t - 1`` is available for the same survival group.

    Returns:
        pandas.DataFrame: Transition-based empirical survival rates.
    """
    stock = filter_vehicle_age(stock.copy())
    stock = stock[stock[country_dim].isin(countries_to_keep)].copy()
    registrations = registrations[registrations[country_dim].isin(countries_to_keep)].copy()

    if stock_year_dim not in survival_grouping:
        raise ValueError(
            "Transition-based survival rates require 'stock year' in survival_rates.grouping "
            "because consecutive stock snapshots are compared."
        )

    group_dims = [dim for dim in survival_grouping if dim != stock_year_dim]

    required_stock_cols = set(group_dims + [stock_year_dim, age_dim, number_registered_vehicles_dim])
    missing_stock_cols = required_stock_cols - set(stock.columns)
    if missing_stock_cols:
        raise ValueError(
            "Transition-based survival-rate calculation is missing stock columns: "
            f"{sorted(missing_stock_cols)}"
        )

    required_registration_cols = set(group_dims + [time_dim, new_registrations_dim])
    missing_registration_cols = required_registration_cols - set(registrations.columns)
    if missing_registration_cols:
        raise ValueError(
            "Transition-based survival-rate calculation is missing registration columns: "
            f"{sorted(missing_registration_cols)}"
        )

    # Ensure one stock value per group/year/age and one registration value per
    # group/year before constructing the transitions.
    stock_agg = (
        stock.groupby(group_dims + [stock_year_dim, age_dim], as_index=False)[number_registered_vehicles_dim]
        .sum()
    )
    registrations_agg = (
        registrations.groupby(group_dims + [time_dim], as_index=False)[new_registrations_dim]
        .sum()
    )

    # Previous year's stock is shifted forward by one stock year and one age,
    # so it can be joined directly to the current stock row of the same cohort.
    previous_stock = stock_agg.rename(
        columns={number_registered_vehicles_dim: "previous stock"}
    ).copy()
    previous_stock[stock_year_dim] = previous_stock[stock_year_dim] + 1
    previous_stock[age_dim] = previous_stock[age_dim] + 1

    transitions = stock_agg.merge(
        previous_stock[group_dims + [stock_year_dim, age_dim, "previous stock"]],
        on=group_dims + [stock_year_dim, age_dim],
        how="left",
        validate="one_to_one",
    )

    # Registration year corresponding to the youngest age in the stock snapshot.
    # With the current ZEVAMPY age convention age 1 at 01.01.t corresponds to
    # vehicles newly registered during calendar year t-1.
    youngest_age = int(stock_agg[age_dim].min())
    if youngest_age != 1:
        raise ValueError(
            "Transition-based survival rates currently expect ZEVAMPY's vehicle-age "
            f"convention to start at age 1, but the minimum age is {youngest_age}."
        )

    initial_registrations = registrations_agg.rename(
        columns={time_dim: "registration year"}
    ).copy()
    initial_registrations[stock_year_dim] = initial_registrations["registration year"] + 1
    initial_registrations = initial_registrations.rename(
        columns={new_registrations_dim: "initial registrations"}
    )

    transitions = transitions.merge(
        initial_registrations[group_dims + [stock_year_dim, "initial registrations"]],
        on=group_dims + [stock_year_dim],
        how="left",
        validate="many_to_one",
    )

    transitions[ANNUAL_TRANSITION_FACTOR_DIM] = np.where(
        transitions[age_dim] == youngest_age,
        np.divide(
            transitions[number_registered_vehicles_dim],
            transitions["initial registrations"],
            out=np.full(len(transitions), np.nan, dtype=float),
            where=transitions["initial registrations"].fillna(0).to_numpy() != 0,
        ),
        np.divide(
            transitions[number_registered_vehicles_dim],
            transitions["previous stock"],
            out=np.full(len(transitions), np.nan, dtype=float),
            where=transitions["previous stock"].fillna(0).to_numpy() != 0,
        ),
    )

    # A transition curve is meaningful only if the preceding stock snapshot
    # exists. Test this at age 2, which needs age 1 from the previous year.
    available_years = stock_agg[group_dims + [stock_year_dim]].drop_duplicates()
    previous_years = available_years.copy()
    previous_years[stock_year_dim] = previous_years[stock_year_dim] + 1
    previous_years["previous stock year available"] = True
    transitions = transitions.merge(
        previous_years,
        on=group_dims + [stock_year_dim],
        how="left",
        validate="many_to_one",
    )
    transitions = transitions[
        transitions["previous stock year available"].eq(True)
    ].copy()

    # Recursive multiplication of annual transition factors within each curve.
    transitions = transitions.sort_values(group_dims + [stock_year_dim, age_dim])
    transitions[survival_rate_dim] = transitions.groupby(
        group_dims + [stock_year_dim], sort=False
    )[ANNUAL_TRANSITION_FACTOR_DIM].cumprod(skipna=False)

    # Once one required transition is missing, the recursive CSP is undefined
    # from that age onwards. Keep only the contiguous, calculable part of each
    # empirical curve.
    transitions = transitions[transitions[survival_rate_dim].notna()].copy()

    output_cols = survival_grouping + [age_dim, ANNUAL_TRANSITION_FACTOR_DIM, survival_rate_dim]
    result = transitions[output_cols].copy()

    result.to_csv(
        f"{output_path}/2_2_empirical_survival_rates_transition_based.csv",
        sep=";",
        index=False,
        decimal=",",
    )

    return result
