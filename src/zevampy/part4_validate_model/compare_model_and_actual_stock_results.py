"""Validate modelled stock shares against observed vehicle-stock data."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from copy import deepcopy

# Functions
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock
from zevampy.part4_validate_model.merge_dataframes_and_select_powertrain_and_years import \
    merge_dataframes_and_select_powertrain_and_years
from zevampy.part2_survival_rates.plot_survival_rates.plot_all_countries import plot_all_countries
from zevampy.part4_validate_model.calculate_rmse import calculate_rmse
from zevampy.part4_validate_model.update_validation_registration_shares import \
    update_registration_shares_with_actual_values


from zevampy.load_data_and_prepare_inputs.dimension_names import *


def _get_validation_years(model_stock_shares, actual_stock_shares, validation_powertrain):
    actual = actual_stock_shares[
        actual_stock_shares[powertrain_dim] == validation_powertrain
    ]
    model = model_stock_shares[
        model_stock_shares[powertrain_dim] == validation_powertrain
    ]

    if actual.empty:
        raise ValueError(
            f"Validation powertrain '{validation_powertrain}' is not available "
            "in the validation stock-share dataset."
        )
    if model.empty:
        raise ValueError(
            f"Validation powertrain '{validation_powertrain}' is not available "
            "in the modelled stock-share results."
        )

    start_year = max(actual[stock_year_dim].min(), model[stock_year_dim].min())
    end_year = min(actual[stock_year_dim].max(), model[stock_year_dim].max())

    if start_year > end_year:
        raise ValueError(
            f"No overlapping validation years are available for "
            f"'{validation_powertrain}'."
        )

    return int(start_year), int(end_year)


def _prepare_plot_config(base_config, validation_powertrain, years, step):
    config = deepcopy(base_config)
    start_year, end_year = years

    config[plot_params_dim][x_lim_dim] = (start_year, end_year)
    config[plot_params_dim][x_ticks_dim] = list(range(start_year, end_year + 1, 2))
    config[plot_params_dim][y_label_dim] = f"{validation_powertrain} stock share (in %)"

    if step == 1:
        config[plot_params_dim][title_dim] = (
            f"Observed {validation_powertrain} stock shares compared with modelled shares "
            f"using observed {validation_powertrain} registration shares"
        )
        config[file_info_dim][main_title_dim] = (
            f"validation_step_1_actual_{validation_powertrain.lower()}_registrations_"
            "and_empirical_csp_curves"
        )
    else:
        config[plot_params_dim][title_dim] = (
            f"Observed {validation_powertrain} stock shares compared with modelled shares "
            f"using the original {validation_powertrain} registration trajectory"
        )
        config[file_info_dim][main_title_dim] = (
            f"validation_step_2_modelled_{validation_powertrain.lower()}_registrations_"
            "and_empirical_csp_curves"
        )

    return config


def _prepare_rmse_config(base_config, validation_powertrain, years, step):
    config = deepcopy(base_config)
    config[powertrains_rmse_label] = [[validation_powertrain]]
    config[timeframes_rmse_label] = [[years[0], years[1]]]
    config[title_dim] = (
        f"4_{step}_rmse_validation_step_{step}_"
        f"{validation_powertrain.lower()}_all_countries"
    )
    return config


def compare_model_and_actual_stock_results(data, calculated_data, inputs):
    """
    Compare modelled and observed vehicle stock-share results.

    This function validates modelled stock shares against observed vehicle stock-share data by:
    - updating registrations with observed shares for the selected validation powertrain,
    - recalculating stock values,
    - comparing modelled and observed stock shares,
    - generating validation plots, and
    - calculating RMSE metrics.

    Parameters:
        data (dict):
            Dictionary containing observed registration and stock-share datasets.

        calculated_data (dict):
            Dictionary containing model-calculated registrations, stock shares, fitted CSP values, and distribution
            assignments.

        inputs (dict):
            Dictionary containing simulation settings, plotting configurations, and RMSE-validation settings.

    Returns:
        None
    """
    registrations = calculated_data[registrations_label]
    stock_shares = calculated_data[stock_shares_label]
    fitted_csp_values = calculated_data[fitted_csp_values_label]

    validation_powertrain = inputs[validation_powertrain_label]
    actual_registration_shares = data[validation_registration_shares_label]
    actual_stock_shares = data[validation_stock_shares_label]

    registrations_with_actual_shares = update_registration_shares_with_actual_values(registrations,
                                                                                     actual_registration_shares,
                                                                                     validation_powertrain)
    _, stock_shares_with_actual_registrations = calculate_stock(registrations_with_actual_shares, fitted_csp_values,
                                                                inputs[simulation_stock_years_label],
                                                                inputs[historical_csp_label],
                                                                inputs[countries_selected_label],
                                                                inputs[output_path_label],
                                                                inputs[survival_grouping_label])
    years = _get_validation_years(stock_shares_with_actual_registrations,actual_stock_shares, validation_powertrain)
    # Validation Step 1: Compare updated stock shares
    validation_step1_df = merge_dataframes_and_select_powertrain_and_years(stock_shares_with_actual_registrations,
                                                                           actual_stock_shares, validation_powertrain,
                                                                           years)
    # Validation Step 2: Compare original stock shares
    validation_step2_df = merge_dataframes_and_select_powertrain_and_years(stock_shares, actual_stock_shares,
                                                                           validation_powertrain, years)

    # Create columns_to_plot, a dictionary to define column and legend values for the plot
    columns_to_plot = {col: col for col in validation_step1_df.columns if col in {share_dim, f'actual {share_dim}'}}
    plot_config_step1 = _prepare_plot_config(inputs[config_validation_step1_label], validation_powertrain, years, step=1)
    plot_config_step2 = _prepare_plot_config(inputs[config_validation_step2_label], validation_powertrain, years, step=2)
    plot_all_countries(validation_step1_df, plot_config_step1, columns_to_plot, None)
    plot_all_countries(validation_step2_df, plot_config_step2, columns_to_plot, None)
    rmse_config_step1 = _prepare_rmse_config(inputs[config_validation_rmse_step1_label], validation_powertrain, years,
                                             step=1)
    rmse_config_step2 = _prepare_rmse_config(inputs[config_validation_rmse_step2_label], validation_powertrain, years,
                                             step=2)
    calculate_rmse(validation_step1_df, rmse_config_step1, inputs[output_path_label])
    calculate_rmse(validation_step2_df, rmse_config_step2, inputs[output_path_label])
    return











