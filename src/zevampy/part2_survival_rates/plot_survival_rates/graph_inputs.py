"""Define plotting configurations for CSP visualizations."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import *


# Define your configuration dictionary
TITLE = "Empirical cumulative survival probability (CSP) curves for selected European countries"
X_COLUMN = "vehicle age"
X_LABEL = "Vehicle age"
Y_LABEL = "Cumulative Survival Probability (CSP)"
X_LIM = (0, 25)
Y_LIM = (0, None)
FIGURE_HEIGHT = 40
FIGURE_WEIGHT = 40
MARKER_SIZE = 6
LINE_WIDTH = 2
SPACE_BETWEEN_PLOTS = 0.4
NUMBER_OF_COUNTRIES_PER_PLOT = 16
FILE_EXTENSION = '.pdf'
TITLE_FONT = 64
TITLE_VERTICAL_POSITION = 0.93
SUBTITLE_VERTICAL_POSITION=1.025
AXIS_TITLE_FONT = 48
X_AXIS_TITLE_VERTICAL_POSITION = 0.075

file_info = {
    save_figure_dim: True,
    folder_dim: "outputs/figures/",
    main_title_dim: "empirical_cumulative_survival_probability_curves",
    additional_info_dim: 'all_countries',
    group_info_dim: '',  # Can update this dynamically if needed
    comparison_type_dim: '',  # Optional: e.g., 'comparison' for side-by-side analyses
    own_calculation_dim: True,  # Set True if calculations are from own model or study
    file_extension_dim: FILE_EXTENSION
}

base_plot_params = {
    tick_fontsize_dim: 28,
    title_fontsize_dim: 36,
    space_between_plots_dim: SPACE_BETWEEN_PLOTS,
    figure_height_dim: 40,
    figure_width_dim: 40,
    marker_size_dim: MARKER_SIZE,
    line_width_dim: LINE_WIDTH,
    show_grid_dim: True,
    title_dim: TITLE,
    x_column_dim: X_COLUMN,
    x_label_dim: X_LABEL,
    y_label_dim: Y_LABEL,
    x_lim_dim: X_LIM,
    y_lim_dim: Y_LIM,
    number_of_countries_group_dim: NUMBER_OF_COUNTRIES_PER_PLOT,
    title_font_dim: TITLE_FONT,
    title_vertical_position_dim: TITLE_VERTICAL_POSITION,
    subfigure_height_dim: SUBTITLE_VERTICAL_POSITION,
    axis_title_font_dim: AXIS_TITLE_FONT,
    x_axis_title_vertical_position_dim: X_AXIS_TITLE_VERTICAL_POSITION,
    y_axis_title_horizontal_position_dim: X_AXIS_TITLE_VERTICAL_POSITION,
    legend_show_dim: True,
    legend_loc_dim: "lower right",
    legend_bbox_to_anchor_dim: (0.95, 0.15),  # Adjust to place the legend outside the figure
    legend_fontsize_dim: 48,
    fill_between_dim: False,

}

# Configurations for "all countries" and "grouped countries"
config_all = {
    plot_params_dim: base_plot_params,
    file_info_dim: file_info,
}

config_group = {
    plot_params_dim: {
        **base_plot_params,
        tick_fontsize_dim: 40,
        title_fontsize_dim: 56,
        legend_bbox_to_anchor_dim: (0.347, 0.885),  # Adjust to place the legend outside the figure
        legend_fontsize_dim: 44,
    },
    file_info_dim: file_info,
}
