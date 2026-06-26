"""Calculate empirical vehicle survival rates."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import filter_vehicle_age
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.prepare_registrations_data import \
    prepare_registrations_data
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.obtain_survival_rates import obtain_survival_rates
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.save_dataframes import save_dataframes
from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim


def calculate_empirical_survival_rates(stock, registrations, stock_year, countries_to_keep, output_path,
                                       survival_grouping):
    """
    Calculate empirical vehicle survival rates.

    This function estimates empirical survival rates by combining vehicle stock data with historical registration data.
    The workflow includes filtering vehicle ages, preparing registration data, calculating survival rates, and saving
    the resulting datasets.

    Parameters:
        stock (pandas.DataFrame):
            DataFrame containing vehicle stock data.

        registrations (pandas.DataFrame):
            DataFrame containing historical vehicle registration data.

        stock_year (pandas.DataFrame):
            DataFrame containing stock-year information.

        countries_to_keep (list[str]):
            List of countries included in the analysis.

        output_path (str):
            Directory where output files are saved.

        survival_grouping (list[str]):
            Column names defining the grouping used for survival-rate
            estimation.

    Returns:
        pandas.DataFrame:
            DataFrame containing calculated empirical survival rates.
    """
    # Filter stock data for vehicle age range
    stock = filter_vehicle_age(stock)
    stock = stock[stock[country_dim].isin(countries_to_keep)]
    # Prepare registrations data and calculate survival rates
    registrations = prepare_registrations_data(registrations, stock_year)
    registrations = registrations[registrations[country_dim].isin(countries_to_keep)]
    stock.to_csv(f'outputs/TEST_STOCK.csv', sep=';', index=False, decimal=',')
    registrations.to_csv(f'outputs/TEST_REGISTRATIONS.csv', sep=';', index=False, decimal=',')
    survival_rates = obtain_survival_rates(stock, registrations, survival_grouping)
    # Save outputs
    save_dataframes(survival_rates, output_path)
    return survival_rates


