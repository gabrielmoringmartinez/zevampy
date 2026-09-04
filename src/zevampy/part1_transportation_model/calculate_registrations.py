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

    Total registrations are already known independently from the historical
    and projected registration inputs. They are therefore not reconstructed by
    summing selected powertrains, whose shares may intentionally cover only a
    subset of the market.
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
