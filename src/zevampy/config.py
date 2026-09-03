"""Load configuration settings for the ZEVAMPY model."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import yaml


def load_config(path=None):
    """
    Load the model configuration from a YAML file.

    If no configuration file path is provided, a default configuration
    dictionary is returned. The configuration contains default settings
    for input/output paths, selected countries, powertrains, model years,
    historical validation, and the survival-rate source.

    Parameters:
        path (str, optional):
            Path to a YAML configuration file. If None, a default
            configuration is used.

    Returns:
        dict:
            Dictionary containing model configuration parameters.
    """
    if path is None:
        return {
            "data": {
                "input_path": "inputs",
                "output_path": "outputs",
            },
            "geography": {
                "countries": [],
                "use_clusters": True,
            },
            "powertrains": [],
            "model": {
                "start_new_registration_year": 1970,
                "first_stock_year": 2014,
                "end_year": 2050,
                "csp_reference_year": 2021,
                "csp_available_years": 45,
                "historical_validation": False,
                "validation_powertrain": "BEV",
            },
            "survival_rates": {
                "grouping": ["geo country"],
                "source": "stock_by_age",
            },
        }

    with open(path, "r") as f:
        return yaml.safe_load(f) or {}
