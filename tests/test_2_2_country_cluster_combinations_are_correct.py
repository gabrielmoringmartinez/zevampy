# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from pathlib import Path
import pandas as pd
from zevampy.load_data_and_prepare_inputs.load_data import DEFAULT_INPUT_FILES


def test_country_cluster_combinations_are_correct():
    """
    Verify that all (geo country, cluster) combinations in the default
    registrations data are valid according to the default country-cluster labels.

    Raises:
        AssertionError:
            If any (geo country, cluster) pair in the registrations data
            is not found in the reference labels.
    """
    # File paths
    input_dir = Path("inputs")

    registrations_file = input_dir / DEFAULT_INPUT_FILES["registration_shares"]
    labels_file = input_dir / DEFAULT_INPUT_FILES["country_clusters"]

    # Load both CSVs
    registrations_df = pd.read_csv(registrations_file, delimiter=';', decimal=',')
    labels_df = pd.read_csv(labels_file, delimiter=';', decimal=',')

    # Get unique (country, cluster) pairs
    registrations_pairs = set(
        registrations_df[["geo country", "cluster"]].drop_duplicates().itertuples(index=False, name=None)
    )
    labels_pairs = set(
        labels_df[["geo country", "cluster"]].drop_duplicates().itertuples(index=False, name=None)
    )

    # Identify mismatched pairs
    missing_pairs = registrations_pairs - labels_pairs

    # Fail the test if any pairs are missing
    if missing_pairs:
        missing_str = "\n".join([f"- {country}, cluster {cluster}" for country, cluster in sorted(missing_pairs)])
        raise AssertionError(
            "The following (geo country, cluster) combinations in "
            f"'{registrations_file.name}' are not present in "
            f"'{labels_file.name}':\n{missing_str}"
        )
