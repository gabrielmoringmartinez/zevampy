"""Plot empirical and fitted CSP curves for individual groups."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import matplotlib.pyplot as plt
from zevampy.part2_survival_rates.plot_survival_rates.customize_axes import customize_axes
from zevampy.load_data_and_prepare_inputs.dimension_names import *


def plot_survival_rate_country(ax, label, x, y, country_name, plot_params):
    """
    Plot survival-rate data for a single group.

    Parameters:
        ax (matplotlib.axes.Axes):
            Axis object used for plotting.

        label (str):
            Legend label for the plotted curve.

        x (list or numpy.ndarray):
            X-axis values, typically vehicle ages.

        y (list or numpy.ndarray):
            Y-axis values, typically survival probabilities.

        country_name (str):
            Name of the plotted group or country.

        plot_params (dict):
            Dictionary containing plot formatting settings.

    Returns:
        None
    """
    ax.plot(x, y, '-o', markersize=plot_params[marker_size_dim], linewidth=plot_params[line_width_dim], label=label)
    ax.set_title(country_name, fontsize=plot_params[title_fontsize_dim], y=plot_params[subfigure_height_dim])
    plt.style.use('seaborn-v0_8-white')
    ax = plt.gca()
    customize_axes(ax, plot_params)



