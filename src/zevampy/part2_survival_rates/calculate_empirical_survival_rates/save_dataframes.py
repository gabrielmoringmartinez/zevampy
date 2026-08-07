"""Save empirical survival-rate datasets."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT


def save_dataframes(survival_rates, output_path, filename="2_2_empirical_survival_rates.csv"):
    """
    Save empirical survival-rate data to CSV files.

    Parameters:
        survival_rates (pandas.DataFrame):
            DataFrame containing empirical survival rates.

        output_path (str):
            Directory where the CSV file is saved.

    Returns:
        None
    """
    survival_rates.to_csv(f'{output_path}/{filename}', sep=';', index=False, decimal=',')
