# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from copy import deepcopy
from pathlib import Path
import math
import shutil

import pandas as pd
import pytest

from zevampy.load_data_and_prepare_inputs import load_data_and_prepare_inputs
from zevampy.load_data_and_prepare_inputs.ensure_clean_directory import ensure_clean_directory
from zevampy.load_data_and_prepare_inputs.dimension_names import initial_registration_year_label
from zevampy.part3_stock_calculation import calculate_and_plot_csps_and_stock


CORE_FILES = [
    "0_country_clusters.csv",
    "1_2_A_2_historical_new_registrations_data_passenger_cars.csv",
    "1_3_new_registrations_projected.csv",
]


def _create_powertrain_stock_inputs(tmp_path, country_only_stock_year=False):
    """Create a two-powertrain stock-by-age example with known survival curves."""
    source_dir = Path("tests/test_inputs_single_country")
    input_dir = tmp_path / "powertrain_inputs"
    input_dir.mkdir()

    for filename in CORE_FILES:
        shutil.copy(source_dir / filename, input_dir / filename)

    historical = pd.read_csv(
        source_dir / "1_2_A_2_historical_new_registrations_data_passenger_cars.csv",
        sep=";",
        decimal=",",
    )

    # Use positive shares for both powertrains throughout the cohort history so
    # that both empirical survival curves can be estimated for every age.
    registration_share_rows = []
    for year in range(1970, 2051):
        for powertrain, share in [("BEV", 0.4), ("Gasoline", 0.6)]:
            registration_share_rows.append(
                {
                    "time": year,
                    "geo country": "Example Country",
                    "cluster": 1,
                    "powertrain": powertrain,
                    "relative sales": share,
                }
            )
    pd.DataFrame(registration_share_rows).to_csv(
        input_dir / "1_1_new_registrations_by_fuel_type_clusters.csv",
        sep=";",
        decimal=",",
        index=False,
    )

    if country_only_stock_year:
        stock_year_rows = [
            {
                "geo country": "Example Country",
                "stock year of empirical csp data": 2009,
            }
        ]
        reference_years = {"Total": 2009, "BEV": 2009, "Gasoline": 2009}
    else:
        # Deliberately use different stock snapshots by powertrain. The older
        # Gasoline reference year also tests registration-history derivation.
        stock_year_rows = [
            {
                "geo country": "Example Country",
                "powertrain": "Total",
                "stock year of empirical csp data": 2009,
            },
            {
                "geo country": "Example Country",
                "powertrain": "BEV",
                "stock year of empirical csp data": 2009,
            },
            {
                "geo country": "Example Country",
                "powertrain": "Gasoline",
                "stock year of empirical csp data": 1989,
            },
        ]
        reference_years = {"Total": 2009, "BEV": 2009, "Gasoline": 1989}

    pd.DataFrame(stock_year_rows).to_csv(
        input_dir / "2_2_A_1_stock_year.csv",
        sep=";",
        decimal=",",
        index=False,
    )

    registrations_by_year = dict(
        zip(historical["time"], historical["new vehicle registrations"])
    )
    shares = {"Total": 1.0, "BEV": 0.4, "Gasoline": 0.6}
    gammas = {"Total": 20.0, "BEV": 8.0, "Gasoline": 18.0}

    stock_rows = []
    for powertrain in ["Total", "BEV", "Gasoline"]:
        reference_year = reference_years[powertrain]
        for age in range(1, 21):
            registration_year = reference_year - age + 1
            registrations = registrations_by_year[registration_year] * shares[powertrain]
            survival_rate = math.exp(-((age / gammas[powertrain]) ** 3))
            stock_rows.append(
                {
                    "geo country": "Example Country",
                    "powertrain": powertrain,
                    "vehicle age": age,
                    "number of registered vehicles": registrations * survival_rate,
                }
            )

    pd.DataFrame(stock_rows).to_csv(
        input_dir / "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv",
        sep=";",
        decimal=",",
        index=False,
    )

    return input_dir


def _base_config(input_dir, output_dir):
    return {
        "data": {
            "input_path": str(input_dir),
            "output_path": str(output_dir),
        },
        "geography": {
            "countries": ["Example Country"],
            "use_clusters": True,
        },
        "powertrains": ["BEV", "Gasoline"],
        "model": {
            "first_stock_year": 2014,
            "end_year": 2030,
            "historical_validation": False,
        },
        "survival_rates": {
            "source": "stock_by_age",
            "grouping": ["geo country", "powertrain"],
            "csp_available_years": 20,
            "files": {
                "stock_by_age": "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv",
                "stock_year": "2_2_A_1_stock_year.csv",
            },
        },
    }


