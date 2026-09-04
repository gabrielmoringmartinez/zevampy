"""Preprocess historical and projected vehicle registration datasets."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import country_dim, time_dim


def preprocess_historical_registrations(
    historical_registrations,
    registrations_projected,
    countries_to_keep,
    start_year,
    end_year,
):
    """Combine historical and projected total registrations for the model horizon.

    The first year in the projected-registration dataset defines the transition
    from observed historical registrations to projected values. Historical values
    are retained only for earlier years.

    Parameters:
        historical_registrations (pandas.DataFrame):
            Observed total registrations by country and year.
        registrations_projected (pandas.DataFrame):
            Projected total registrations by country and year.
        countries_to_keep (list[str]):
            Countries retained in the combined dataset.
        start_year (int):
            Earliest registration year required by the model.
        end_year (int):
            Final registration year included in the model.

    Returns:
        pandas.DataFrame:
            Combined and filtered total-registration time series.
    """
    first_projection_year = int(registrations_projected[time_dim].min())

    historical_registrations = historical_registrations[
        historical_registrations[time_dim] < first_projection_year
    ]
    registrations_projected = registrations_projected[
        registrations_projected[time_dim] >= first_projection_year
    ]

    common_cols = historical_registrations.columns.intersection(
        registrations_projected.columns
    )
    absolute_registrations = pd.concat(
        [
            historical_registrations[common_cols],
            registrations_projected[common_cols],
        ],
        ignore_index=True,
    )
    absolute_registrations = absolute_registrations[
        absolute_registrations[country_dim].isin(countries_to_keep)
    ]
    absolute_registrations = absolute_registrations[
        (absolute_registrations[time_dim] >= start_year)
        & (absolute_registrations[time_dim] <= end_year)
    ]
    return absolute_registrations


