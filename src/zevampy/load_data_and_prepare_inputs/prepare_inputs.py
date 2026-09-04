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
    csp_available_years,
    save_fitted_csp_values,
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


def prepare_inputs(simulation_end_year, data, config=None):
    """Prepare simulation parameters and plotting configuration settings.

    Parameters:
        simulation_end_year (int):
            Maximum year available in the projected-registration dataset.
        data (dict):
            Loaded model datasets used to derive configuration-dependent settings.
        config (dict or None, optional):
            Parsed ZEVAMPY configuration.

    Returns:
        dict:
            Internal simulation, survival, validation, output, and plot settings.

    Raises:
        ValueError:
            If the survival-source configuration is invalid, the CSP horizon is
            invalid, historical registrations do not cover the required cohort
            horizon, or the validation powertrain is not selected.
    """
    config = config or {}
    data_config = config.get("data") or {}
    outputs_config = data_config.get("output_path", "outputs")
    model_config = config.get("model") or {}
    geography_config = config.get("geography") or {}
    survival_config = config.get("survival_rates") or {}

    powertrains = config.get("powertrains") or default_powertrains
    initial_stock_year = model_config.get("first_stock_year", initial_simulation_stock_year)
    end_year = model_config.get("end_year", simulation_end_year)
    simulation_stock_years = [initial_stock_year, end_year]
    countries = geography_config.get("countries") or eu_countries_and_norway
    use_clusters = geography_config.get("use_clusters", default_use_clusters)
    csp_avail_years = survival_config.get("csp_available_years", csp_available_years)
    historical_validation_active = model_config.get("historical_validation", False)
    validation_powertrain = model_config.get("validation_powertrain", validation_powertrain_default)
    survival_grouping = survival_config.get("grouping", [country_dim])
    survival_source = survival_config.get("source", survival_source_stock_by_age_label)
    survival_files = survival_config.get("files") or {}

    if survival_source not in VALID_SURVIVAL_SOURCES:
        raise ValueError(
            f"Invalid survival_rates.source '{survival_source}'. "
            f"Supported values are: {sorted(VALID_SURVIVAL_SOURCES)}"
        )

    _validate_survival_file_configuration(survival_source, survival_files)

    if not isinstance(csp_avail_years, int) or csp_avail_years < 1:
        raise ValueError("survival_rates.csp_available_years must be a positive integer.")

    # The earliest registration cohort is derived from the first stock year
    # and the CSP horizon. For stock-by-age inputs, an earlier stock reference
    # year may require additional historical registration cohorts to estimate
    # the empirical survival rates.
    earliest_reference_year = initial_stock_year
    if survival_source == survival_source_stock_by_age_label:
        stock_year = data[stock_year_label]
        earliest_stock_reference_year = int(
            stock_year[stock_year_empirical_csp_data_dim].min()
        )
        earliest_reference_year = min(
            initial_stock_year,
            earliest_stock_reference_year,
        )

    initial_new_registrations_year = earliest_reference_year - csp_avail_years + 1

    _validate_historical_registration_coverage(
        data[historical_registrations_label],
        countries,
        initial_new_registrations_year,
    )

    inputs_simulation = {
        countries_selected_label: countries,
        simulation_stock_years_label: simulation_stock_years,
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


def _validate_survival_file_configuration(survival_source, survival_files):
    """Validate source-specific survival file settings.

    Parameters:
        survival_source (str):
            Configured survival-rate source.
        survival_files (dict):
            Mapping of survival-source input file keys to filenames.

    Raises:
        ValueError:
            If an empirical or parameter source is selected without its required
            input filename.
    """
    if survival_source == survival_source_empirical_label and not survival_files.get("empirical"):
        raise ValueError(
            "survival_rates.files.empirical must be provided when "
            "survival_rates.source is 'empirical'."
        )
    if survival_source == survival_source_parameters_label and not survival_files.get("parameters"):
        raise ValueError(
            "survival_rates.files.parameters must be provided when "
            "survival_rates.source is 'parameters'."
        )


def _validate_historical_registration_coverage(
    historical_registrations,
    countries,
    required_start_year,
):
    """Validate historical registration coverage for all selected countries.

    Parameters:
        historical_registrations (pandas.DataFrame):
            Historical total new registrations by country and year.
        countries (list[str]):
            Countries included in the model run.
        required_start_year (int):
            Earliest registration cohort needed for the configured stock year and
            CSP horizon.

    Raises:
        ValueError:
            If a selected country is absent or begins later than the required
            registration cohort year.
    """
    selected = historical_registrations[
        historical_registrations[country_dim].isin(countries)
    ]
    earliest_years = selected.groupby(country_dim)[time_dim].min()

    missing_countries = sorted(set(countries) - set(earliest_years.index))
    if missing_countries:
        raise ValueError(
            "Historical registration data are missing for selected countries: "
            f"{missing_countries}"
        )

    insufficient = earliest_years[earliest_years > required_start_year]
    if not insufficient.empty:
        details = ", ".join(
            f"{country}: starts {int(year)}"
            for country, year in insufficient.items()
        )
        raise ValueError(
            "Historical registration data do not cover the full cohort horizon. "
            f"The configured first stock year and CSP horizon require registrations "
            f"from {required_start_year} onward. Insufficient coverage: {details}."
        )


