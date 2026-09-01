# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from collections import defaultdict
from pathlib import Path
import pandas as pd

INPUT_DIR = Path("inputs")
DIMENSION_COLUMNS = {
    "geo country",
    "powertrain",
    "cluster",
    "year",
    "time",
}

def list_dimensions_and_unique_values():
    """
       Scan CSV input files to identify and report unique values for key dimension columns.

       This function searches all CSV files in the 'inputs' directory and extracts unique values
       from specified dimension columns (e.g., "geo country", "powertrain", "cluster", "time").
       It prints the unique values found per file and a combined list across all files for each dimension.

       Notes:
           - CSV files are read with semicolon (';') delimiter and comma (',') decimal notation.
           - Files that cannot be read will print a warning message but do not halt execution.

       Returns:
           None: Outputs are printed directly to the console.
       """
    files = INPUT_DIR.glob("*.csv")
    dimension_values = defaultdict(lambda: defaultdict(set))

    for path in files:
        try:
            df = pd.read_csv(
                path,
                delimiter=";",
                decimal=",",
            )

            for column in df.columns:
                column_clean = column.strip()

                if column_clean in DIMENSION_COLUMNS:
                    unique_values = (
                        df[column]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .unique()
                    )

                    dimension_values[column_clean][path.name] = set(unique_values)

        except Exception as exc:
            print(f"Could not read {path.name}: {exc}")

    for dimension, sources in dimension_values.items():
        print(f"\n=== Dimension: {dimension} ===")

        all_values = set()

        for filename, values in sources.items():
            print(f"From {filename}: {sorted(values)}")
            all_values |= values

        print(
            f"Combined ({len(all_values)} unique): "
            f"{sorted(all_values)}"
        )