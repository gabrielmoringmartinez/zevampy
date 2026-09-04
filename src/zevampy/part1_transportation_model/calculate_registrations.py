"""Calculate historical and projected vehicle registrations by powertrain."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.part1_transportation_model.preprocess_historical_registrations import preprocess_historical_registrations
from zevampy.part1_transportation_model.combine_shares_and_absolute_registrations import \
    combine_shares_and_absolute_registrations
from zevampy.load_data_and_prepare_inputs.dimension_names import (
    country_dim,
    time_dim,
    powertrain_dim,
    relative_sales_dim,
    new_registrations_dim,
    registrations_by_powertrain_dim,
    total_powertrain_label,
)


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
    """Calculate vehicle registrations for selected technologies and the total market.

    Parameters:
        historical_registrations (pandas.DataFrame):
            Historical total new registrations by country and year.
        countries_selected (list[str]):
            Countries included in the model run.
        registrations_projected (pandas.DataFrame):
            Projected total registrations by country and year.
        clusters (pandas.DataFrame or None):
            Country-cluster mapping used when cluster-based shares are enabled.
        registration_shares_by_cluster (pandas.DataFrame):
            Registration shares for explicitly modelled powertrains.
        simulation_years (list[int]):
            First and final stock-simulation years.
        start_registrations_year (int):
            Earliest registration cohort required by the CSP horizon.
        use_clusters (bool):
            Whether to map registration shares through country clusters.
        output_path (str):
            Directory where registration outputs are written.

    Returns:
        pandas.DataFrame:
            Registrations by country, year, and powertrain, including the internally
            generated ``Total`` rows.
    """
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
    registrations_by_powertrain = _append_total_registrations(
        registrations_by_powertrain
    )
    registrations_by_powertrain.to_csv(
        f"{output_path}/1_2_registrations_by_powertrain.csv",
        sep=",",
        index=False,
        decimal=".",
    )
    return registrations_by_powertrain


def _append_total_registrations(registrations):
    """Append one complete-market ``Total`` row per country and year.

    Total registrations are known independently from the historical and projected
    registration inputs and are therefore not reconstructed from selected
    powertrains, whose shares may intentionally cover only part of the market.

    Parameters:
        registrations (pandas.DataFrame):
            Registration table for explicitly modelled powertrains.

    Returns:
        pandas.DataFrame:
            Registration table including one ``Total`` row for each country/year.

    Raises:
        ValueError:
            If the reserved ``Total`` label is already present in the input.
    """
    if total_powertrain_label in set(registrations[powertrain_dim].dropna()):
        raise ValueError(
            f"'{total_powertrain_label}' is reserved for the model-generated "
            "complete registration series."
        )

    total_rows = (
        registrations
        .sort_values([country_dim, time_dim, powertrain_dim])
        .groupby([country_dim, time_dim], as_index=False)
        .first()
    )
    total_rows[powertrain_dim] = total_powertrain_label
    total_rows[relative_sales_dim] = 1.0
    total_rows[registrations_by_powertrain_dim] = total_rows[new_registrations_dim]

    result = pd.concat([registrations, total_rows], ignore_index=True)
    return result.sort_values([country_dim, time_dim, powertrain_dim]).reset_index(drop=True)