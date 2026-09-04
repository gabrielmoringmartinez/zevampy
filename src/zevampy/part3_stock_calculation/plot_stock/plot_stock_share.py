"""Plot vehicle stock-share results for different powertrains."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part2_survival_rates.plot_survival_rates.plot_all_countries import plot_all_countries
from zevampy.load_data_and_prepare_inputs.dimension_names import *


def plot_stock_shares(stock_shares, config_scenario, powertrains):
    """
    Generate stock-share plots for each powertrain.

    This function filters stock-share data by powertrain and generates country-level stock-share plots using the
    provided plotting configuration.

    Parameters:
        stock_shares (pandas.DataFrame):
            DataFrame containing calculated stock shares.

        config_scenario (dict):
            Plot configuration dictionary.

        powertrains (list[str]):
            Powertrain categories included in the analysis.

    Returns:
        None
    """
    columns_to_plot = {share_dim: share_dim.capitalize()}

    for pt in stock_shares[powertrain_dim].unique():

        # Total is retained in the tabular stock-share output as the
        # denominator (share = 1), but plotting a flat 100% Total-share curve
        # is not informative.
        if pt == total_powertrain_label:
            continue

        stock_subset = stock_shares[
            stock_shares[powertrain_dim] == pt
            ]

        if stock_subset.empty:
            continue

        # Optional: add label for filename
        config_local = config_scenario.copy()
        config_local[file_info_dim] = config_local[file_info_dim].copy()
        config_local[plot_params_dim] = config_scenario[plot_params_dim].copy()
        # Update title dynamically
        pt_title = pt.replace("_", " ")
        existing_title = config_local[plot_params_dim][title_dim]
        config_local[plot_params_dim][title_dim] = f"{pt_title} {existing_title}"
        existing_ylabel =  config_local[plot_params_dim][y_label_dim]
        config_local[plot_params_dim][y_label_dim] = f"{pt_title} {existing_ylabel}"
        pt_file = pt.replace(" ", "_")
        existing_info = config_local[file_info_dim].get(additional_info_dim, "").rstrip("_")
        config_local[file_info_dim][additional_info_dim] = (f"{existing_info}{pt_file}")
        plot_all_countries(
            stock_subset,
            config_local,
            columns_to_plot,
            None
        )

