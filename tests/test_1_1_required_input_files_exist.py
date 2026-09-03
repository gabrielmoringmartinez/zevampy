from pathlib import Path

from zevampy.load_data_and_prepare_inputs.load_data import DEFAULT_INPUT_FILES


def test_default_model_input_files_exist():
    """
    Verify that the input files required by the default ZEVAMPY example exist.

    The default configuration uses:
    - country clustering,
    - registration data,
    - stock-by-age data,
    - and stock-year information.

    Alternative survival-rate inputs are user supplied and are therefore
    not expected to exist in the default input directory.
    """
    input_dir = Path("inputs")

    required_keys = [
        "country_clusters",
        "registration_shares",
        "historical_registrations",
        "projected_registrations",
        "stock_by_age",
        "stock_year",
    ]

    for key in required_keys:
        file_path = input_dir / DEFAULT_INPUT_FILES[key]

        assert file_path.is_file(), (
            f"Required default input file is missing for '{key}': "
            f"{file_path}"
        )


def test_optional_validation_input_files_exist():
    """
    Verify that the validation datasets distributed with the example exist.

    These files are optional for normal model runs but are required when
    historical validation is enabled.
    """
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
