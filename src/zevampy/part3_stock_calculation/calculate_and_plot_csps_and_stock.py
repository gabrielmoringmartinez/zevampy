"""Calculate CSP curves and vehicle stock results."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import warnings

from zevampy.part1_transportation_model import calculate_registrations
from zevampy.part2_survival_rates.calculate_empirical_survival_rates import calculate_empirical_survival_rates
from zevampy.part2_survival_rates.get_csp_values_from_parameters import get_csp_values_from_parameters
from zevampy.part2_survival_rates.plot_survival_rates import get_csp_plots
from zevampy.part3_stock_calculation.calculate_stock.compute_csp_values_and_compute_stock import (
    compute_csp_values_and_compute_stock,
)
from zevampy.part3_stock_calculation.calculate_stock.calculate_stock import calculate_stock
from zevampy.part3_stock_calculation.plot_stock import plot_stock_shares
from zevampy.load_data_and_prepare_inputs.dimension_names import *


def calculate_and_plot_csps_and_stock(data, inputs):
    """Calculate registrations, CSP curves, stock values, and stock shares.

    Survival assumptions can originate from stock-by-age data, user-supplied
    empirical survival rates, or user-supplied CSP parameters. All three
    routes converge on the same stock-calculation workflow.
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

    survival_source = inputs[survival_source_label]
    survival_grouping = inputs[survival_grouping_label]
    empirical_survival_rates = None

    if survival_source == survival_source_stock_by_age_label:
        registrations_for_survival = _prepare_registrations_for_survival(
            registrations,
            survival_grouping,
        )
        empirical_survival_rates = calculate_empirical_survival_rates(
            data[stock_by_age_label],
            registrations_for_survival,
            data[stock_year_label],
            inputs[countries_selected_label],
            inputs[output_path_label],
            survival_grouping,
        )
        empirical_survival_rates = _prepare_empirical_survival_rates(
            empirical_survival_rates,
            registrations,
            inputs,
            require_complete_age_coverage=False,
        )
        results = compute_csp_values_and_compute_stock(
            empirical_survival_rates,
            registrations,
            inputs[simulation_stock_years_label],
            inputs[distribution_bounds_label],
            inputs[csp_available_years_label],
            inputs[countries_selected_label],
            survival_grouping,
            inputs[output_path_label],
            _stock_shares_are_valid(registrations, empirical_survival_rates, survival_grouping),
            inputs[save_options_stock_label],
            inputs[save_fitted_csp_values_label],
        )

    elif survival_source == survival_source_empirical_label:
        empirical_survival_rates = _prepare_empirical_survival_rates(
            data[alternative_survival_rates_label].copy(),
            registrations,
            inputs,
            require_complete_age_coverage=True,
        )
        if inputs[save_fitted_csp_values_label]:
            empirical_survival_rates.to_csv(
                f"{inputs[output_path_label]}/2_2_empirical_survival_rates.csv",
                index=False,
                decimal=".",
            )
        results = compute_csp_values_and_compute_stock(
            empirical_survival_rates,
            registrations,
            inputs[simulation_stock_years_label],
            inputs[distribution_bounds_label],
            inputs[csp_available_years_label],
            inputs[countries_selected_label],
            survival_grouping,
            inputs[output_path_label],
            _stock_shares_are_valid(registrations, empirical_survival_rates, survival_grouping),
            inputs[save_options_stock_label],
            inputs[save_fitted_csp_values_label],
        )

    elif survival_source == survival_source_parameters_label:
        parameters = _prepare_parameter_groups(
            data[alternative_csp_parameters_label].copy(),
            registrations,
            inputs,
        )
        fitted_csp_values, optimal_distribution_dict = get_csp_values_from_parameters(
            parameters,
            inputs[csp_available_years_label],
            survival_grouping,
            inputs[output_path_label],
            inputs[save_fitted_csp_values_label],
        )
        stock_shares_are_valid = _stock_shares_are_valid(
            registrations,
            parameters,
            survival_grouping,
        )
        stock_values, stock_shares = calculate_stock(
            registrations,
            fitted_csp_values,
            inputs[simulation_stock_years_label],
            inputs[countries_selected_label],
            inputs[output_path_label],
            stock_shares_are_valid,
            survival_grouping,
            inputs[save_options_stock_label],
        )
        results = (
            stock_values,
            stock_shares,
            parameters,
            optimal_distribution_dict,
            fitted_csp_values,
        )

    else:
        raise ValueError(f"Unsupported survival-rate source: {survival_source}")

    stock_values, stock_shares, optimum_parameters_wg, optimal_distribution_dict, fitted_csp_values = results

    if empirical_survival_rates is not None:
        get_csp_plots(
            empirical_survival_rates,
            fitted_csp_values,
            inputs[config_all_label],
            inputs[config_group_label],
            survival_grouping,
        )

    stock_shares_are_valid = stock_shares is not None
    if not stock_shares_are_valid:
        warnings.warn(
            "Stock shares will not be plotted because not all registration powertrains "
            "have corresponding survival assumptions. Absolute stock is still available "
            "for powertrains with survival assumptions.",
            UserWarning,
        )
    else:
        plot_stock_shares(
            stock_shares,
            inputs[config_bev_reference_scenario_label],
            inputs[powertrain_dim],
        )

    return {
        registrations_label: registrations,
        empirical_survival_rates_label: empirical_survival_rates,
        stock_values_label: stock_values,
        stock_shares_label: stock_shares,
        optimum_parameters_wg_label: optimum_parameters_wg,
        optimal_distribution_dict_label: optimal_distribution_dict,
        fitted_csp_values_label: fitted_csp_values,
    }


