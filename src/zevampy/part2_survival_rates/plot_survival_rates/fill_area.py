"""Fill plot areas between two curves when requested."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT


def fill_area_based_on_label(ax, merged_df_country, x_column, columns_to_plot_keys, fill_between_label):
    """Fill the area between the first two plotted curves when enabled.

    Parameters:
        ax (matplotlib.axes.Axes):
            Axes containing the survival-rate plot.
        merged_df_country (pandas.DataFrame):
            Data plotted for one group.
        x_column (str):
            Column used for the x-axis.
        columns_to_plot_keys (list[str]):
            Ordered y-axis columns available for plotting.
        fill_between_label (bool):
            Whether area filling is enabled.

    Returns:
        matplotlib.axes.Axes:
            Updated axes object.
    """
    if not fill_between_label or len(columns_to_plot_keys) < 2:
        return ax
    return fill_area(ax, merged_df_country, x_column, columns_to_plot_keys)


def fill_area(ax, df, x_label, y_label):
    """Fill positive and negative differences between two curves.

    Parameters:
        ax (matplotlib.axes.Axes):
            Axes containing the curves.
        df (pandas.DataFrame):
            Data containing x values and the two y series.
        x_label (str):
            Column used for the x-axis.
        y_label (list[str]):
            Two columns defining the curves to compare.

    Returns:
        matplotlib.axes.Axes:
            Updated axes object.
    """
    ax.fill_between(
        df[x_label],
        df[y_label[0]],
        df[y_label[1]],
        where=(df[y_label[0]] > df[y_label[1]]),
        interpolate=True,
        color="red",
        alpha=0.25,
    )
    ax.fill_between(
        df[x_label],
        df[y_label[0]],
        df[y_label[1]],
        where=(df[y_label[0]] <= df[y_label[1]]),
        interpolate=True,
        color="green",
        alpha=0.25,
    )
    return ax

