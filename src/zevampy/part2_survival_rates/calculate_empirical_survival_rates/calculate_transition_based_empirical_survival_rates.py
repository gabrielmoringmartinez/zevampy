"""Calculate transition-based empirical vehicle survival rates."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import filter_vehicle_age
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.obtain_transition_based_survival_rates import (
    obtain_transition_based_survival_rates,
)


def calculate_transition_based_empirical_survival_rates(
    stock,
    registrations,
    countries_to_keep,
    output_path,
    survival_grouping,
):
    """Calculate empirical CSPs from consecutive stock snapshots."""
    stock = filter_vehicle_age(stock)
    stock = stock[stock[country_dim].isin(countries_to_keep)].copy()
    registrations = registrations[registrations[country_dim].isin(countries_to_keep)].copy()

    survival_rates = obtain_transition_based_survival_rates(
        stock,
        registrations,
        survival_grouping,
    )
    return survival_rates
