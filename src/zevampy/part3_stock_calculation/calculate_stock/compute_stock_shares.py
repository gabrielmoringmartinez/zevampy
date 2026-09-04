"""Compute vehicle stock shares using the independently modelled total fleet."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import (
    country_dim,
    stock_year_dim,
    powertrain_dim,
    stock_dim,
    share_dim,
    total_powertrain_label,
)


def compute_stock_shares(stock_df):
    """Calculate powertrain stock shares against the complete ``Total`` fleet.

    The total fleet is calculated independently from total new registrations
    and the configured total/country survival curve. Selected technologies do
    not need to exhaustively partition the market and are never summed to
    reconstruct the denominator.
    """
    stock_grouped = (
        stock_df
        .groupby([country_dim, stock_year_dim, powertrain_dim], as_index=False)[stock_dim]
        .sum()
    )

    total_stock = stock_grouped[
        stock_grouped[powertrain_dim] == total_powertrain_label
    ][[country_dim, stock_year_dim, stock_dim]].rename(
        columns={stock_dim: f"{stock_dim}_total"}
    )

    expected_country_years = stock_grouped[[country_dim, stock_year_dim]].drop_duplicates()
    available_country_years = total_stock[[country_dim, stock_year_dim]].drop_duplicates()
    missing_total = (
        expected_country_years
        .merge(
            available_country_years,
            on=[country_dim, stock_year_dim],
            how="left",
            indicator=True,
        )
        .query("_merge == 'left_only'")
        .drop(columns="_merge")
    )
    if not missing_total.empty:
        raise ValueError(
            "Cannot calculate stock shares because the modelled Total fleet is "
            "missing for some country/year combinations: "
            f"{missing_total.head(20).to_dict(orient='records')}"
        )

    stock_merged = pd.merge(
        stock_grouped,
        total_stock,
        on=[country_dim, stock_year_dim],
        how="left",
        validate="many_to_one",
    )

    if (stock_merged[f"{stock_dim}_total"] <= 0).any():
        invalid = stock_merged.loc[
            stock_merged[f"{stock_dim}_total"] <= 0,
            [country_dim, stock_year_dim],
        ].drop_duplicates()
        raise ValueError(
            "Cannot calculate stock shares because Total stock is zero or negative "
            f"for: {invalid.head(20).to_dict(orient='records')}"
        )

    stock_merged[share_dim] = (
        stock_merged[stock_dim] / stock_merged[f"{stock_dim}_total"]
    )

    return stock_merged[
        [country_dim, stock_year_dim, powertrain_dim, stock_dim, share_dim]
    ]
