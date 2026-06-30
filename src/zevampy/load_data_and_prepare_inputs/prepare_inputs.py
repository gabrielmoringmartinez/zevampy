"""Prepare model inputs and plot configuration settings for ZEVAMPY."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part1_transportation_model.input_data import eu_countries_and_norway, default_use_clusters, \
    default_powertrains
from zevampy.part2_survival_rates.input_data import distribution_bounds
from zevampy.part3_stock_calculation.calculate_stock.input_data import initial_simulation_stock_year, \
    historical_csp, \
    save_options_stock, csp_data_ref_year, csp_available_years, save_fitted_csp_values, initial_registration_year
from zevampy.part2_survival_rates.plot_survival_rates.graph_inputs import config_all, config_group
from zevampy.part3_stock_calculation.plot_stock.graph_inputs import config_bev_reference_scenario
from zevampy.part4_validate_model.graph_inputs import config_validation_step1, config_validation_step2
from zevampy.part4_validate_model.rmse_inputs import config_validation_rmse_step1, config_validation_rmse_step2
from zevampy.part5_sensitivity_analysis.graph_inputs import config_sensitivity_1, config_sensitivity_2, \
    config_sensitivity_3, config_sensitivity_4

from zevampy.load_data_and_prepare_inputs.dimension_names import *
import warnings
import os


def prepare_inputs(simulation_end_year, config=None):
    """
    Prepare simulation parameters and plot configurations.

    This function combines default settings with optional user-defined
    configuration values. It prepares model parameters such as selected
    countries, powertrains, stock simulation years, CSP settings, validation
    options, sensitivity-analysis options, output paths, and plot
    configurations.

    Parameters:
        simulation_end_year (int):
            Final year available in the projected registrations dataset.

        config (dict, optional):
            Configuration dictionary loaded from a YAML file. If None or
            empty, default model settings are used.

    Returns:
        dict:
            Dictionary containing simulation parameters and plot
            configuration settings.

    Raises:
        ValueError:
            If the available registration history is shorter than the
            configured CSP time horizon.

    Warns:
        UserWarning:
            If `csp_available_years` is lower than the typical value of
            45 years.
    """
    data_config = config.get("data", {})
    outputs_config = data_config.get("output_path", "outputs")
    model_config = config.get("model", {})
    geography_config = config.get("geography") or {}
    powertrains = config.get("powertrains") or default_powertrains
    csp_plot_years = config.get("csp_plot_years") or {}
    initial_stock_year = model_config.get("first_stock_year", initial_simulation_stock_year)
    initial_new_registrations_year = model_config.get("start_new_registration_year", initial_registration_year)
    end_year = model_config.get("end_year", simulation_end_year)
    simulation_stock_years = [initial_stock_year, end_year]
    countries = geography_config.get("countries") or eu_countries_and_norway
    use_clusters = geography_config.get("use_clusters", default_use_clusters)
    csp_ref_year = model_config.get("csp_reference_year", csp_data_ref_year)
    csp_avail_years = model_config.get("csp_available_years", csp_available_years)
    historical_csp_active = model_config.get("historical_csp", historical_csp)
    historical_validation_active = model_config.get("historical_validation", historical_csp)
    sensitivity_analysis_active =  model_config.get("sensitivity_analysis", historical_csp)
    survival_config = config.get("survival_rates", {})
    survival_grouping = survival_config.get("grouping", [country_dim])
    # Simulation-related parameters
    inputs_simulation = {
        countries_selected_label: countries,
        simulation_stock_years_label: simulation_stock_years,
        csp_data_ref_year_label: csp_ref_year,
        csp_available_years_label: csp_avail_years,
        historical_csp_label: historical_csp_active,
        historical_validation_label: historical_validation_active,
        sensitivity_analysis_label: sensitivity_analysis_active,
        save_options_stock_label: save_options_stock,
        save_fitted_csp_values_label: save_fitted_csp_values,
        distribution_bounds_label: distribution_bounds,
        powertrain_dim: powertrains,
        csp_plot_years_label: csp_plot_years,
        initial_registration_year_label: initial_new_registrations_year,
        use_clusters_label: use_clusters,
        output_path_label: outputs_config,
        survival_grouping_label: survival_grouping
    }
    # Plot configuration parameters
    inputs_plot_configuration = {
        config_all_label: config_all,
        config_group_label: config_group,
        config_bev_reference_scenario_label: config_bev_reference_scenario,
        config_validation_step1_label: config_validation_step1,
        config_validation_step2_label: config_validation_step2,
        config_validation_rmse_step1_label: config_validation_rmse_step1,
        config_validation_rmse_step2_label: config_validation_rmse_step2,
        config_sensitivity_1_label: config_sensitivity_1,
        config_sensitivity_2_label: config_sensitivity_2,
        config_sensitivity_3_label: config_sensitivity_3,
        config_sensitivity_4_label: config_sensitivity_4,
    }
    inputs = {
        **inputs_simulation,
        **inputs_plot_configuration
    }
    figures_path = os.path.join(outputs_config, "figures/")
    for plot_config_label in [
        config_all_label,
        config_group_label,
        config_bev_reference_scenario_label,
        config_validation_step1_label,
        config_validation_step2_label,
        config_sensitivity_1_label,
        config_sensitivity_2_label,
        config_sensitivity_3_label,
        config_sensitivity_4_label,
    ]:
        inputs[plot_config_label][file_info_dim][folder_dim] = figures_path

    x_lim = tuple(simulation_stock_years)
    for plot_config_label in [
        config_bev_reference_scenario_label,
        config_sensitivity_1_label,
        config_sensitivity_2_label,
        config_sensitivity_3_label,
        config_sensitivity_4_label,
    ]:
        inputs[plot_config_label]["plot_params"]["x_lim"] = x_lim

    available_registration_history = (initial_stock_year - initial_new_registrations_year) + 1
    if available_registration_history < csp_avail_years:
        raise ValueError(
            "Invalid model configuration: not enough historical registration data "
            "to calculate stock accurately.\n\n"

            f"start_new_registration_year = {initial_new_registrations_year}\n"
            f"first_stock_year = {initial_stock_year}\n"
            f"csp_available_years = {csp_avail_years}\n"
            f"available history = {available_registration_history} years\n\n"

            "Requirement:\n"
            "first_stock_year - start_new_registration_year >= csp_available_years\n\n"

            "How to fix:\n"
            f"- Set first_stock_year >= {initial_new_registrations_year + csp_avail_years - 1}\n"
            f"- OR provide older start_new_registration_year <= {initial_stock_year - csp_avail_years + 1}\n"
            "- OR reduce csp_available_years (⚠ may reduce accuracy of stock estimation)\n\n"

            "Note:\n"
            "Typical configuration uses ~45 years of CSP data. "
            "Using fewer years may undercount older vehicle stock."
        )
    if csp_avail_years < 45:
        warnings.warn(
            "csp_available_years is lower than the typical value of 45 years. "
            "This truncates the survival function and may lead to systematic "
            "underestimation of older vehicle cohorts. As a result, absolute "
            "vehicle stock levels are likely to be underestimated. The shorter "
            "the CSP time horizon, the stronger this bias becomes.",
            UserWarning
        )
    return inputs
