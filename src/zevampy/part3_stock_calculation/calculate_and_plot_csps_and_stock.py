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
    """Run the configured survival-rate and stock-calculation workflow.

    The workflow starts from modelled registrations and then either derives
    empirical survival rates from stock-by-age data, fits supplied empirical rates,
    or generates CSP curves from user-supplied parameters. All sources converge on
    the same cohort stock calculation and total-fleet stock-share denominator.

    Parameters:
        data (dict):
            Loaded datasets required by the configured survival source.
        inputs (dict):
            Prepared simulation, survival, output, and plotting settings.

    Returns:
        dict:
            Registration results, empirical survival rates when applicable, stock
            values, stock shares, fitted/selected CSP information, and CSP curves.

    Raises:
        ValueError:
            If the configured survival source is unsupported or required survival
            groups are missing.
    """
    registrations = calculate_registrations(
        data[historical_registrations_label],
        inputs[countries_selected_label],
        data[registrations_projected_label],
        data[clusters_label],
        data[registration_shares_by_cluster_label],
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
            inputs[csp_available_years_label],
        )
        empirical_survival_rates = _prepare_empirical_survival_rates(
            empirical_survival_rates,
            registrations,
            inputs,
            require_complete_age_coverage=False,
        )
        _validate_survival_group_coverage(
            empirical_survival_rates,
            registrations,
            survival_grouping,
            "stock-by-age survival data",
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
            True,
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
        _validate_survival_group_coverage(
            empirical_survival_rates,
            registrations,
            survival_grouping,
            "alternative empirical survival-rate data",
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
            True,
            inputs[save_options_stock_label],
            inputs[save_fitted_csp_values_label],
        )

    elif survival_source == survival_source_parameters_label:
        parameters = _prepare_parameter_groups(
            data[alternative_csp_parameters_label].copy(),
            registrations,
            inputs,
        )
        _validate_survival_group_coverage(
            parameters,
            registrations,
            survival_grouping,
            "alternative CSP-parameter data",
        )
        fitted_csp_values, optimal_distribution_dict = get_csp_values_from_parameters(
            parameters,
            inputs[csp_available_years_label],
            survival_grouping,
            inputs[output_path_label],
            inputs[save_fitted_csp_values_label],
        )
        stock_shares_are_valid = True
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
            "Stock-share calculation is disabled for this run. "
            "Absolute stock results remain available.",
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
    """Prepare registration cohorts for empirical survival-rate estimation.

    Parameters:
        registrations (pandas.DataFrame):
            Modelled registrations including selected technologies and ``Total``.
        survival_grouping (list[str]):
            Configured survival-rate grouping dimensions.

    Returns:
        pandas.DataFrame:
            Registration cohorts with the registration-count column expected by the
            empirical survival-rate calculation. Country-only grouping uses
            ``Total`` registrations; powertrain grouping retains each technology.
    """
    if powertrain_dim in survival_grouping:
        return (
            registrations
            .drop(columns=[new_registrations_dim])
            .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
        )
    return (
        registrations[registrations[powertrain_dim] == total_powertrain_label]
        [[country_dim, time_dim, registrations_by_powertrain_dim]]
        .rename(columns={registrations_by_powertrain_dim: new_registrations_dim})
    )


def _filter_survival_groups(df, registrations, inputs):
    """Filter survival assumptions to groups participating in the current run.

    Parameters:
        df (pandas.DataFrame):
            Empirical survival-rate or parameter table.
        registrations (pandas.DataFrame):
            Modelled registration groups for the current run.
        inputs (dict):
            Prepared model settings, including selected countries and grouping.

    Returns:
        pandas.DataFrame:
            Survival assumptions restricted to modelled countries and, when
            applicable, modelled powertrains.

    Raises:
        ValueError:
            If no survival assumptions remain after filtering.
    """
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
    """Filter and validate empirical survival rates for the configured CSP horizon.

    Parameters:
        survival_rates (pandas.DataFrame):
            Empirical survival-rate table.
        registrations (pandas.DataFrame):
            Modelled registrations defining required survival groups.
        inputs (dict):
            Prepared model settings including countries, grouping, and CSP horizon.
        require_complete_age_coverage (bool):
            If True, require exactly one value for every age from 1 through the
            configured CSP horizon in every survival group.

    Returns:
        pandas.DataFrame:
            Filtered empirical survival rates within the configured age horizon.

    Raises:
        ValueError:
            If no groups remain or complete age coverage is required but missing.
    """
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
    """Filter supplied CSP parameters to groups participating in the current run.

    Parameters:
        parameters (pandas.DataFrame):
            Validated CSP parameter table.
        registrations (pandas.DataFrame):
            Modelled registrations defining the required survival groups.
        inputs (dict):
            Prepared model settings including countries and survival grouping.

    Returns:
        pandas.DataFrame:
            Parameter rows retained for the current model run.
    """
    return _filter_survival_groups(parameters, registrations, inputs)


def _validate_survival_group_coverage(
    survival_data,
    registrations,
    survival_grouping,
    dataset_name,
):
    """Validate that every modelled survival group has an assumption.

    For country-level survival rates this requires every modelled country. For
    country-plus-powertrain survival rates it requires every modelled
    country/powertrain combination, including ``Total``. Missing groups are treated
    as an error instead of silently producing incomplete fleet results.

    Parameters:
        survival_data (pandas.DataFrame):
            Survival-rate or parameter input to validate.
        registrations (pandas.DataFrame):
            Modelled registrations defining required groups.
        survival_grouping (list[str]):
            Columns identifying one survival group.
        dataset_name (str):
            Human-readable name used in error messages.

    Raises:
        ValueError:
            If one or more modelled survival groups are missing from the supplied
            assumptions.
    """
    required_groups = registrations[survival_grouping].drop_duplicates()
    available_groups = survival_data[survival_grouping].drop_duplicates()

    missing_groups = (
        required_groups
        .merge(available_groups, on=survival_grouping, how="left", indicator=True)
        .query("_merge == 'left_only'")
        .drop(columns="_merge")
    )

    if not missing_groups.empty:
        raise ValueError(
            f"Missing survival assumptions in {dataset_name} for modelled groups: "
            f"{missing_groups.head(20).to_dict(orient='records')}"
        )

