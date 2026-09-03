"""Calculate vehicle stock values from registrations and CSP curves."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part3_stock_calculation.calculate_stock.repeat_csp_data_for_all_years import repeat_csp_data_for_all_years
from zevampy.part3_stock_calculation.calculate_stock.calculate_year_of_first_registration import \
    calculate_year_of_first_registration
from zevampy.part3_stock_calculation.calculate_stock.merge_survival_rates_with_registrations import \
    merge_survival_rates_with_registrations
from zevampy.part3_stock_calculation.calculate_stock.compute_stock_values import compute_stock_values
from zevampy.part3_stock_calculation.calculate_stock.select_optimum_distribution import select_optimum_distribution
from zevampy.part3_stock_calculation.calculate_stock.cleanup_stock_data import cleanup_stock_data
from zevampy.part3_stock_calculation.calculate_stock.compute_stock_shares import compute_stock_shares
from zevampy.part3_stock_calculation.calculate_eu_share.calculate_eu_share import calculate_eu_share
from zevampy.part3_stock_calculation.calculate_stock.save_outputs import save_outputs

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def calculate_stock(registrations, csp_values, stock_years, countries_selected, output_path,
                    calculate_stock_shares, survival_grouping=None, save_options=None):
    """
    Calculate vehicle stock values and stock shares.

    This function combines vehicle registrations with fitted CSP curves to estimate vehicle stock values by country,
    stock year, vehicle age, and powertrain. Optionally, stock shares and aggregated EU-region shares are also
    calculated.

    Parameters:
        registrations (pandas.DataFrame):
            Vehicle registrations by country, year, and powertrain.

        csp_values (pandas.DataFrame):
            Fitted CSP values by survival group and vehicle age.

        stock_years (list[int]):
            Simulation start and end years.

        countries_selected (list[str]):
            Countries included in the simulation.

        output_path (str):
            Directory used for saving outputs.

        calculate_stock_shares (bool):
            If True, stock shares are calculated.

        survival_grouping (list[str], optional):
            Columns defining the survival-rate grouping.

        save_options (bool, optional):
            If True, calculated outputs are saved.

    Returns:
        tuple:
            - pandas.DataFrame:
              Calculated vehicle stock values.
            - pandas.DataFrame or None:
              Calculated stock shares if enabled, otherwise None.
    """
    if survival_grouping is None:
        survival_grouping = [country_dim]
    columns_to_drop = [survival_rate_weibull_dim, survival_rate_weibull_gaussian_dim, distribution_dim, cluster_dim,
                       stock_weibull_dim, stock_wg_dim, new_registrations_dim, relative_sales_dim,
                       registrations_by_powertrain_dim]
    survival_rates = repeat_csp_data_for_all_years(csp_values, stock_years)
    survival_rates = calculate_year_of_first_registration(survival_rates)
    stock_data = merge_survival_rates_with_registrations(survival_rates, registrations, survival_grouping)
    stock_data = compute_stock_values(stock_data)
    stock_data[stock_dim] = stock_data.apply(select_optimum_distribution, axis=1)
    stock_data = stock_data.rename(columns={time_dim: year_of_first_registration_dim})
    stock_data = cleanup_stock_data(stock_data, columns_to_drop)
    if calculate_stock_shares:
        stock_shares = compute_stock_shares(stock_data)
        stock_shares = calculate_eu_share(stock_shares, countries_selected)
    else:
        stock_shares = None
    if save_options:
        save_outputs(stock_data, stock_shares, save_options, output_path)
    return stock_data, stock_shares














