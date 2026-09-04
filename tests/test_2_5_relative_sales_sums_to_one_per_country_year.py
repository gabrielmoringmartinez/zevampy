# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from pathlib import Path

import pandas as pd

from zevampy.load_data_and_prepare_inputs.load_data import DEFAULT_INPUT_FILES


INPUT_DIR = Path("inputs")
FILENAME = DEFAULT_INPUT_FILES["registration_shares"]
TOLERANCE = 1e-6


def test_relative_sales_are_valid_per_country_year():
    """Verify that powertrain shares are bounded and never exceed the total market.

    ZEVAMPY allows registration-share inputs to represent only a subset of the
    market, so selected/available shares may sum to less than 1. They must not
    be negative, exceed 1 individually, or sum to more than 1 for a country and
    year.
    """
    path = INPUT_DIR / FILENAME
    df = pd.read_csv(path, delimiter=";", decimal=",")

    required_cols = {"time", "geo country", "relative sales"}
    missing = required_cols - set(df.columns)
    assert not missing, f"Missing columns in {FILENAME}: {sorted(missing)}"

    df["relative sales"] = pd.to_numeric(df["relative sales"], errors="coerce")
    assert not df["relative sales"].isna().any(), (
        f"File '{FILENAME}' contains missing or non-numeric relative sales."
    )
    assert (df["relative sales"] >= -TOLERANCE).all(), (
        f"File '{FILENAME}' contains negative relative sales."
    )
    assert (df["relative sales"] <= 1 + TOLERANCE).all(), (
        f"File '{FILENAME}' contains relative sales above 1."
    )

    grouped = df.groupby(["time", "geo country"])["relative sales"].sum()
    invalid = grouped[grouped > 1 + TOLERANCE]

    if not invalid.empty:
        details = "\n".join(
            f"{country} in {year}: sum = {value}"
            for (year, country), value in invalid.items()
        )
        raise AssertionError(
            f"In file '{FILENAME}', relative sales exceed 1 for the following "
            f"year-country combinations:\n{details}"
        )
