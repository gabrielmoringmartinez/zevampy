"""Calculate aggregated EU vehicle stock shares."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.part3_stock_calculation.calculate_eu_share.filter_calculate_and_add_eu_share import add_eu_stock_share
from zevampy.part1_transportation_model.input_data import eu_countries_and_norway
from zevampy.load_data_and_prepare_inputs.dimension_names import eu_27_plus_norway_label


def calculate_eu_share(stock_share, countries_selected):
    """Add an EU-27+Norway aggregate when the complete country set is present.

    Parameters:
        stock_share (pandas.DataFrame):
            Country-level stock shares and stock values.
        countries_selected (list[str]):
            Countries included in the current model run.

    Returns:
        pandas.DataFrame:
            Input stock-share table, with the EU-27+Norway aggregate appended when
            all required countries are available.
    """
    countries_selected = set(countries_selected)
    if set(eu_countries_and_norway).issubset(countries_selected):
        stock_share = add_eu_stock_share(stock_share, eu_27_plus_norway_label)
    return stock_share
