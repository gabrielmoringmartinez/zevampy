"""Generate CSP curves directly from user-supplied distribution parameters."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import *
from zevampy.part2_survival_rates.get_function_values import (
    get_weibull_function,
    get_weibull_and_normal_function,
)


def get_csp_values_from_parameters(
    parameters,
    csp_available_years,
    survival_grouping,
    output_path="outputs",
    save_options=False,
):
    """Generate CSP curves directly from user-supplied Weibull or WG parameters.

    The parameter table contains one row per survival group. Weibull rows require
    gamma and beta; WG rows additionally require k, mu, and sigma. Fit-quality
    metrics are not required because the parameters are supplied rather than
    estimated in this workflow.

    Parameters:
        parameters (pandas.DataFrame):
            Validated CSP parameter table.
        csp_available_years (int):
            Number of vehicle ages for which CSP values are generated.
        survival_grouping (list[str]):
            Dimensions identifying each survival group.
        output_path (str, optional):
            Directory where parameter and fitted-CSP outputs are written.
        save_options (bool, optional):
            If True, save the supplied parameters and generated CSP curves.

    Returns:
        tuple:
            - pandas.DataFrame: Generated Weibull/WG CSP values by group and age.
            - dict: Survival groups classified by selected distribution.
    """
    rows = []

    for _, parameter_row in parameters.iterrows():
        gamma = float(parameter_row[gamma_weibull_dim])
        beta = float(parameter_row[beta_weibull_dim])
        distribution = parameter_row[distribution_dim]

        weibull_values = get_weibull_function(gamma, beta, csp_available_years)

        if distribution == weibull_gaussian_label:
            wg_values = get_weibull_and_normal_function(
                gamma,
                beta,
                float(parameter_row[k_weibull_gaussian_dim]),
                float(parameter_row[mu_weibull_gaussian_dim]),
                float(parameter_row[sigma_weibull_gaussian_dim]),
                csp_available_years,
            )
        else:
            # WG values are intentionally undefined when only Weibull
            # parameters are supplied. They are not used when distribution
            # is Weibull, but the column is retained for the common internal
            # CSP schema used by the stock calculation.
            wg_values = [np.nan] * csp_available_years

        for age, (weibull_value, wg_value) in enumerate(
            zip(weibull_values, wg_values),
            start=1,
        ):
            result = {dim: parameter_row[dim] for dim in survival_grouping}
            result.update({
                age_dim: age,
                survival_rate_weibull_dim: weibull_value,
                survival_rate_weibull_gaussian_dim: wg_value,
                distribution_dim: distribution,
            })
            rows.append(result)

    fitted_csp_values = pd.DataFrame(rows)

    if save_options:
        parameters.to_csv(
            f"{output_path}/2_1_optimum_parameters_csp_curves.csv",
            index=False,
            decimal=".",
        )
        fitted_csp_values.to_csv(
            f"{output_path}/2_3_fitted_CSP_curves.csv",
            index=False,
            decimal=".",
        )

    optimal_distribution_dict = {
        dist: parameters.loc[
            parameters[distribution_dim] == dist,
            survival_grouping,
        ].to_dict(orient="records")
        for dist in parameters[distribution_dim].unique()
    }

    return fitted_csp_values, optimal_distribution_dict