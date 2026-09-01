# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from pathlib import Path
import pandas as pd
import pytest

INPUT_DIR = Path("inputs")


def get_all_input_csv_files():
    """
        Get a list of all CSV files in the 'inputs' directory.

        This helper function scans the 'inputs' folder and returns only files
        with a '.csv' extension, ensuring they are regular files (not directories).

        Returns:
            list of str: Filenames of all CSV files found in the inputs directory.
        """
    return [
        path.name
        for path in INPUT_DIR.glob("*.csv")
        if path.is_file()
    ]


@pytest.mark.parametrize("filename", get_all_input_csv_files())
def test_no_missing_values_in_input_csv(filename):
    """
       Test that checks input CSV files for missing or partially filled data.

       This test loads each CSV file in the 'inputs' folder with appropriate parsing settings
       (semicolon delimiter, comma decimal) and performs two checks:
       1. Verifies there are no missing values anywhere in the file.
       2. Ensures there are no partially filled rows (rows with a mix of null and non-null values).

       If either condition fails, the test will raise an AssertionError specifying the problematic file.

       Args:
           filename (str): Name of the input CSV file to be tested.

       Raises:
           AssertionError: If missing values or partially filled rows are found in the CSV.
       """
    file_path = INPUT_DIR / filename
    df = pd.read_csv(
        file_path,
        delimiter=";",
        decimal=",",
        keep_default_na=True,
        na_values=["", " ", "  ", "NA", "n/a", "null"],
    )
    # Check if any missing values exist
    assert not df.isnull().values.any(), f"Missing values found in: {filename}"

    # Optional: check that there are no partially filled rows
    partially_filled = df.notnull().any(axis=1) & df.isnull().any(axis=1)
    assert not partially_filled.any(), f"Partially filled rows found in: {filename}"
