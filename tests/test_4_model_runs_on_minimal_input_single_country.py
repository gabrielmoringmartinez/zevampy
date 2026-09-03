# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from copy import deepcopy

import pandas as pd
import pytest

from zevampy.load_data_and_prepare_inputs import load_data_and_prepare_inputs
from zevampy.load_data_and_prepare_inputs.ensure_clean_directory import ensure_clean_directory
from zevampy.part3_stock_calculation import calculate_and_plot_csps_and_stock
from zevampy.part4_validate_model import compare_model_and_actual_stock_results

test_config = {
    "data": {
        "output_path": "outputs",
    },
    "geography": {
        "countries": ["Example Country"],
        "use_clusters": True,
    },
    "powertrains": ["BEV", "Gasoline"],
    "model": {
        "first_stock_year": 2014,
        "end_year": 2050,
        "historical_validation": True,
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


@pytest.mark.parametrize("input_dir", [
    "tests/test_inputs_single_country",
    "tests/test_inputs_single_country_reduced_years"
])
def test_model_runs_on_minimal_input(input_dir, tmp_path):
    """
    Test that the full BEV stock modeling workflow runs successfully on minimal input datasets.

    This test is parameterized to run twice:
    1. Using a dataset for a single country.
    2. Using a dataset for a single country with a reduced year range.

    For each case, the test:
    - Creates isolated temporary output directories.
    - Loads data from the specified test input folder.
    - Runs CSP curve generation and BEV stock calculation.
    - Asserts that all output DataFrames are non-empty.
    - Executes the model validation step to confirm it handles reduced input correctly.

    This ensures the model runs end-to-end without errors, even when working
    with small or simplified datasets.

    Args:
        input_dir (str):
            Path to the test-specific input dataset.

        tmp_path (Path):
            Temporary directory provided by pytest for isolated test outputs.

    Raises:
        AssertionError:
            If any output DataFrame is unexpectedly empty.
    """
    # Clean output directories before running test
    output_dir = tmp_path / "outputs"
    config = deepcopy(test_config)
    config["data"]["output_path"] = str(output_dir)
    ensure_clean_directory(output_dir)
    ensure_clean_directory(output_dir / "figures")
    # Use test-specific input folder
    test_data, test_inputs = load_data_and_prepare_inputs(input_dir, config=config)
    test_csp_and_stock_calculated_data = calculate_and_plot_csps_and_stock(test_data, test_inputs)
    # Simple assertion — check result is not empty
    for key, value in test_csp_and_stock_calculated_data.items():
        if isinstance(value, pd.DataFrame):
            assert not value.empty, f"'{key}' DataFrame is unexpectedly empty"
    compare_model_and_actual_stock_results(test_data, test_csp_and_stock_calculated_data, test_inputs)