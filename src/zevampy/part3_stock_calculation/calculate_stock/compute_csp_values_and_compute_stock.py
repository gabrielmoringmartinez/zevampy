"""Compute fitted CSP curves and vehicle stock values."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part2_survival_rates.calculate_csp_parameters import calculate_csp_parameters
from zevampy.part2_survival_rates.get_fitted_csp_values import get_fitted_csp_values
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock


def compute_csp_values_and_compute_stock(survival_rates, registrations, stock_years, bounds_distributions,
                                         historical_csp, csp_available_years, countries_selected, survival_grouping,
                                         output_path="outputs", calculate_stock_shares=True,
                                         save_options=None, save_csp=False):
    """
    Compute fitted CSP values and vehicle stock estimates.

    This function fits Weibull and Weibull-Gaussian CSP curves, calculates fitted CSP values, and computes vehicle stock
    values and stock shares based on registrations and survival rates.

    Parameters:
        survival_rates (pandas.DataFrame):
            Empirical survival-rate data.

        registrations (pandas.DataFrame):
            Vehicle registrations by country, year, and powertrain.

        stock_years (list[int]):
            Simulation start and end years.

        bounds_distributions (dict):
            Parameter bounds used for CSP optimization.

        historical_csp (str):
            Flag indicating whether historical CSP calculations are
            enabled.

        csp_available_years (int):
            Number of CSP years used in the calculations.

        countries_selected (list[str]):
            Countries included in the simulation.

        survival_grouping (list[str]):
            Columns defining the survival-rate grouping.

        output_path (str, optional):
            Directory used for saving outputs.

        calculate_stock_shares (bool, optional):
            If True, stock shares are calculated.

        save_options (bool, optional):
            If True, stock outputs are saved.

        save_csp (bool, optional):
            If True, fitted CSP outputs are saved.

    Returns:
        tuple:
            - pandas.DataFrame:
              Calculated stock values.
            - pandas.DataFrame or None:
              Calculated stock shares.
            - pandas.DataFrame:
              Optimized CSP parameters.
            - dict:
              Optimal distribution assignments.
            - pandas.DataFrame:
              Fitted CSP values.
    """
    optimum_parameters_wg, optimal_distribution_dict = calculate_csp_parameters(survival_rates, bounds_distributions,
                                                                                output_path, survival_grouping,
                                                                                save_csp)
    fitted_csp_values = get_fitted_csp_values(survival_rates, optimum_parameters_wg, csp_available_years,
                                              output_path, survival_grouping, save_csp)
    return optimum_parameters_wg, optimal_distribution_dict, fitted_csp_values