def _prepare_registrations_for_survival(registrations, survival_grouping):
    if powertrain_dim in survival_grouping:
        return (
            registrations
            .drop(columns=[new_registrations_dim])
            .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
        )
    return (
        registrations
        .groupby([country_dim, time_dim], as_index=False)[registrations_by_powertrain_dim]
        .sum()
        .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
    )


def _filter_survival_groups(df, registrations, inputs):
    result = df[df[country_dim].isin(inputs[countries_selected_label])].copy()
    if powertrain_dim in inputs[survival_grouping_label] and powertrain_dim in result.columns:
        registration_powertrains = set(registrations[powertrain_dim].dropna().unique())
        result = result[result[powertrain_dim].isin(registration_powertrains)].copy()
    if result.empty:
        raise ValueError(
            "No survival assumptions remain after applying the configured countries and powertrains."
        )
    return result


def _prepare_empirical_survival_rates(survival_rates, registrations, inputs, require_complete_age_coverage):
    survival_rates = _filter_survival_groups(survival_rates, registrations, inputs)
    csp_years = inputs[csp_available_years_label]
    survival_rates = survival_rates[survival_rates[age_dim] <= csp_years].copy()

    if require_complete_age_coverage:
        expected_ages = set(range(1, csp_years + 1))
        incomplete_groups = []
        for group_values, group_df in survival_rates.groupby(inputs[survival_grouping_label]):
            available_ages = set(group_df[age_dim].astype(int).unique())
            if available_ages != expected_ages or len(group_df) != csp_years:
                if not isinstance(group_values, tuple):
                    group_values = (group_values,)
                group = dict(zip(inputs[survival_grouping_label], group_values))
                incomplete_groups.append(group)
        if incomplete_groups:
            raise ValueError(
                "Alternative empirical survival-rate data must contain exactly one value "
                f"for every vehicle age from 1 to {csp_years} in each survival group. "
                f"Incomplete groups: {incomplete_groups[:5]}"
            )
    return survival_rates


def _prepare_parameter_groups(parameters, registrations, inputs):
    return _filter_survival_groups(parameters, registrations, inputs)


def _stock_shares_are_valid(registrations, survival_data, survival_grouping):
    if powertrain_dim not in survival_grouping:
        return True
    registration_powertrains = set(registrations[powertrain_dim].dropna().unique())
    survival_powertrains = set(survival_data[powertrain_dim].dropna().unique())
    return not (registration_powertrains - survival_powertrains)
