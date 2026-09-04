"""Update modelled registration shares with observed validation values."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import *


SHARE_TOLERANCE = 1e-6


def update_registration_shares_with_actual_values(
    registrations,
    actual_registration_shares,
    validation_powertrain,
):
    """Replace one modelled powertrain registration share with observed values.

    The model-generated ``Total`` registration series remains equal to the
    independently supplied complete-market registrations. For explicitly modelled
    technologies, the baseline represented market share is preserved where
    possible, supporting both exhaustive and intentionally partial powertrain
    inputs.

    Parameters:
        registrations (pandas.DataFrame):
            Modelled registrations including relative shares and ``Total`` rows.
        actual_registration_shares (pandas.DataFrame):
            Observed registration shares used in validation step 1.
        validation_powertrain (str):
            Powertrain whose modelled share is replaced with observed values.

    Returns:
        pandas.DataFrame:
            Registration table updated with the observed validation trajectory.

    Raises:
        ValueError:
            If validation data are missing, duplicated, outside valid share bounds,
            incompatible with the modelled groups, or would require inconsistent
            represented shares.
    """
    df = registrations.copy()
    actual = actual_registration_shares[
        actual_registration_shares[powertrain_dim] == validation_powertrain
    ].copy()

    if actual.empty:
        raise ValueError(
            f"Validation registration-share data do not contain the selected "
            f"powertrain '{validation_powertrain}'."
        )

    required_columns = {country_dim, time_dim, powertrain_dim, relative_sales_dim}
    missing = required_columns - set(actual.columns)
    if missing:
        raise ValueError(
            "Validation registration-share data are missing required columns: "
            f"{sorted(missing)}"
        )

    duplicate_rows = actual.duplicated([country_dim, time_dim], keep=False)
    if duplicate_rows.any():
        raise ValueError(
            "Validation registration-share data contain multiple rows for "
            f"'{validation_powertrain}' for the same country and year."
        )

    for _, row in actual.iterrows():
        country = row[country_dim]
        year = row[time_dim]
        observed_share = float(row[relative_sales_dim])

        if observed_share < -SHARE_TOLERANCE or observed_share > 1 + SHARE_TOLERANCE:
            raise ValueError(
                f"Observed registration share for {validation_powertrain} must be between "
                f"0 and 1. Got {observed_share} for {country}, {year}."
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

        explicit_mask = group_mask & (df[powertrain_dim] != total_powertrain_label)
        other_mask = explicit_mask & (df[powertrain_dim] != validation_powertrain)

        baseline_explicit_sum = df.loc[explicit_mask, relative_sales_dim].sum()
        baseline_selected_share = df.loc[selected_mask, relative_sales_dim].iloc[0]
        baseline_other_sum = baseline_explicit_sum - baseline_selected_share

        df.loc[selected_mask, relative_sales_dim] = observed_share

        if other_mask.any() and baseline_other_sum > SHARE_TOLERANCE:
            if observed_share <= baseline_explicit_sum:
                # Preserve the amount of the market that was explicitly
                # represented before inserting the observed validation share.
                target_other_sum = baseline_explicit_sum - observed_share
            else:
                # Let the observed technology use the unmodelled remainder
                # first. Only shrink the other explicit technologies if the
                # resulting represented market would otherwise exceed 100%.
                target_other_sum = min(
                    baseline_other_sum,
                    max(0.0, 1.0 - observed_share),
                )

            df.loc[other_mask, relative_sales_dim] *= (
                target_other_sum / baseline_other_sum
            )

        explicit_share_sum = df.loc[explicit_mask, relative_sales_dim].sum()
        if explicit_share_sum > 1 + SHARE_TOLERANCE:
            raise ValueError(
                "Observed validation share is inconsistent with the explicitly "
                f"modelled powertrains for {country}, {year}: their shares sum to "
                f"{explicit_share_sum:.6f}, which exceeds 1."
            )

        df.loc[explicit_mask, registrations_by_powertrain_dim] = (
            df.loc[explicit_mask, new_registrations_dim]
            * df.loc[explicit_mask, relative_sales_dim]
        )

    total_mask = df[powertrain_dim] == total_powertrain_label
    df.loc[total_mask, relative_sales_dim] = 1.0
    df.loc[total_mask, registrations_by_powertrain_dim] = df.loc[
        total_mask, new_registrations_dim
    ]

    return df

