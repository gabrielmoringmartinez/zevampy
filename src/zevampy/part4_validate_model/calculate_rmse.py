"""Calculate RMSE metrics for stock-share model validation."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import numpy as np
from zevampy.part4_validate_model.append_values import append_values
from zevampy.load_data_and_prepare_inputs.dimension_names import *


def calculate_rmse(df, config, output_path):
    """
    Calculate RMSE values for stock-share validation results.

    This function compares predicted and actual stock shares and calculates root mean squared error (RMSE) values
    for selected countries, powertrains, and timeframes.

    Parameters:
        df (pandas.DataFrame):
            DataFrame containing predicted and actual stock shares.

        config (dict):
            Configuration dictionary containing RMSE settings, including powertrains and timeframes.

        output_path (str):
            Directory where RMSE results are saved.

    Returns:
        None
    """
    df = df.copy()
    df['error'] = df[share_dim] - df[f'actual {share_dim}']
    df['squared_error'] = df['error'] ** 2
    # Collect RMSE results for each group
    rows_rmse = []
    countries = df[country_dim].unique()

    for powertrain in config[powertrains_rmse_label]:
        filtered_powertrain_df = df[df[powertrain_dim].isin(powertrain)]

        for timeframe in config[timeframes_rmse_label]:
            filtered_timeframe_df = filtered_powertrain_df[filtered_powertrain_df[stock_year_dim].between(timeframe[0],
                                                                                                          timeframe[1])]
            m = (timeframe[1] - timeframe[0])+1

            for country in countries:
                filtered_country_df = filtered_timeframe_df[filtered_timeframe_df[country_dim] == country]
                sum_squared_errors = filtered_country_df['squared_error'].sum()
                rmse = np.sqrt((1 / m) * sum_squared_errors)
                append_values(rows_rmse, country, timeframe, powertrain, 'real values', rmse)

    rmse_df = pd.DataFrame(rows_rmse)
    rmse_df.to_csv(f'{output_path}/{config[title_dim]}.csv', sep=',', index=False, decimal='.')
    return


