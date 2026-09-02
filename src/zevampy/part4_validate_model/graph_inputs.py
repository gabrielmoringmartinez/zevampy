"""Default plotting configuration for stock-share validation figures."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import *

# Define your configuration dictionary
TITLE = "Actual BEV stock shares compared to estimated BEV shares using 2021 CSP curves and actual new BEV registrations"
X_COLUMN = stock_year_dim
X_LABEL = "year"
Y_LABEL = "Battery Electric Vehicle (BEV) stock share (in %)"
X_LIM = (2014, 2023)
X_TICKS_VALUES = [2015, 2017, 2019, 2021, 2023]
Y_LIM = (0, None)
DECIMALS = 2
NUM_COLUMNS = 5
NUM_ROWS = 7
FIGURE_HEIGHT = 40
FIGURE_WEIGHT = 40
MARKER_SIZE = 6
LINE_WIDTH = 2
SPACE_BETWEEN_PLOTS = 0.4
FILE_EXTENSION = '.pdf'
TITLE_FONT = 40
TITLE_VERTICAL_POSITION = 0.91
AXIS_TITLE_FONT = 40
X_AXIS_TITLE_VERTICAL_POSITION = 0.19
Y_AXIS_TITLE_HORIZONTAL_POSITION = 0.07
SHARE = True
validation_powertrain_default = "BEV"

file_info = {
    save_figure_dim: True,
    folder_dim: "outputs/figures/",
    main_title_dim: "validation_step_1_actual_new_bev_registrations_and_empirical_csp_curves",
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
    number_of_decimals_dim: DECIMALS,
    x_ticks_dim: X_TICKS_VALUES,
    num_rows_dim: NUM_ROWS,
    num_columns_dim: NUM_COLUMNS,
    share_dim: True,
    title_font_dim: TITLE_FONT,
    title_vertical_position_dim: TITLE_VERTICAL_POSITION,
    axis_title_font_dim: AXIS_TITLE_FONT,
    x_axis_title_vertical_position_dim: X_AXIS_TITLE_VERTICAL_POSITION,
    y_axis_title_horizontal_position_dim: Y_AXIS_TITLE_HORIZONTAL_POSITION,
    # Legend parameters
    legend_show_dim: True,
    legend_loc_dim: "lower right",
    legend_bbox_to_anchor_dim: (0.91, 0.235),  # Adjust to place the legend outside the figure
    legend_fontsize_dim: 40,
    fill_between_dim: False,

}

# Configurations for "all countries" and "grouped countries"
config_validation_step1 = {
    plot_params_dim: base_plot_params,
    file_info_dim: file_info,
}

config_validation_step2 = {
    file_info_dim: {
        **file_info,
        main_title_dim: "validation_step_2_actual_new_bev_registrations_and_empirical_csp_curves",
    },
    plot_params_dim: {
        **base_plot_params,
        title_dim: "Actual BEV stock shares compared to estimated BEV shares using 2021 CSP curves and estimated new BEV registrations (Möring, 2024)",
    },
}
