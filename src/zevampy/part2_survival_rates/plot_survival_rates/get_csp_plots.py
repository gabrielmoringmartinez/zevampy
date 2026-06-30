"""Generate CSP plots for all survival-rate groups."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import math
from zevampy.part2_survival_rates.plot_survival_rates.plot_all_countries import plot_all_countries
from zevampy.part2_survival_rates.plot_survival_rates.plot_group_of_countries import plot_group_of_countries
from zevampy.part2_survival_rates.plot_survival_rates.get_columns_to_plot import get_columns_to_plot

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def get_csp_plots(survival_rates, fitted_csp_values, config_all, config_group, survival_grouping, powertrains):
    """
    Generate CSP plots for all survival-rate groups.

    This function merges empirical and fitted CSP values, creates labels for the selected survival-rate grouping, and
    generates plots for all groups and selected subsets of groups.

    Parameters:
        survival_rates (pandas.DataFrame):
            DataFrame containing empirical survival-rate data.

        fitted_csp_values (pandas.DataFrame):
            DataFrame containing fitted CSP values.

        config_all (dict):
            Plot configuration for all survival-rate groups.

        config_group (dict):
            Plot configuration for grouped survival-rate plots.

        survival_grouping (list[str]):
            Column names defining the survival-rate grouping.

    Returns:
        None
    """
    # Keep only config.yaml
    print("TEST THIS")
    print(powertrains)
    print("before")
    print("(before) Powertrains in survival_rates:")
    print(survival_rates[powertrain_dim].unique())
    print("(before )Powertrains in fitted_csp_values:")
    print(fitted_csp_values[powertrain_dim].unique())
    survival_rates = survival_rates[
        survival_rates[powertrain_dim].isin(powertrains)
    ].copy()
    fitted_csp_values = fitted_csp_values[
        fitted_csp_values[powertrain_dim].isin(powertrains)
    ].copy()
    print("AFTER")
    print("(after) Powertrains in survival_rates:")
    print(survival_rates[powertrain_dim].unique())
    print("(after) Powertrains in fitted_csp_values:")
    print(fitted_csp_values[powertrain_dim].unique())
    merged_df = pd.merge(survival_rates, fitted_csp_values, on=survival_grouping + [age_dim], how='left')
    merged_df = add_survival_group_label(merged_df, survival_grouping)
    # Define column mappings for different distributions
    columns_to_plot_all = get_columns_to_plot()
    columns_to_plot_weibull = get_columns_to_plot(weibull_label)
    columns_to_plot_wg = get_columns_to_plot(weibull_gaussian_label)

    # Plot all countries
    plot_all_countries(merged_df, config_all, columns_to_plot_all, None)
    plot_all_countries(merged_df, config_all, columns_to_plot_weibull, weibull_label)
    plot_all_countries(merged_df, config_all, columns_to_plot_wg, weibull_gaussian_label)
    groups = merged_df[survival_grouping_label].unique()
    countries_per_group = config_group[plot_params_dim][number_of_countries_group_dim]

    if len(groups) > 1:
        number_of_groups = math.ceil(len(groups) / countries_per_group)
        for group in range(1, number_of_groups + 1):
            plot_group_of_countries(
                merged_df,
                group,
                config_group,
                columns_to_plot_all,
                None,
            )


def add_survival_group_label(df, survival_grouping):
    """
    Add readable labels for survival-rate groups.

    This function creates a combined label column used for plotting
    and grouping survival-rate results.

    Parameters:
        df (pandas.DataFrame):
            DataFrame containing survival-group columns.

        survival_grouping (list[str]):
            Column names defining the survival-rate grouping.

    Returns:
        pandas.DataFrame:
            DataFrame containing the added survival-group label column.
    """
    df = df.copy()

    if survival_grouping == [country_dim]:
        df[survival_grouping_label] = df[country_dim]
    else:
        df[survival_grouping_label] = df[survival_grouping].astype(str).agg(" | ".join, axis=1)

    return df

