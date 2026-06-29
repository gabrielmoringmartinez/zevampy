"""Calculate empirical vehicle survival rates from stock data."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import numpy as np
from zevampy.load_data_and_prepare_inputs.dimension_names import age_dim, country_dim, new_registrations_dim, \
    survival_rate_dim, number_registered_vehicles_dim, stock_year_dim, time_dim


def obtain_survival_rates(stock, registrations, survival_grouping):
    """
    Calculate empirical vehicle survival rates for all available stock years.
    """
    stock = stock.copy()
    registrations = registrations.copy()

    stock["_registration_year"] = stock[stock_year_dim] - stock[age_dim]

    registrations = registrations.rename(
        columns={time_dim: "_registration_year"}
    )

    join_cols = survival_grouping + ["_registration_year"]
    output_cols = survival_grouping + [age_dim]
    registrations.to_csv(f'outputs/TEST_registration_1.csv', sep=';', index=False, decimal=',')

    registrations = (
        registrations
        .groupby(join_cols, as_index=False)[new_registrations_dim]
        .sum()
    )

    survival_rates = pd.merge(
        stock,
        registrations,
        on=join_cols,
        how="left",
        validate="many_to_one",
    )

    survival_rates[survival_rate_dim] = np.divide(
        survival_rates[number_registered_vehicles_dim],
        survival_rates[new_registrations_dim],
        out=np.zeros(len(survival_rates), dtype=float),
        where=survival_rates[new_registrations_dim] != 0,
    )

    return survival_rates[output_cols + [survival_rate_dim]]