def _run(config):
    output_dir = Path(config["data"]["output_path"])
    ensure_clean_directory(output_dir)
    ensure_clean_directory(output_dir / "figures")
    data, inputs = load_data_and_prepare_inputs(
        config["data"]["input_path"],
        config=config,
    )
    result = calculate_and_plot_csps_and_stock(data, inputs)
    return data, inputs, result


def test_stock_by_age_supports_powertrain_specific_reference_years(tmp_path):
    """Stock-by-age CSPs should be estimated separately for each powertrain."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    config = _base_config(input_dir, tmp_path / "stock_by_age_outputs")

    _, inputs, result = _run(config)

    # Gasoline uses a 1989 stock snapshot. With a 20-year CSP horizon the
    # model therefore needs registrations back to 1970.
    assert inputs[initial_registration_year_label] == 1970

    empirical = result["empirical_survival_rates"]
    assert set(empirical["powertrain"]) == {"Total", "BEV", "Gasoline"}
    assert len(empirical) == 60

    age_10 = empirical[empirical["vehicle age"] == 10].set_index("powertrain")
    assert age_10.loc["BEV", "survival rate"] == pytest.approx(
        math.exp(-((10 / 8.0) ** 3)), rel=1e-10
    )
    assert age_10.loc["Gasoline", "survival rate"] == pytest.approx(
        math.exp(-((10 / 18.0) ** 3)), rel=1e-10
    )

    parameters = result["optimum_parameters_wg"]
    assert set(parameters["powertrain"]) == {"Total", "BEV", "Gasoline"}
    assert len(parameters) == 3

    stock = result["stock_values"]
    assert set(stock["powertrain"]) == {"Total", "BEV", "Gasoline"}


def test_country_stock_year_can_be_shared_across_powertrains(tmp_path):
    """A country-only stock year should broadcast to all powertrain CSP groups."""
    input_dir = _create_powertrain_stock_inputs(tmp_path, country_only_stock_year=True)
    config = _base_config(input_dir, tmp_path / "country_year_outputs")

    _, _, result = _run(config)
    empirical = result["empirical_survival_rates"]

    assert set(empirical["powertrain"]) == {"Total", "BEV", "Gasoline"}
    assert len(empirical) == 60


def test_empirical_and_parameter_sources_preserve_powertrain_grouping(tmp_path):
    """Outputs from a powertrain-specific run should be reusable by both alternative sources."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    baseline_config = _base_config(input_dir, tmp_path / "baseline")
    _, _, baseline = _run(baseline_config)

    empirical_config = deepcopy(baseline_config)
    empirical_config["data"]["output_path"] = str(tmp_path / "empirical")
    empirical_config["survival_rates"] = {
        "source": "empirical",
        "grouping": ["geo country", "powertrain"],
        "csp_available_years": 20,
        "files": {
            "empirical": str(
                (tmp_path / "baseline" / "2_2_empirical_survival_rates.csv").resolve()
            )
        },
    }
    _, _, empirical = _run(empirical_config)

    parameter_config = deepcopy(baseline_config)
    parameter_config["data"]["output_path"] = str(tmp_path / "parameters")
    parameter_config["survival_rates"] = {
        "source": "parameters",
        "grouping": ["geo country", "powertrain"],
        "csp_available_years": 20,
        "files": {
            "parameters": str(
                (tmp_path / "baseline" / "2_1_optimum_parameters_csp_curves.csv").resolve()
            )
        },
    }
    _, _, parameters = _run(parameter_config)

    assert set(empirical["stock_values"]["powertrain"]) == {"Total", "BEV", "Gasoline"}
    assert set(parameters["stock_values"]["powertrain"]) == {"Total", "BEV", "Gasoline"}

    baseline_stock = baseline["stock_values"]["stock"].sum()
    parameter_stock = parameters["stock_values"]["stock"].sum()
    assert parameter_stock == pytest.approx(baseline_stock, rel=1e-12, abs=1e-9)


