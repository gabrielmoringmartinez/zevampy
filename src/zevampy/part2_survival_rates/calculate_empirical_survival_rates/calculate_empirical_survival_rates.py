"""Calculate empirical vehicle survival rates."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part2_survival_rates.calculate_empirical_survival_rates.filter_vehicle_age import filter_vehicle_age
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.prepare_registrations_data import \
    prepare_registrations_data
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.obtain_survival_rates import obtain_survival_rates
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.save_dataframes import save_dataframes
from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim


def calculate_empirical_survival_rates(
    stock,
    registrations,
    stock_year,
    countries_to_keep,
    output_path,
    survival_grouping,
    csp_available_years,
):
    """Calculate empirical survival rates from stock-by-age and registration cohorts.

    Parameters:
        stock (pandas.DataFrame):
            Age-resolved vehicle stock data.
        registrations (pandas.DataFrame):
            Registration cohorts aligned with the configured survival grouping.
        stock_year (pandas.DataFrame):
            Reference year associated with each stock-by-age survival group.
        countries_to_keep (list[str]):
            Countries included in the model run.
        output_path (str):
            Directory where empirical survival-rate output is written.
        survival_grouping (list[str]):
            Dimensions defining each survival-rate group.
        csp_available_years (int):
            Maximum vehicle age retained for CSP estimation.

    Returns:
        pandas.DataFrame:
            Empirical survival rates by configured survival group and vehicle age.
    """
    stock = filter_vehicle_age(stock, max_age=csp_available_years)
    stock = stock[stock[country_dim].isin(countries_to_keep)]

    registrations = prepare_registrations_data(
        registrations,
        stock_year,
        survival_grouping,
        max_age=csp_available_years,
    )
    registrations = registrations[registrations[country_dim].isin(countries_to_keep)]
    survival_rates = obtain_survival_rates(stock, registrations, survival_grouping)
    save_dataframes(survival_rates, output_path)
    return survival_rates




