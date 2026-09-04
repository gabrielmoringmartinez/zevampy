"""Load model datasets and prepare simulation input parameters."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import logging

from zevampy.load_data_and_prepare_inputs.load_data import load_data
from zevampy.load_data_and_prepare_inputs.prepare_inputs import prepare_inputs
from zevampy.load_data_and_prepare_inputs.dimension_names import (
    country_dim,
    survival_source_stock_by_age_label,
)

logger = logging.getLogger(__name__)


def load_data_and_prepare_inputs(input_path, config=None):
    """Load model datasets and derive simulation input settings.

    Parameters:
        input_path (str or pathlib.Path):
            Directory containing the configured model inputs.
        config (dict or None, optional):
            Parsed ZEVAMPY configuration. Defaults are used when omitted.

    Returns:
        tuple:
            - dict: Loaded and validated input datasets.
            - dict: Prepared simulation and plotting settings.
    """
    config = config or {}
    model_config = config.get("model") or {}
    geography_config = config.get("geography") or {}
    survival_config = config.get("survival_rates") or {}

    historical_validation_active = model_config.get("historical_validation", False)
    validation_powertrain = model_config.get("validation_powertrain", "BEV")
    use_clusters_active = geography_config.get("use_clusters", True)
    powertrains = config.get("powertrains") if config else None
    survival_grouping = survival_config.get("grouping", [country_dim])
    survival_source = survival_config.get("source", survival_source_stock_by_age_label)
    survival_files = survival_config.get("files") or {}

    data_config = config.get("data") or {}
    input_files = data_config.get("files", {})

    logger.debug(
        "Model options: historical_validation=%s, validation_powertrain=%s, "
        "use_clusters=%s, survival_grouping=%s, survival_source=%s",
        historical_validation_active,
        validation_powertrain,
        use_clusters_active,
        survival_grouping,
        survival_source,
    )

    data, max_year = load_data(
        input_path,
        historical_validation_active=historical_validation_active,
        validation_powertrain=validation_powertrain,
        use_clusters_active=use_clusters_active,
        powertrains=powertrains,
        survival_grouping=survival_grouping,
        survival_source=survival_source,
        survival_files=survival_files,
        input_files=input_files,
    )

    logger.debug(
        "Loaded %d input datasets; projected registration data extend to %s.",
        len(data),
        max_year,
    )
    inputs = prepare_inputs(max_year, data=data, config=config)
    return data, inputs

