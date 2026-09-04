# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import pytest

from zevampy.load_data_and_prepare_inputs.load_data import validate_registration_shares
from zevampy.part1_transportation_model.calculate_registrations import _append_total_registrations
from zevampy.part3_stock_calculation.calculate_stock.compute_stock_shares import compute_stock_shares


def test_stock_shares_use_total_fleet_not_sum_of_selected_powertrains():
    stock = pd.DataFrame(
        {
            "geo country": ["Example Country"] * 3,
            "stock year": [2030] * 3,
            "powertrain": ["Total", "BEV", "Gasoline"],
            "stock": [10_000_000, 2_000_000, 6_000_000],
        }
    )

    result = compute_stock_shares(stock).set_index("powertrain")

    assert result.loc["Total", "share"] == pytest.approx(1.0)
    assert result.loc["BEV", "share"] == pytest.approx(0.20)
    assert result.loc["Gasoline", "share"] == pytest.approx(0.60)

    # The selected technologies cover only 80% of the total fleet. The BEV
    # share must therefore not be calculated as BEV / (BEV + Gasoline) = 25%.
    assert result.loc["BEV", "share"] != pytest.approx(0.25)


def test_registration_shares_may_cover_only_part_of_the_market():
    shares = pd.DataFrame(
        {
            "time": [2030, 2030],
            "geo country": ["Example Country", "Example Country"],
            "powertrain": ["BEV", "Gasoline"],
            "relative sales": [0.05, 0.90],
        }
    )

    # 95% explicit market coverage is valid. The remaining 5% does not need
    # to be represented by a synthetic Rest-of-powertrains category.
    validate_registration_shares(shares, "test registration shares")


def test_registration_shares_cannot_exceed_the_total_market():
    shares = pd.DataFrame(
        {
            "time": [2030, 2030],
            "geo country": ["Example Country", "Example Country"],
            "powertrain": ["BEV", "Gasoline"],
            "relative sales": [0.20, 0.90],
        }
    )

    with pytest.raises(ValueError, match="exceed 1"):
        validate_registration_shares(shares, "test registration shares")


def test_total_registrations_are_generated_independently():
    registrations = pd.DataFrame(
        {
            "geo country": ["Example Country", "Example Country"],
            "time": [2030, 2030],
            "powertrain": ["BEV", "Gasoline"],
            "new vehicle registrations": [1_000_000, 1_000_000],
            "relative sales": [0.05, 0.90],
            "registrations by powertrain": [50_000, 900_000],
        }
    )

    result = _append_total_registrations(registrations)
    total = result[result["powertrain"] == "Total"].iloc[0]

    assert total["relative sales"] == pytest.approx(1.0)
    assert total["registrations by powertrain"] == pytest.approx(1_000_000)
