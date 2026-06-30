"""Load model datasets and prepare simulation input parameters."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.load_data import load_data
from zevampy.load_data_and_prepare_inputs.prepare_inputs import prepare_inputs
from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim

def load_data_and_prepare_inputs(input_path, config=None):
    """
    Load input datasets and prepare simulation input parameters.

    This function combines the data-loading and input-preparation steps
    required to run the ZEVAMPY model workflow. It first loads all required
    datasets from the specified input directory and then prepares the
    simulation settings and plotting configurations based on the provided
    configuration dictionary.

    Parameters:
        input_path (str):
            Path to the directory containing the input CSV files.

        config (dict, optional):
            Configuration dictionary containing model settings, selected
            countries, powertrains, survival-rate settings, and analysis
            options. If None, default settings are used.

    Returns:
        tuple:
            - data (dict):
                Dictionary containing all loaded datasets.

            - inputs (dict):
                Dictionary containing prepared simulation inputs and
                plotting configurations.
    """
    config = config or {}
    model_config = config.get("model") or {}
    geography_config = config.get("geography") or {}

    historical_csp_active = model_config.get("historical_csp", False)
    historical_validation_active = model_config.get("historical_validation", True)
    sensitivity_analysis_active = model_config.get("sensitivity_analysis", True)
    use_clusters_active = geography_config.get("use_clusters", True)

    powertrains = config.get("powertrains") if config else None
    csp_plot_years = config.get("csp_plot_years") if config else None


    survival_config = config.get("survival_rates", {}) if config else {}
    survival_grouping = survival_config.get("grouping", [country_dim])

    data, max_year = load_data(
        input_path,
        historical_validation_active=historical_validation_active,
        sensitivity_analysis_active=sensitivity_analysis_active,
        historical_csp_active=historical_csp_active,
        use_clusters_active=use_clusters_active,
        powertrains=powertrains,
        survival_grouping=survival_grouping,

    )
    inputs = prepare_inputs(max_year, config=config)
    return data, inputs
