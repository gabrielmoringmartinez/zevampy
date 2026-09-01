"""Default input parameters for CSP and stock calculations."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part1_transportation_model.input_data import eu_countries_and_norway
from zevampy.load_data_and_prepare_inputs.dimension_names import eu_9_label, eu_26_plus_norway_label, \
    eu_27_plus_norway_label

# Other geographical EU groups for comparing with 2008, and 2016, where less empirical country data is available
eu_9 = ['Austria', 'Denmark', 'Finland', 'France', 'Germany', 'Ireland', 'Italy', 'Netherlands', 'Spain']
eu_26_and_norway = eu_countries_and_norway.copy()
eu_26_and_norway.remove('Bulgaria')

eu_country_groups = {
    eu_9_label: eu_9,
    eu_26_plus_norway_label: eu_26_and_norway,
    eu_27_plus_norway_label: eu_countries_and_norway # Assuming this is the full set
}
# Initial year on which the new registrations are considered to calculate CSP rates
initial_registration_year = 1970
# Initial year on which the stock is modelled
initial_simulation_stock_year = 2014
# Year when the empirical CSP data is used
csp_data_ref_year = 2021
# Number of years which are considered. The vehicle age reaches a maximum of f.example, 45 years
csp_available_years = 45
# If older historical data is not available, we set it to No. 2021 is considered actual data, non-historical
historical_csp = "False"
# The paths for saving the stock values
save_options_stock = {
    "stock_data_filename": "3_1_stock_data_including_vehicle_age.csv",
    "stock_shares_filename": "3_2_stock_shares.csv"
}
save_fitted_csp_values = True
