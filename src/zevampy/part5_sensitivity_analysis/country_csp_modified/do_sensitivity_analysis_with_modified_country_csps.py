"""Sensitivity analysis using modified country-specific CSP curves."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import logging

from zevampy.part2_survival_rates.plot_survival_rates.plot_all_countries import plot_all_countries
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock
from zevampy.part5_sensitivity_analysis.country_adjectives import country_adjectives
from zevampy.part5_sensitivity_analysis.country_csp_modified.replace_survival_rates_with_country_specific_csp import \
    replace_survival_rates_with_country_specific_csp
from zevampy.part5_sensitivity_analysis.country_csp_modified.update_optimal_distribution import \
    update_optimal_distribution_based_on_country_csp
from zevampy.part5_sensitivity_analysis.country_csp_modified.generate_columns_to_plot import \
    generate_columns_to_plot
from zevampy.part5_sensitivity_analysis.update_stock_shares import update_stock_shares

from zevampy.load_data_and_prepare_inputs.dimension_names import *

logger = logging.getLogger(__name__)


def do_sensitivity_analysis_with_modified_country_csps(registrations, stock_shares, survival_rates,
                                                       optimal_distribution_dict, config, countries_selected,
                                                       output_path):
    """
    Perform sensitivity analysis with modified country-specific CSPs.

    This function replaces cumulative survival probability (CSP) curves with country-specific alternatives,
    recalculates stock shares, and evaluates the resulting impact on stock-share projections.

    Parameters:
        registrations (pandas.DataFrame):
            Vehicle registration data.

        stock_shares (pandas.DataFrame):
            Calculated stock-share data.

        survival_rates (pandas.DataFrame):
            Fitted CSP values by country and vehicle age.

        optimal_distribution_dict (dict):
            Mapping between countries and selected CSP distributions.

        config (dict):
            Configuration settings for plotting and sensitivity analysis.

        countries_selected (list[str]):
            Countries included in the stock simulation.

        output_path (str):
            Directory where outputs are saved.

    Returns:
        None
    """
    plot_params = config[plot_params_dim]
    columns_to_plot = {share_dim: share_dim.capitalize()}
    stock_shares_df = stock_shares
    available_csp_countries = set(survival_rates[country_dim].unique())
    for country in plot_params[countries_selected_label]:
        if country not in available_csp_countries:
            logger.warning("Skipping sensitivity CSP replacement for '%s' because it is not available in the fitted"
                           " CSP data.", country,)
            continue

        updated_survival_rates = replace_survival_rates_with_country_specific_csp(survival_rates, country)
        updated_opt_dist_dict = update_optimal_distribution_based_on_country_csp(country, optimal_distribution_dict)
        stock_shares_are_valid = True
        stock_values, stock_shares = calculate_stock(registrations, updated_survival_rates,
                                                     plot_params[simulation_stock_years_label],
                                                     plot_params[historical_csp_label], countries_selected,
                                                     stock_shares_are_valid, output_path)
        stock_shares_df = update_stock_shares(stock_shares_df, stock_shares, country)
        columns_to_plot = generate_columns_to_plot(columns_to_plot, [country], country_adjectives)
    bev_stock_shares = stock_shares_df[stock_shares_df[powertrain_dim] == plot_params[powertrain_to_plot_label]]
    plot_all_countries(bev_stock_shares, config, columns_to_plot, None)
