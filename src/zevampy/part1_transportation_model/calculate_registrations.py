"""Calculate historical and projected vehicle registrations by powertrain."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.part1_transportation_model.preprocess_historical_registrations import preprocess_historical_registrations
from zevampy.part1_transportation_model.calculate_country_shares import calculate_country_shares
from zevampy.part1_transportation_model.calculate_projected_registrations import calculate_projected_registrations
from zevampy.part1_transportation_model.combine_shares_and_absolute_registrations import \
    combine_shares_and_absolute_registrations


def calculate_registrations(historical_registrations, countries_selected, registrations_projected,
                            clusters, registration_shares_by_cluster, reference_year, simulation_years,
                            start_registrations_year, use_clusters, output_path):
    """
    Calculate and save vehicle registrations by powertrain.

    This function combines historical registration data, projected registrations, and powertrain registration shares
    to estimate vehicle registrations by country, year, and powertrain category. The resulting datasets are saved as
     CSV files in the specified output directory.

    Parameters:
        historical_registrations (pandas.DataFrame):
            Historical vehicle registration dataset.

        countries_selected (list[str]):
            List of countries included in the simulation.

        registrations_projected (pandas.DataFrame):
            Projected total vehicle registrations by year.

        clusters (pandas.DataFrame):
            Country-cluster assignment dataset.

        registration_shares_by_cluster (pandas.DataFrame):
            Powertrain registration shares for each cluster.

        reference_year (int):
            Reference year used to calculate country-level registration shares.

        simulation_years (list[int]):
            Simulation start and end years.

        start_registrations_year (int):
            First year included in the historical registration dataset.

        use_clusters (bool):
            Whether country clusters should be used to estimate
            powertrain shares.

        output_path (str):
            Directory where output CSV files will be saved.

    Returns:
        pandas.DataFrame:
            DataFrame containing historical and projected vehicle registrations by country, year, and powertrain.
    """
    end_year = simulation_years[1]
    absolute_registrations = preprocess_historical_registrations(historical_registrations, registrations_projected,
                                                                 reference_year, countries_selected,
                                                                 start_registrations_year, end_year)
    absolute_registrations.to_csv(f'{output_path}/1_1_absolute_registrations.csv', sep=',', index=False, decimal='.')
    registrations_by_powertrain = combine_shares_and_absolute_registrations(absolute_registrations,
                                                                            registration_shares_by_cluster, clusters,
                                                                            use_clusters)
    registrations_by_powertrain.to_csv(f'{output_path}/1_2_registrations_by_powertrain.csv', sep=',', index=False,
                                       decimal='.')
    return registrations_by_powertrain
