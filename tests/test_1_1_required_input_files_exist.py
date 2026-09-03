from pathlib import Path

from zevampy.load_data_and_prepare_inputs.load_data import (
    DEFAULT_INPUT_FILES,
    DEFAULT_SURVIVAL_FILES,
)


def test_default_model_input_files_exist():
    """Verify that the core files required by the default ZEVAMPY example exist."""
    input_dir = Path("inputs")

    required_keys = [
        "country_clusters",
        "registration_shares",
        "historical_registrations",
        "projected_registrations",
    ]

    for key in required_keys:
        file_path = input_dir / DEFAULT_INPUT_FILES[key]
        assert file_path.is_file(), (
            f"Required default input file is missing for '{key}': {file_path}"
        )


def test_default_stock_by_age_survival_files_exist():
    """Verify that the default stock-by-age survival-source files exist."""
    input_dir = Path("inputs")

    for key, filename in DEFAULT_SURVIVAL_FILES.items():
        file_path = input_dir / filename
        assert file_path.is_file(), (
            f"Required default survival input file is missing for '{key}': "
            f"{file_path}"
        )


def test_optional_validation_input_files_exist():
    """Verify that the validation datasets distributed with the example exist."""
    input_dir = Path("inputs")

    validation_keys = [
        "validation_registration_shares",
        "validation_stock_shares",
    ]

    for key in validation_keys:
        file_path = input_dir / DEFAULT_INPUT_FILES[key]
        assert file_path.is_file(), (
            f"Optional validation input file is missing for '{key}': "
            f"{file_path}"
        )
