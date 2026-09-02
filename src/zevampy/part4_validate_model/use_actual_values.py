"""Replace modelled values with observed validation data."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import *


def use_actual_values(
        df_model,
        df_actual,
        keys=None,
        column_to_update=relative_sales_dim,
):
    """Replace modelled values with observed values for matching rows."""
    if keys is None:
        keys = [country_dim, time_dim, powertrain_dim]

    df_model = df_model.copy()
    df_actual = df_actual.copy()

    df_model.set_index(keys, inplace=True)
    df_model.sort_index(inplace=True)

    df_actual.set_index(keys, inplace=True)
    df_actual.sort_index(inplace=True)

    df_model.update(df_actual[[column_to_update]])
    df_model.reset_index(inplace=True)
    return df_model
