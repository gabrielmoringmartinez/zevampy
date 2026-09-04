"""Prepare registration data for empirical survival-rate estimation."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import (
    age_dim,
    country_dim,
    time_dim,
    stock_year_empirical_csp_data_dim,
)
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import filter_vehicle_age


def _get_stock_year_merge_columns(stock_year, survival_grouping):
    """Determine how stock reference years should be merged with registrations.

    Parameters:
        stock_year (pandas.DataFrame):
            Stock reference-year table.
        survival_grouping (list[str]):
            Configured survival-rate grouping dimensions.

    Returns:
        list[str]:
            Full survival grouping when group-specific reference years are supplied,
            otherwise country only.
    """
    if all(dim in stock_year.columns for dim in survival_grouping):
        return list(survival_grouping)
    return [country_dim]


def prepare_registrations_data(
    registrations,
    stock_year,
    survival_grouping,
    max_age=45,
):
    """Align registration cohorts with the reference year of each survival group.

    Reference years may be defined for the complete survival group, such as
    country plus powertrain, or only by country. Country-only reference years are
    applied to every powertrain in that country.

    Parameters:
        registrations (pandas.DataFrame):
            Registration cohorts used to estimate empirical survival rates.
        stock_year (pandas.DataFrame):
            Reference year for each stock-by-age group.
        survival_grouping (list[str]):
            Configured dimensions defining survival groups.
        max_age (int, optional):
            Maximum vehicle age retained after cohort alignment.

    Returns:
        pandas.DataFrame:
            Registrations with derived vehicle ages and applicable stock reference
            years, filtered to the requested age horizon.

    Raises:
        ValueError:
            If one or more registration groups cannot be assigned a stock reference
            year.
    """
    merge_columns = _get_stock_year_merge_columns(stock_year, survival_grouping)

    registrations = pd.merge(
        registrations,
        stock_year[merge_columns + [stock_year_empirical_csp_data_dim]],
        on=merge_columns,
        how="left",
        validate="many_to_one",
    )

    missing_reference_year = registrations[stock_year_empirical_csp_data_dim].isna()
    if missing_reference_year.any():
        missing_groups = (
            registrations.loc[missing_reference_year, merge_columns]
            .drop_duplicates()
            .head(10)
            .to_dict(orient="records")
        )
        raise ValueError(
            "Missing stock reference year while aligning registration cohorts. "
            f"Affected groups: {missing_groups}"
        )

    registrations[age_dim] = (
        registrations[stock_year_empirical_csp_data_dim]
        - registrations[time_dim]
        + 1
    )
    return filter_vehicle_age(registrations, max_age=max_age)



