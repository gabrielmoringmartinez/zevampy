"""Calculate CSP curves and vehicle stock results."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part1_transportation_model import calculate_registrations
from zevampy.part2_survival_rates.calculate_empirical_survival_rates import calculate_empirical_survival_rates
from zevampy.part3_stock_calculation.calculate_stock.compute_csp_values_and_compute_stock import \
    compute_csp_values_and_compute_stock
from zevampy.part2_survival_rates.plot_survival_rates import get_csp_plots
from zevampy.part3_stock_calculation.plot_stock import plot_stock_shares

from zevampy.load_data_and_prepare_inputs.dimension_names import *
import warnings


def calculate_and_plot_csps_and_stock(data, inputs):
    """
    Calculate CSP curves, vehicle stock values, and stock shares.

    This function performs the complete CSP-based stock-calculation workflow, including vehicle registrations,
    empirical survival-rate estimation, CSP fitting, stock calculations, and visualization of CSP curves and stock
    shares.

    The workflow includes:
    1. Calculating historical and projected vehicle registrations.
    2. Estimating empirical survival rates.
    3. Computing CSP curves and vehicle stock values.
    4. Generating CSP plots.
    5. Plotting vehicle stock shares.

    Parameters:
        data (dict):
            Dictionary containing input datasets.

        inputs (dict):
            Dictionary containing model settings and plotting
            configurations.

    Returns:
        dict:
            Dictionary containing calculated registrations, empirical survival rates, stock values, stock shares,
            fitted CSP parameters, and fitted CSP curves.

    Raises:
        KeyError:
            If required input keys are missing.

        ValueError:
            If provided data dimensions or formats are invalid.
    """
    registrations = calculate_registrations(data[historical_registrations_label], inputs[countries_selected_label],
                                            data[registrations_projected_label], data[clusters_label],
                                            data[registration_shares_by_cluster_label], inputs[csp_data_ref_year_label],
                                            inputs[simulation_stock_years_label],
                                            inputs[initial_registration_year_label], inputs[use_clusters_label],
                                            inputs[output_path_label])
    registrations_for_survival = registrations.copy()

    if powertrain_dim in inputs[survival_grouping_label]:
        registrations_for_survival = (
            registrations
            .drop(columns=[new_registrations_dim])
            .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
        )
    else:
        registrations_for_survival = (
            registrations_for_survival
            .groupby([country_dim, time_dim], as_index=False)[registrations_by_powertrain_dim]
            .sum()
            .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
        )
    registrations_for_survival=data[historical_registrations_label]
    data[stock_by_age_label].to_csv(f'outputs/TEST_stock_by_age.csv', sep=';', index=False, decimal=',')
    registrations_for_survival.to_csv(f'outputs/TEST_registrations_for_survival.csv', sep=';', index=False, decimal=',')
    empirical_survival_rates = calculate_empirical_survival_rates(data[stock_by_age_label], registrations_for_survival,
                                                                  data[stock_year_label],
                                                                  inputs[countries_selected_label],
                                                                  inputs[output_path_label],
                                                                  inputs[survival_grouping_label])

    if powertrain_dim in inputs[survival_grouping_label] and powertrain_dim in registrations.columns:
        registration_powertrains = set(registrations[powertrain_dim].dropna().unique())
    else:
        registration_powertrains = set()

    survival_powertrains = (
        set(empirical_survival_rates[powertrain_dim].dropna().unique())
        if powertrain_dim in empirical_survival_rates.columns
        else registration_powertrains
    )

    missing_survival_powertrains = registration_powertrains - survival_powertrains
    stock_shares_are_valid = not missing_survival_powertrains

    empirical_survival_rates = empirical_survival_rates[empirical_survival_rates[age_dim] <=
                                                        inputs[csp_available_years_label]].copy()
    optimum_parameters_wg, optimal_distribution_dict, fitted_csp_values = \
        compute_csp_values_and_compute_stock(empirical_survival_rates, registrations,
                                             inputs[simulation_stock_years_label],
                                             inputs[distribution_bounds_label], inputs[historical_csp_label],
                                             inputs[csp_available_years_label], inputs[countries_selected_label],
                                             inputs[survival_grouping_label], inputs[output_path_label],
                                             stock_shares_are_valid, inputs[save_options_stock_label],
                                             inputs[save_fitted_csp_values_label],
                                             )
    get_csp_plots(empirical_survival_rates, fitted_csp_values, inputs[config_all_label], inputs[config_group_label],
                  inputs[survival_grouping_label], inputs[powertrain_dim])
    return {
        registrations_label: registrations,
        empirical_survival_rates_label: empirical_survival_rates,
        optimum_parameters_wg_label: optimum_parameters_wg,
        optimal_distribution_dict_label: optimal_distribution_dict,
        fitted_csp_values_label: fitted_csp_values
    }