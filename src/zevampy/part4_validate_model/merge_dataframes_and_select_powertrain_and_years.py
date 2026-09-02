"""Merge and filter validation datasets for stock-share comparisons."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def merge_dataframes_and_select_powertrain_and_years(df1, df2, powertrain="BEV", years=(2014, 2023)):
    """
    Merge modelled and observed stock-share datasets.

    This function filters two datasets by powertrain and year range, renames observed share values, and merges both
    datasets for validation analysis.

    Parameters:
        df1 (pandas.DataFrame):
            DataFrame containing modelled stock-share data.

        df2 (pandas.DataFrame):
            DataFrame containing observed stock-share data.

        powertrain (str or list[str], optional):
            Powertrain category or categories included in the comparison.

        years (tuple[int, int], optional):
            Start and end years used for filtering.

    Returns:
        pandas.DataFrame:
            Merged DataFrame containing modelled and observed stock-share data.
    """
    # Accept either a single powertrain string or a list of powertrains.
    powertrains = [powertrain] if isinstance(powertrain, str) else powertrain

    # Apply filtering conditions to both DataFrames
    df1 = df1[df1[powertrain_dim].isin(powertrains)]
    df1 = df1[df1[stock_year_dim].between(years[0], years[1])]

    df2 = df2[df2[powertrain_dim].isin(powertrains)]
    df2 = df2[df2[stock_year_dim].between(years[0], years[1])]

    # Identify the first three columns for the merge
    merge_columns = df1.columns[:3].tolist()

    # Drop 'stock' column from both DataFrames
    df1 = df1.drop(columns=[stock_dim], errors='ignore')
    df2 = df2.drop(columns=[stock_dim], errors='ignore')

    # Rename 'share' column in df2 to 'actual share'
    df2 = df2.rename(columns={share_dim: f'actual {share_dim}'})

    # Merge the DataFrames on the first three columns
    merged_df = pd.merge(df1, df2, on=merge_columns, how='inner')

    return merged_df

