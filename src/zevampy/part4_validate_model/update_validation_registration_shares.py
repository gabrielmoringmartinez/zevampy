"""Update registration shares using observed data for a selected powertrain."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import numpy as np

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def update_registration_shares_with_actual_values(registrations, actual_registration_shares, validation_powertrain):
    """Replace one powertrain's modelled registration share with observed values.

    For every country-year combination for which an observed share is available,
    the selected powertrain is replaced by the observed value. The remaining
    modelled powertrain shares are rescaled proportionally so that all shares
    continue to sum to one.
    """
    df = registrations.copy()
    actual = actual_registration_shares[
        actual_registration_shares[powertrain_dim] == validation_powertrain
    ].copy()

    if actual.empty:
        raise ValueError(
            f"Validation powertrain '{validation_powertrain}' is not available "
            "in the validation registration-share dataset."
        )

    required_columns = {country_dim, time_dim, powertrain_dim, relative_sales_dim}
    missing = required_columns - set(actual.columns)
    if missing:
        raise ValueError("Validation registration-share data are missing required columns: " f"{sorted(missing)}")

    duplicate_rows = actual.duplicated([country_dim, time_dim], keep=False)
    if duplicate_rows.any():
        raise ValueError(
            f"Validation registration-share data contain more than one row for "
            f"'{validation_powertrain}' for the same country and year."
        )

    tolerance = 1e-12

    for _, row in actual.iterrows():
        country = row[country_dim]
        year = row[time_dim]
        observed_share = row[relative_sales_dim]

        if observed_share < 0 or observed_share > 1:
            raise ValueError(
                f"Observed registration share for '{validation_powertrain}' must "
                f"be between 0 and 1, but got {observed_share} for {country}, {year}."
            )

        group_mask = (
            (df[country_dim] == country)
            & (df[time_dim] == year)
        )

        if not group_mask.any():
            continue

        selected_mask = group_mask & (df[powertrain_dim] == validation_powertrain)
        if not selected_mask.any():
            raise ValueError(
                f"Validation powertrain '{validation_powertrain}' is missing from "
                f"modelled registrations for {country}, {year}."
            )

        other_mask = group_mask & (df[powertrain_dim] != validation_powertrain)
        other_share_sum = df.loc[other_mask, relative_sales_dim].sum()
        remaining_share = 1.0 - observed_share

        df.loc[selected_mask, relative_sales_dim] = observed_share

        if other_mask.any():
            if other_share_sum > tolerance:
                scale_factor = remaining_share / other_share_sum
                df.loc[other_mask, relative_sales_dim] *= scale_factor
            elif remaining_share > tolerance:
                raise ValueError(
                    f"Cannot redistribute the remaining registration share for "
                    f"{country}, {year}: all non-{validation_powertrain} modelled "
                    "shares are zero."
                )
        elif not np.isclose(observed_share, 1.0):
            raise ValueError(
                f"Cannot set '{validation_powertrain}' to a share of {observed_share} "
                f"for {country}, {year} because no other powertrains are available."
            )

    df[registrations_by_powertrain_dim] = (
        df[new_registrations_dim] * df[relative_sales_dim]
    )

    return df
