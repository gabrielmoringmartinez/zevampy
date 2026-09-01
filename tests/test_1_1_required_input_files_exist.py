# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from pathlib import Path
from zevampy.load_data_and_prepare_inputs.load_data import DEFAULT_INPUT_FILES


def test_required_input_files_exist():
    """
    Test to verify that all required input data files exist in the 'inputs' directory.

    This test checks three categories of input files necessary for the modeling workflow:
    1. Essential inputs required for core calculations.
    2. Validation inputs used to compare model outputs with observed data.
    3. Sensitivity analysis inputs needed for parameter variation studies.

    The test asserts that each file exists and raises an informative error message
    indicating the missing file and its category if any file is not found.

    Raises:
        AssertionError: If any of the required input files is missing.
    """
    # Define required input files by category
    input_dir = Path("inputs")

    essential_inputs = [
        DEFAULT_INPUT_FILES["country_clusters"],
        DEFAULT_INPUT_FILES["registration_shares"],
        DEFAULT_INPUT_FILES["historical_registrations"],
        DEFAULT_INPUT_FILES["projected_registrations"],
        DEFAULT_INPUT_FILES["stock_by_age"],
        DEFAULT_INPUT_FILES["stock_year"],
    ]

    validation_inputs = [
        DEFAULT_INPUT_FILES["validation_registration_shares"],
        DEFAULT_INPUT_FILES["validation_stock_shares"],
    ]

    sensitivity_inputs = [
        DEFAULT_INPUT_FILES["historical_csp_parameters"],
        DEFAULT_INPUT_FILES["historical_survival_rates"],
    ]

    all_required_files = {
        "essential": essential_inputs,
        "validation": validation_inputs,
        "sensitivity": sensitivity_inputs
    }

    for category, files in all_required_files.items():
        for filename in files:
            file_path = input_dir / filename
            assert file_path.exists(), (
                f"Missing {category} input file: {file_path}"
            )
