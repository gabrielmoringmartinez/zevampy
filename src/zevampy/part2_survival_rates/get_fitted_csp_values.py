"""Calculate fitted CSP values using Weibull and Weibull-Gaussian models."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd


from zevampy.part2_survival_rates.calculate_country_fitted_values import calculate_country_fitted_values
from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim, age_dim, distribution_dim, weibull_label, \
    weibull_gaussian_label


def get_fitted_csp_values(survival_rates, pdf_parameters, csp_available_years, output_path, survival_grouping,
                          save_options=False):
    """
    Calculate fitted CSP values for all survival groups.

    The function computes fitted cumulative survival probability (CSP) curves using Weibull and Weibull-Gaussian (WG)
    distribution parameters. The fitted CSP values are generated for each survival group and vehicle age, combined into
    a single DataFrame, and optionally saved as a CSV file.

    Parameters:
        survival_rates (pandas.DataFrame):
            DataFrame containing empirical survival rates.

        pdf_parameters (pandas.DataFrame):
            DataFrame containing fitted Weibull and Weibull-Gaussian distribution parameters.

        csp_available_years (int):
            Number of vehicle ages (years) for which CSP values are calculated.

        output_path (str):
            Directory where fitted CSP outputs are saved.

        survival_grouping (list):
            List of column names defining the survival-rate grouping dimensions (e.g. country or powertrain).

        save_options (bool, optional):
            If True, save the fitted CSP values to a CSV file. Defaults to False.

    Returns:
        pandas.DataFrame:
            DataFrame containing fitted CSP values for all survival groups, vehicle ages, and distribution types.
    """
    survival_groups = survival_rates[survival_grouping].drop_duplicates()
    weibull_results = pd.DataFrame()
    wg_results = pd.DataFrame()
    for _, group in survival_groups.iterrows():
        mask = True
        for dim in survival_grouping:
            mask = mask & (survival_rates[dim] == group[dim])

        survival_rates_group = survival_rates.loc[mask].copy()

        weibull_results, wg_results = calculate_country_fitted_values(
            group,
            survival_rates_group,
            pdf_parameters,
            weibull_results,
            wg_results,
            csp_available_years,
            survival_grouping
        )

    fitted_csp_values = pd.merge(
        weibull_results,
        wg_results,
        on=survival_grouping + [age_dim],
        suffixes=(f" {weibull_label}", f" {weibull_gaussian_label}"),
        how="inner"
    )

    fitted_csp_values = pd.merge(
        fitted_csp_values,
        pdf_parameters[survival_grouping + [distribution_dim]],
        on=survival_grouping,
        how="left"
    )

    if save_options:
        fitted_csp_values.to_csv(
            f"{output_path}/2_3_fitted_CSP_curves.csv",
            sep=",",
            index=False,
            decimal="."
        )

    return fitted_csp_values

