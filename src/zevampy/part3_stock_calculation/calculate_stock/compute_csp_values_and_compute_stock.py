"""Fit CSP curves from empirical survival rates and compute vehicle stock."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part2_survival_rates.calculate_csp_parameters import calculate_csp_parameters
from zevampy.part2_survival_rates.get_fitted_csp_values import get_fitted_csp_values
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock


def compute_csp_values_and_compute_stock(
    survival_rates,
    registrations,
    stock_years,
    bounds_distributions,
    csp_available_years,
    countries_selected,
    survival_grouping,
    output_path="outputs",
    calculate_stock_shares=True,
    save_options=None,
    save_csp=False,
):
    """Fit Weibull/WG CSP curves to empirical rates and calculate stock."""
    optimum_parameters_wg, optimal_distribution_dict = calculate_csp_parameters(
        survival_rates,
        bounds_distributions,
        output_path,
        survival_grouping,
        save_csp,
    )
    fitted_csp_values = get_fitted_csp_values(
        survival_rates,
        optimum_parameters_wg,
        csp_available_years,
        output_path,
        survival_grouping,
        save_csp,
    )
    stock_values, stock_shares = calculate_stock(
        registrations,
        fitted_csp_values,
        stock_years,
        countries_selected,
        output_path,
        calculate_stock_shares,
        survival_grouping,
        save_options,
    )
    return (
        stock_values,
        stock_shares,
        optimum_parameters_wg,
        optimal_distribution_dict,
        fitted_csp_values,
    )
