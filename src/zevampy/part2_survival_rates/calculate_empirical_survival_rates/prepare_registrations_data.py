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


def prepare_registrations_data(registrations, stock_year, max_age=45):
    """Align historical registration cohorts with stock-reference years."""
    registrations = pd.merge(registrations, stock_year, on=country_dim, how="left")
    registrations[age_dim] = (
        registrations[stock_year_empirical_csp_data_dim]
        - registrations[time_dim]
        + 1
    )
    return filter_vehicle_age(registrations, max_age=max_age)

