"""Default input parameters for CSP and stock calculations."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part1_transportation_model.input_data import eu_countries_and_norway
from zevampy.load_data_and_prepare_inputs.dimension_names import eu_27_plus_norway_label

# Country groups used for standard aggregated stock-share outputs.
eu_country_groups = {
    eu_27_plus_norway_label: eu_countries_and_norway,
}

# Initial year on which new registrations are considered for stock calculations.
initial_registration_year = 1970
# Initial year on which the stock is modelled.
initial_simulation_stock_year = 2014
# Reference year associated with the default empirical CSP data.
csp_data_ref_year = 2021
# Number of vehicle ages represented by the CSP curve.
csp_available_years = 45
# Output filenames for stock values and stock shares.
save_options_stock = {
    "stock_data_filename": "3_1_stock_data_including_vehicle_age.csv",
    "stock_shares_filename": "3_2_stock_shares.csv",
}
save_fitted_csp_values = True