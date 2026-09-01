"""Calculate optimized CSP distribution parameters."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part2_survival_rates.run_diff_evol_algorithm import run_diff_evol_algorithm_weibull, \
    run_diff_evol_algorithm_weibull_gaussian
from zevampy.part2_survival_rates.select_optimal_type_of_distribution import select_optimal_type_of_distribution

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def calculate_csp_parameters(survival_rates, bounds, output_path, survival_grouping, save_options=False):
    """
    Optimize CSP distribution parameters for survival-rate groups.

    This function fits Weibull and Weibull-Gaussian distributions to
    empirical cumulative survival probability (CSP) data. It first
    estimates Weibull parameters, then estimates Weibull-Gaussian
    parameters using the fitted Weibull values as a basis. Finally, it
    selects the preferred distribution type for each survival-rate group
    and optionally saves the optimized parameters to a CSV file.

    Parameters:
        survival_rates (pandas.DataFrame):
            DataFrame containing empirical survival-rate data.

        bounds (dict):
            Dictionary defining optimization bounds for the Weibull and
            Weibull-Gaussian distribution parameters.

        output_path (str):
            Directory where optimized CSP parameters are saved if
            `save_options` is True.

        survival_grouping (list[str]):
            Column names defining the grouping used for survival-rate
            estimation, such as country or powertrain.

        save_options (bool, optional):
            If True, save the optimized CSP parameters to a CSV file.
            Defaults to False.

    Returns:
        tuple:
            - pandas.DataFrame:
                Optimized CSP parameters for each survival-rate group,
                including the selected distribution type.

            - dict:
                Dictionary mapping each selected distribution type to the
                survival-rate groups assigned to it.
    """
    # Extract bounds for Weibull and Gaussian distributions
    bounds_weibull = bounds[weibull_label]
    bounds_gaussian = bounds[weibull_gaussian_label]
    bounds_gaussian = [bounds_gaussian[k_weibull_gaussian_dim], bounds_gaussian[mu_weibull_gaussian_dim],
                       bounds_gaussian[sigma_weibull_gaussian_dim]]
    # Get the unique country names from the survival rates
    survival_groups = survival_rates[survival_grouping].drop_duplicates()
    # Run the differential evolution algorithm to optimize the Weibull parameters for each country
    optimum_parameters_weibull = run_diff_evol_algorithm_weibull(bounds_weibull, survival_groups, survival_rates,
                                                                 survival_grouping)
    # Run the differential evolution algorithm to optimize the Weibull-Gaussian parameters for each country
    optimum_parameters_weibull_gaussian = run_diff_evol_algorithm_weibull_gaussian(bounds_gaussian, survival_groups,
                                                                                   survival_rates,
                                                                                   optimum_parameters_weibull,
                                                                                   survival_grouping)
    # Select the optimal distribution type (Weibull or WG) based on the fitted parameters
    optimum_parameters_weibull_gaussian = select_optimal_type_of_distribution(optimum_parameters_weibull_gaussian)
    # Save the optimized parameters and distribution types to a CSV file
    if save_options:
        optimum_parameters_weibull_gaussian.to_csv(f'{output_path}/2_1_optimum_parameters_csp_curves.csv', sep=',',
                                                   index=False, decimal='.')
    # Create a dictionary mapping each distribution type to a list of countries
    country_opt_dist_dict = {
        dist: optimum_parameters_weibull_gaussian.loc[
            optimum_parameters_weibull_gaussian[distribution_dim] == dist,
            survival_grouping
        ].to_dict(orient="records")
        for dist in optimum_parameters_weibull_gaussian[distribution_dim].unique()
    }
    return optimum_parameters_weibull_gaussian, country_opt_dist_dict
