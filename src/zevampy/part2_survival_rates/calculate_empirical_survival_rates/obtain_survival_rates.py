"""Calculate empirical vehicle survival rates from stock data."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import numpy as np
from zevampy.load_data_and_prepare_inputs.dimension_names import age_dim, country_dim, new_registrations_dim, \
    survival_rate_dim, number_registered_vehicles_dim


def obtain_survival_rates(stock, registrations, survival_grouping):
    """
    Calculate empirical vehicle survival rates.

    This function estimates survival rates by dividing the number of registered vehicles in the stock dataset by the
    corresponding historical vehicle registrations.

    Parameters:
        stock (pandas.DataFrame):
            DataFrame containing vehicle stock data.

        registrations (pandas.DataFrame):
            DataFrame containing historical vehicle registrations.

        survival_grouping (list[str]):
            Column names defining the grouping used for survival-rate estimation.

    Returns:
        pandas.DataFrame:
            DataFrame containing empirical survival rates by survival group and vehicle age.
    """
    # Merge with selected columns and calculate survival rate

    merge_cols = survival_grouping + [age_dim]
    survival_rates = pd.merge(stock, registrations[merge_cols + [new_registrations_dim]],
                              on=merge_cols, how='left')
    # Divide stock of a certain vehicle age at a certain stock year by the new registrations at the vehicle age's year
    # to obtain the survival rate
    survival_rates[survival_rate_dim] = np.divide(survival_rates[number_registered_vehicles_dim],
                                                  survival_rates[new_registrations_dim],
                                                  out=np.zeros(len(survival_rates), dtype=float),
                                                  where=survival_rates[new_registrations_dim] != 0, )

    survival_rates = survival_rates[
        merge_cols + [survival_rate_dim]
        ]

    return survival_rates

