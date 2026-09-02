"""Load model datasets and prepare simulation input parameters."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import logging

from zevampy.load_data_and_prepare_inputs.load_data import load_data
from zevampy.load_data_and_prepare_inputs.prepare_inputs import prepare_inputs
from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim

logger = logging.getLogger(__name__)


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
    historical_validation_active = model_config.get("historical_validation", False)
    validation_powertrain = model_config.get("validation_powertrain", "BEV")
    sensitivity_analysis_active = model_config.get("sensitivity_analysis", False)
    use_clusters_active = geography_config.get("use_clusters", True)

    powertrains = config.get("powertrains") if config else None

    survival_config = config.get("survival_rates", {}) if config else {}
    survival_grouping = survival_config.get("grouping", [country_dim])

    data_config = config.get("data") or {}
    input_files = data_config.get("files", {})

    logger.debug(
        "Model options: historical_validation=%s, sensitivity_analysis=%s, " "historical_csp=%s, use_clusters=%s, survival_grouping=%s",
        historical_validation_active, sensitivity_analysis_active, historical_csp_active, use_clusters_active,
        survival_grouping, )

    data, max_year = load_data(
        input_path,
        historical_validation_active=historical_validation_active,
        validation_powertrain=validation_powertrain,
        sensitivity_analysis_active=sensitivity_analysis_active,
        historical_csp_active=historical_csp_active,
        use_clusters_active=use_clusters_active,
        powertrains=powertrains,
        survival_grouping=survival_grouping,
        input_files=input_files,
    )

    logger.debug("Loaded %d input datasets; projected registration data extend to %s.", len(data), max_year, )
    inputs = prepare_inputs(max_year, config=config)
    return data, inputs
