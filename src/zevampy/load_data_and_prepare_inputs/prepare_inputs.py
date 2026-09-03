"""Prepare model inputs and plot configuration settings for ZEVAMPY."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import os
import warnings

from zevampy.part1_transportation_model.input_data import (
    eu_countries_and_norway,
    default_use_clusters,
    default_powertrains,
)
from zevampy.part2_survival_rates.input_data import distribution_bounds
from zevampy.part3_stock_calculation.calculate_stock.input_data import (
    initial_simulation_stock_year,
    save_options_stock,
    csp_data_ref_year,
    csp_available_years,
    save_fitted_csp_values,
    initial_registration_year,
)
from zevampy.part2_survival_rates.plot_survival_rates.graph_inputs import config_all, config_group
from zevampy.part3_stock_calculation.plot_stock.graph_inputs import config_bev_reference_scenario
from zevampy.part4_validate_model.graph_inputs import (
    config_validation_step1,
    config_validation_step2,
    validation_powertrain_default,
)
from zevampy.part4_validate_model.rmse_inputs import config_validation_rmse_step1, config_validation_rmse_step2
from zevampy.load_data_and_prepare_inputs.dimension_names import *


VALID_SURVIVAL_SOURCES = {
    survival_source_stock_by_age_label,
    survival_source_empirical_label,
    survival_source_parameters_label,
}


def prepare_inputs(simulation_end_year, config=None):
    """Prepare simulation parameters and plot configuration settings."""
    config = config or {}
    data_config = config.get("data") or {}
    outputs_config = data_config.get("output_path", "outputs")
    model_config = config.get("model") or {}
    geography_config = config.get("geography") or {}
    survival_config = config.get("survival_rates") or {}

    powertrains = config.get("powertrains") or default_powertrains
    initial_stock_year = model_config.get("first_stock_year", initial_simulation_stock_year)
    initial_new_registrations_year = model_config.get("start_new_registration_year", initial_registration_year)
    end_year = model_config.get("end_year", simulation_end_year)
    simulation_stock_years = [initial_stock_year, end_year]
    countries = geography_config.get("countries") or eu_countries_and_norway
    use_clusters = geography_config.get("use_clusters", default_use_clusters)
    csp_ref_year = model_config.get("csp_reference_year", csp_data_ref_year)
    csp_avail_years = model_config.get("csp_available_years", csp_available_years)
    historical_validation_active = model_config.get("historical_validation", False)
    validation_powertrain = model_config.get("validation_powertrain", validation_powertrain_default)
    survival_grouping = survival_config.get("grouping", [country_dim])
    survival_source = survival_config.get("source", survival_source_stock_by_age_label)
    survival_source_file = survival_config.get("file")

    if survival_source not in VALID_SURVIVAL_SOURCES:
        raise ValueError(
            f"Invalid survival_rates.source '{survival_source}'. "
            f"Supported values are: {sorted(VALID_SURVIVAL_SOURCES)}"
        )

    if survival_source != survival_source_stock_by_age_label and not survival_source_file:
        raise ValueError(
            f"survival_rates.file must be provided when survival_rates.source is '{survival_source}'."
        )

    inputs_simulation = {
        countries_selected_label: countries,
        simulation_stock_years_label: simulation_stock_years,
        csp_data_ref_year_label: csp_ref_year,
        csp_available_years_label: csp_avail_years,
        historical_validation_label: historical_validation_active,
        validation_powertrain_label: validation_powertrain,
        save_options_stock_label: save_options_stock,
        save_fitted_csp_values_label: save_fitted_csp_values,
        distribution_bounds_label: distribution_bounds,
        powertrain_dim: powertrains,
        initial_registration_year_label: initial_new_registrations_year,
        use_clusters_label: use_clusters,
        output_path_label: outputs_config,
        survival_grouping_label: survival_grouping,
        survival_source_label: survival_source,
        survival_source_file_label: survival_source_file,
    }

    inputs_plot_configuration = {
        config_all_label: config_all,
        config_group_label: config_group,
        config_bev_reference_scenario_label: config_bev_reference_scenario,
        config_validation_step1_label: config_validation_step1,
        config_validation_step2_label: config_validation_step2,
        config_validation_rmse_step1_label: config_validation_rmse_step1,
        config_validation_rmse_step2_label: config_validation_rmse_step2,
    }

    inputs = {**inputs_simulation, **inputs_plot_configuration}
    figures_path = os.path.join(outputs_config, "figures/")
    for plot_config_label in [
        config_all_label,
        config_group_label,
        config_bev_reference_scenario_label,
        config_validation_step1_label,
        config_validation_step2_label,
    ]:
        inputs[plot_config_label][file_info_dim][folder_dim] = figures_path

    inputs[config_bev_reference_scenario_label]["plot_params"]["x_lim"] = tuple(simulation_stock_years)

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
            "(first_stock_year - start_new_registration_year) + 1 >= csp_available_years\n\n"
            "How to fix:\n"
            f"- Set first_stock_year >= {initial_new_registrations_year + csp_avail_years - 1}\n"
            f"- OR provide older start_new_registration_year <= {initial_stock_year - csp_avail_years + 1}\n"
            "- OR reduce csp_available_years (may reduce stock-estimation accuracy)."
        )

    if csp_avail_years < 45:
        warnings.warn(
            "csp_available_years is lower than the typical value of 45 years. "
            "This truncates the survival function and may lead to systematic "
            "underestimation of older vehicle cohorts.",
            UserWarning,
        )

    if historical_validation_active and validation_powertrain not in powertrains:
        raise ValueError(
            f"Validation powertrain '{validation_powertrain}' is not included "
            f"in the selected model powertrains: {powertrains}"
        )

    return inputs