def test_missing_powertrain_survival_group_raises_error(tmp_path):
    """Every modelled country/powertrain combination must have survival assumptions."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    parameter_file = tmp_path / "missing_powertrain_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country", "Example Country"],
            "powertrain": ["Total", "BEV"],
            "gamma (Weibull)": [20.0, 8.0],
            "beta (Weibull)": [3.0, 3.0],
            "distribution": ["Weibull", "Weibull"],
        }
    ).to_csv(parameter_file, index=False)

    config = _base_config(input_dir, tmp_path / "missing_group_outputs")
    config["survival_rates"] = {
        "source": "parameters",
        "grouping": ["geo country", "powertrain"],
        "csp_available_years": 20,
        "files": {"parameters": str(parameter_file.resolve())},
    }

    with pytest.raises(ValueError, match="Missing survival assumptions") as error:
        _run(config)

    assert "Gasoline" in str(error.value)


def test_missing_total_survival_group_raises_error(tmp_path):
    """Powertrain-specific survival data must also contain the complete Total fleet."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    parameter_file = tmp_path / "missing_total_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country", "Example Country"],
            "powertrain": ["BEV", "Gasoline"],
            "gamma (Weibull)": [8.0, 18.0],
            "beta (Weibull)": [3.0, 3.0],
            "distribution": ["Weibull", "Weibull"],
        }
    ).to_csv(parameter_file, index=False)

    config = _base_config(input_dir, tmp_path / "missing_total_outputs")
    config["survival_rates"] = {
        "source": "parameters",
        "grouping": ["geo country", "powertrain"],
        "csp_available_years": 20,
        "files": {"parameters": str(parameter_file.resolve())},
    }

    with pytest.raises(ValueError, match="Missing survival assumptions") as error:
        _run(config)

    assert "Total" in str(error.value)


def test_missing_powertrain_stock_year_raises_error(tmp_path):
    """Group-specific stock years must cover every stock-by-age survival group."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    stock_year_file = input_dir / "2_2_A_1_stock_year.csv"
    stock_year = pd.read_csv(stock_year_file, sep=";", decimal=",")
    stock_year = stock_year[stock_year["powertrain"].isin(["Total", "BEV"])]
    stock_year.to_csv(stock_year_file, sep=";", decimal=",", index=False)

    config = _base_config(input_dir, tmp_path / "missing_year_outputs")

    with pytest.raises(ValueError, match="missing reference years") as error:
        load_data_and_prepare_inputs(str(input_dir), config=config)

    assert "Gasoline" in str(error.value)


def test_historical_validation_runs_with_powertrain_specific_parameters(tmp_path):
    """Historical validation should also use the configured powertrain-specific CSPs."""
    import yaml
    from zevampy.run_model import run_model

    parameter_file = tmp_path / "validation_powertrain_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country", "Example Country", "Example Country"],
            "powertrain": ["Total", "BEV", "Gasoline"],
            "gamma (Weibull)": [20.0, 8.0, 18.0],
            "beta (Weibull)": [3.0, 3.0, 3.0],
            "distribution": ["Weibull", "Weibull", "Weibull"],
        }
    ).to_csv(parameter_file, index=False)

    output_dir = tmp_path / "validation_outputs"
    config = {
        "data": {
            "input_path": "tests/test_inputs_single_country",
            "output_path": str(output_dir),
        },
        "geography": {
            "countries": ["Example Country"],
            "use_clusters": True,
        },
        "powertrains": ["BEV", "Gasoline"],
        "model": {
            "first_stock_year": 2014,
            "end_year": 2030,
            "historical_validation": True,
            "validation_powertrain": "BEV",
        },
        "survival_rates": {
            "source": "parameters",
            "grouping": ["geo country", "powertrain"],
            "csp_available_years": 45,
            "files": {"parameters": str(parameter_file.resolve())},
        },
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w", encoding="utf-8") as stream:
        yaml.safe_dump(config, stream, sort_keys=False)

    run_model(config_path=str(config_path))

    assert (output_dir / "4_1_rmse_validation_step_1_bev_all_countries.csv").is_file()
    assert (output_dir / "4_2_rmse_validation_step_2_bev_all_countries.csv").is_file()



def test_stock_by_age_rejects_gapped_vehicle_ages(tmp_path):
    """Stock-by-age fitting should reject missing ages within a survival group."""
    input_dir = _create_powertrain_stock_inputs(tmp_path)
    stock_path = input_dir / "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv"
    stock = pd.read_csv(stock_path, sep=";", decimal=",")
    stock = stock[
        ~((stock["powertrain"] == "BEV") & (stock["vehicle age"] == 4))
    ]
    stock.to_csv(stock_path, sep=";", decimal=",", index=False)

    config = _base_config(input_dir, tmp_path / "gapped_age_outputs")

    with pytest.raises(ValueError, match="consecutive integer vehicle age starting at 1"):
        load_data_and_prepare_inputs(
            config["data"]["input_path"],
            config=config,
        )


