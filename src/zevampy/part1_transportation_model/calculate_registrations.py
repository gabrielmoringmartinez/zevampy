"""Calculate historical and projected vehicle registrations by powertrain."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part1_transportation_model.preprocess_historical_registrations import preprocess_historical_registrations
from zevampy.part1_transportation_model.combine_shares_and_absolute_registrations import \
    combine_shares_and_absolute_registrations


def calculate_registrations(
    historical_registrations,
    countries_selected,
    registrations_projected,
    clusters,
    registration_shares_by_cluster,
    simulation_years,
    start_registrations_year,
    use_clusters,
    output_path,
):
    """Calculate and save vehicle registrations by powertrain."""
    end_year = simulation_years[1]
    absolute_registrations = preprocess_historical_registrations(
        historical_registrations,
        registrations_projected,
        countries_selected,
        start_registrations_year,
        end_year,
    )
    absolute_registrations.to_csv(
        f"{output_path}/1_1_absolute_registrations.csv",
        sep=",",
        index=False,
        decimal=".",
    )
    registrations_by_powertrain = combine_shares_and_absolute_registrations(
        absolute_registrations,
        registration_shares_by_cluster,
        clusters,
        use_clusters,
    )
    registrations_by_powertrain.to_csv(
        f"{output_path}/1_2_registrations_by_powertrain.csv",
        sep=",",
        index=False,
        decimal=".",
    )
    return registrations_by_powertrain
