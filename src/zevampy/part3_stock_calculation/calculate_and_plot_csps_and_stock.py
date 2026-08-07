"""Calculate CSP curves and vehicle stock results."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd

from zevampy.part1_transportation_model import calculate_registrations
from zevampy.part2_survival_rates.calculate_empirical_survival_rates import calculate_empirical_survival_rates
from zevampy.part2_survival_rates.calculate_empirical_survival_rates.save_dataframes import save_dataframes
from zevampy.part3_stock_calculation.calculate_stock.compute_csp_values_and_compute_stock import \
    compute_csp_values_and_compute_stock
from zevampy.part2_survival_rates.plot_survival_rates import get_csp_plots

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def calculate_and_plot_csps_and_stock(data, inputs):
    """Calculate empirical CSPs, fit CSP curves, and prepare stock-model inputs.

    Two empirical survival-rate methodologies are calculated in parallel:

    1. ``registration based``: stock of a cohort divided by its original new
       registrations.
    2. ``transition based``: first point based on registrations, followed by
       year-to-year stock transitions of the same cohort.

    Both empirical datasets are fitted independently with the same Weibull and
    Weibull-Gaussian fitting routines. The fitted parameter output (2_1) and
    fitted CSP output (2_3) therefore contain a ``survival rate methodology``
    column that identifies which empirical method produced each fit.
    """
    registrations = calculate_registrations(
        data[historical_registrations_label],
        inputs[countries_selected_label],
        data[registrations_projected_label],
        data[clusters_label],
        data[registration_shares_by_cluster_label],
        inputs[csp_data_ref_year_label],
        inputs[simulation_stock_years_label],
        inputs[initial_registration_year_label],
        inputs[use_clusters_label],
        inputs[output_path_label],
    )

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

    # Historical registrations are currently used for empirical CSP estimation.
    registrations_for_survival = data[historical_registrations_label]

    empirical_survival_rates = calculate_empirical_survival_rates(
        data[stock_by_age_label],
        registrations_for_survival,
        data[stock_year_label],
        inputs[countries_selected_label],
        inputs[output_path_label],
        inputs[survival_grouping_label],
    )

    # Local import avoids a package-initialization cycle in the current module layout.
    from zevampy.part2_survival_rates.calculate_empirical_survival_rates.calculate_transition_based_empirical_survival_rates import (
        calculate_transition_based_empirical_survival_rates,
    )

    transition_empirical_survival_rates = calculate_transition_based_empirical_survival_rates(
        data[stock_by_age_label],
        registrations_for_survival,
        inputs[countries_selected_label],
        inputs[output_path_label],
        inputs[survival_grouping_label],
    )

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

    empirical_survival_rates = empirical_survival_rates[
        empirical_survival_rates[age_dim] <= inputs[csp_available_years_label]
    ].copy()
    transition_empirical_survival_rates = transition_empirical_survival_rates[
        transition_empirical_survival_rates[age_dim] <= inputs[csp_available_years_label]
    ].copy()

    # Keep only genuine empirical observations. Missing or infinite CSP values
    # are not imputed. This is especially important for young BEV cohorts,
    # where older transition denominators can be zero or unavailable.
    empirical_survival_rates = empirical_survival_rates[
        empirical_survival_rates[survival_rate_dim].notna()
        & np.isfinite(empirical_survival_rates[survival_rate_dim])
    ].copy()
    transition_empirical_survival_rates = transition_empirical_survival_rates[
        transition_empirical_survival_rates[survival_rate_dim].notna()
        & np.isfinite(transition_empirical_survival_rates[survival_rate_dim])
    ].copy()

    # Store both empirical methodologies in one comparable 2_2 file. The
    # annual transition factor is deliberately excluded because it is an
    # intermediate quantity that has no registration-based equivalent and
    # would therefore introduce structural empty values.
    empirical_output_columns = (
        inputs[survival_grouping_label]
        + [age_dim, survival_rate_dim, methodology_dim]
    )
    combined_empirical_survival_rates = pd.concat(
        [
            empirical_survival_rates[empirical_output_columns],
            transition_empirical_survival_rates[empirical_output_columns],
        ],
        ignore_index=True,
        sort=False,
    )
    combined_empirical_survival_rates = combined_empirical_survival_rates.sort_values(
        inputs[survival_grouping_label] + [methodology_dim, age_dim]
    ).reset_index(drop=True)
    save_dataframes(
        combined_empirical_survival_rates,
        inputs[output_path_label],
        filename="2_2_empirical_survival_rates.csv",
    )

    # Fit both methodologies independently. A transition-based curve does not
    # need observations for every age up to csp_available_years: the optimizer
    # uses the available continuous empirical sequence, while 2_3 evaluates
    # the fitted distribution over the full configured age horizon.
    fitting_grouping = inputs[survival_grouping_label] + [methodology_dim]
    fit_columns = fitting_grouping + [age_dim, survival_rate_dim]
    combined_empirical_survival_rates_for_fit = combined_empirical_survival_rates[
        fit_columns
    ].copy()

    optimum_parameters_wg, optimal_distribution_dict, fitted_csp_values = \
        compute_csp_values_and_compute_stock(
            combined_empirical_survival_rates_for_fit,
            registrations,
            inputs[simulation_stock_years_label],
            inputs[distribution_bounds_label],
            inputs[historical_csp_label],
            inputs[csp_available_years_label],
            inputs[countries_selected_label],
            fitting_grouping,
            inputs[output_path_label],
            stock_shares_are_valid,
            inputs[save_options_stock_label],
            inputs[save_fitted_csp_values_label],
        )

    # Preserve the existing CSP plot behavior: plots continue to show the
    # registration-based method. Both methods remain available in 2_3 for
    # dedicated methodological comparison plots later.
    fitted_csp_values_registration = fitted_csp_values[
        fitted_csp_values[methodology_dim] == registration_based_method_label
    ].copy()
    get_csp_plots(
        empirical_survival_rates,
        fitted_csp_values_registration,
        inputs[config_all_label],
        inputs[config_group_label],
        inputs[survival_grouping_label],
        inputs[powertrain_dim],
        inputs[csp_plot_years_label],
    )

    return {
        registrations_label: registrations,
        empirical_survival_rates_label: empirical_survival_rates,
        transition_empirical_survival_rates_label: transition_empirical_survival_rates,
        optimum_parameters_wg_label: optimum_parameters_wg,
        optimal_distribution_dict_label: optimal_distribution_dict,
        fitted_csp_values_label: fitted_csp_values,
    }
