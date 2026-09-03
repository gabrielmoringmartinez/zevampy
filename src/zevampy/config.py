"""Load configuration settings for the ZEVAMPY model."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import yaml


def load_config(path=None):
    """
    Load the model configuration from a YAML file.

    If no configuration file path is provided, a default configuration
    dictionary is returned.

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
                "first_stock_year": 2014,
                "end_year": 2050,
                "historical_validation": False,
                "validation_powertrain": "BEV",
            },
            "survival_rates": {
                "source": "stock_by_age",
                "grouping": ["geo country"],
                "csp_available_years": 45,
                "files": {
                    "stock_by_age": "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv",
                    "stock_year": "2_2_A_1_stock_year.csv",
                },
            },
        }

    with open(path, "r") as f:
        return yaml.safe_load(f) or {}
