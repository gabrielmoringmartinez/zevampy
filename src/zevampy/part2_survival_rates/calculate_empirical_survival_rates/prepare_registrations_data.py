"""Prepare registration data for empirical survival-rate estimation."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
from zevampy.load_data_and_prepare_inputs.dimension_names import age_dim, country_dim, time_dim, \
    stock_year_empirical_csp_data_dim, stock_year_dim
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import filter_vehicle_age


def prepare_registrations_data(registrations, stock):
    """
    Prepare registration data for survival-rate estimation for all available stock years.
    """
    stock_years = (
        stock[[country_dim, stock_year_dim]]
        .drop_duplicates()
        .copy()
    )

    registrations = pd.merge(
        registrations,
        stock_years,
        on=country_dim,
        how="inner",
    )

    registrations[age_dim] = (
        registrations[stock_year_dim]
        - registrations[time_dim]
    )

    registrations = filter_vehicle_age(registrations)

    return registrations
