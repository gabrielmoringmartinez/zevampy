# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from pathlib import Path
import pandas as pd
from zevampy.load_data_and_prepare_inputs.load_data import DEFAULT_INPUT_FILES, DEFAULT_SURVIVAL_FILES


INPUT_DIR = Path("inputs")

REFERENCE_FILE = INPUT_DIR / DEFAULT_INPUT_FILES["country_clusters"]

FILES_TO_CHECK = {
    "historical registrations": DEFAULT_INPUT_FILES["historical_registrations"],
    "stock by age": DEFAULT_SURVIVAL_FILES["stock_by_age"],
    "stock year": DEFAULT_SURVIVAL_FILES["stock_year"],
}


def load_countries_from_file(file_path: str, column_name: str = "geo country") -> set:
    """
       Load unique country names from a specified CSV file and column.

       Args:
           file_path (str): Path to the CSV input file.
           column_name (str): Name of the column containing country names (default "geo country").

       Returns:
           set: A set of unique country names (words) with spaces at the start and end removed.
       """
    df = pd.read_csv(file_path, delimiter=';', decimal=',')
    return set(df[column_name].dropna().str.strip().unique())


def test_countries_exist_in_reference():
    """
        Verify that all countries listed in specified input files exist in the reference country list.

        This test loads country names from each file in FILES_TO_CHECK and compares them against the
        official reference list of countries found in '0_country_clusters.csv'.

        If any country appears in an input file but not in the reference file, the test fails and
        reports which countries are unknown and in which files.

        Raises:
            AssertionError: If unknown countries are found in any of the input files.
        """
    reference_countries = load_countries_from_file(REFERENCE_FILE)

    for label, filename in FILES_TO_CHECK.items():
        path = INPUT_DIR / filename
        countries = load_countries_from_file(path)

        unknown = countries - reference_countries

        assert not unknown, (
                f"The following countries in '{filename}' are not listed in "
                f"'{REFERENCE_FILE.name}':\n"
                + "\n".join(
            f"- {country}"
            for country in sorted(unknown)
        )
        )


def test_all_files_have_consistent_country_coverage():
    """
        Check that the same set of countries is consistently present across all specified input files.

        This test ensures no country is missing from any of the input files listed in FILES_TO_CHECK.
        It identifies and reports any inconsistencies where countries appear in some files but not all.

        Raises:
            AssertionError: If any countries are missing from one or more input files.
        """
    country_sets = {}
    for label, filename in FILES_TO_CHECK.items():
        path = INPUT_DIR / filename
        country_sets[label] = load_countries_from_file(path)

    all_countries = set.union(*country_sets.values())
    inconsistencies = []

    for country in sorted(all_countries):
        present_in = [label for label, countries in country_sets.items() if country in countries]
        if len(present_in) != len(FILES_TO_CHECK):
            missing_from = set(FILES_TO_CHECK.keys()) - set(present_in)
            inconsistencies.append(
                f"- {country} is missing in: {', '.join(sorted(missing_from))}"
            )

    assert not inconsistencies, (
        "Some countries are not present in all 3 input files:\n" + "\n".join(inconsistencies)
    )
