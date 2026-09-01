"""Sensitivity analysis using modified country-specific registration shares."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import logging

from zevampy.part2_survival_rates.plot_survival_rates.plot_all_countries import plot_all_countries
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock
from zevampy.part5_sensitivity_analysis.country_adjectives import country_adjectives
from zevampy.part5_sensitivity_analysis.country_registrations_modified.generate_columns_to_plot import \
    generate_columns_to_plot
from zevampy.part5_sensitivity_analysis.country_registrations_modified.replace_powertrain_share_registrations_with_country \
    import replace_powertrain_share_registrations_with_country
from zevampy.part5_sensitivity_analysis.update_stock_shares import update_stock_shares

from zevampy.load_data_and_prepare_inputs.dimension_names import *

logger = logging.getLogger(__name__)


def do_sensitivity_analysis_with_modified_country_registrations(registrations, stock_shares, survival_rates,
                                                                optimal_distribution_dict, config, countries_selected,
                                                                output_path):
    """
    Perform sensitivity analysis with modified country registrations.

    This function replaces country-specific registration shares, recalculates stock shares, and evaluates the resulting
    impact on vehicle stock-share projections.

    Parameters:
        registrations (pandas.DataFrame):
            Vehicle registration data.

        stock_shares (pandas.DataFrame):
            Calculated stock-share data.

        survival_rates (pandas.DataFrame):
            Fitted CSP values by country and vehicle age.

        optimal_distribution_dict (dict):
            Mapping between countries and selected CSP
            distributions.

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
    available_registration_countries = set(registrations[country_dim].unique())
    requested_countries = plot_params[countries_selected_label]

    valid_countries = [
        country for country in requested_countries
        if country in available_registration_countries
    ]

    missing_countries = [
        country for country in requested_countries
        if country not in available_registration_countries
    ]

    for country in missing_countries:
        logger.warning("Skipping registration sensitivity for '%s' because it is not available in the registration"
                       " data.", country,)
    for country in valid_countries:
        updated_registrations = replace_powertrain_share_registrations_with_country(registrations, country, plot_params)
        stock_shares_are_valid = True
        stock_values, stock_shares = calculate_stock(updated_registrations, survival_rates,
                                                     plot_params[simulation_stock_years_label],
                                                     plot_params[historical_csp_label], countries_selected,
                                                     stock_shares_are_valid, output_path)
        stock_shares_df = update_stock_shares(stock_shares_df, stock_shares, country)
        columns_to_plot = generate_columns_to_plot(columns_to_plot, [country],
                                                   country_adjectives)
    bev_stock_shares = stock_shares_df[stock_shares_df[powertrain_dim] == plot_params[powertrain_to_plot_label]]
    plot_all_countries(bev_stock_shares, config, columns_to_plot, None)
