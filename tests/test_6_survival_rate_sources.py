# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from copy import deepcopy
from pathlib import Path
import shutil

import pandas as pd
import pytest

from zevampy.load_data_and_prepare_inputs import load_data_and_prepare_inputs
from zevampy.load_data_and_prepare_inputs.ensure_clean_directory import ensure_clean_directory
from zevampy.part3_stock_calculation import calculate_and_plot_csps_and_stock


BASE_CONFIG = {
    "data": {"output_path": "outputs"},
    "geography": {
        "countries": ["Example Country"],
        "use_clusters": True,
    },
    "powertrains": ["BEV", "Gasoline"],
    "model": {
        "start_new_registration_year": 1970,
        "first_stock_year": 2014,
        "end_year": 2050,
        "csp_reference_year": 2021,
        "csp_available_years": 45,
        "historical_validation": False,
    },
    "survival_rates": {
        "grouping": ["geo country"],
        "source": "stock_by_age",
    },
}

INPUT_DIR = "tests/test_inputs_single_country"


def _run(config, output_dir, input_dir=INPUT_DIR):
    """Run the stock model with an isolated temporary output directory."""
    config = deepcopy(config)
    config["data"]["output_path"] = str(output_dir)

    ensure_clean_directory(output_dir)
    ensure_clean_directory(output_dir / "figures")

    data, inputs = load_data_and_prepare_inputs(input_dir, config=config)
    return calculate_and_plot_csps_and_stock(data, inputs)


def test_all_three_survival_sources_run_and_previous_outputs_can_be_reused(tmp_path):
    """Test stock_by_age, empirical, and parameters survival-source workflows."""
    baseline_dir = tmp_path / "baseline"
    baseline = _run(BASE_CONFIG, baseline_dir)

    assert not baseline["stock_values"].empty
    assert not baseline["empirical_survival_rates"].empty

    empirical_config = deepcopy(BASE_CONFIG)
    empirical_config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "empirical",
        "file": str((baseline_dir / "2_2_empirical_survival_rates.csv").resolve()),
    }
    empirical = _run(empirical_config, tmp_path / "empirical")

    assert not empirical["stock_values"].empty
    assert not empirical["empirical_survival_rates"].empty

    parameter_config = deepcopy(BASE_CONFIG)
    parameter_config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "parameters",
        "file": str((baseline_dir / "2_1_optimum_parameters_csp_curves.csv").resolve()),
    }
    parameters = _run(parameter_config, tmp_path / "parameters")

    assert not parameters["stock_values"].empty
    assert parameters["empirical_survival_rates"] is None

    # Reusing the fitted parameters from the baseline run should reproduce
    # the same stock calculation, apart from negligible floating-point noise.
    baseline_stock = baseline["stock_values"]["stock"].sum()
    parameter_stock = parameters["stock_values"]["stock"].sum()
    assert parameter_stock == pytest.approx(baseline_stock, rel=1e-12, abs=1e-9)


def test_parameters_source_accepts_weibull_only_parameters(tmp_path):
    """Weibull parameter input should require only gamma, beta, and distribution."""
    parameter_file = tmp_path / "weibull_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country"],
            "gamma (Weibull)": [15.0],
            "beta (Weibull)": [3.0],
            "distribution": ["Weibull"],
        }
    ).to_csv(parameter_file, index=False)

    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "parameters",
        "file": str(parameter_file.resolve()),
    }

    result = _run(config, tmp_path / "weibull_only")

    assert not result["stock_values"].empty
    assert result["stock_values"]["stock"].notna().all()


def test_parameters_source_does_not_require_stock_by_age_or_stock_year(tmp_path):
    """Direct CSP parameters should bypass stock-by-age survival-rate derivation."""
    source_input_dir = Path(INPUT_DIR)
    alternative_input_dir = tmp_path / "inputs_without_stock_by_age"
    alternative_input_dir.mkdir()

    for filename in [
        "0_country_clusters.csv",
        "1_1_new_registrations_by_fuel_type_clusters.csv",
        "1_2_A_2_historical_new_registrations_data_passenger_cars.csv",
        "1_3_new_registrations_projected.csv",
    ]:
        shutil.copy(source_input_dir / filename, alternative_input_dir / filename)

    parameter_file = alternative_input_dir / "alternative_csp_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country"],
            "gamma (Weibull)": [15.0],
            "beta (Weibull)": [3.0],
            "distribution": ["Weibull"],
        }
    ).to_csv(parameter_file, index=False)

    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "parameters",
        "file": "alternative_csp_parameters.csv",
    }

    output_dir = tmp_path / "no_stock_input_outputs"
    config["data"]["output_path"] = str(output_dir)
    ensure_clean_directory(output_dir)
    ensure_clean_directory(output_dir / "figures")

    data, inputs = load_data_and_prepare_inputs(str(alternative_input_dir), config=config)
    result = calculate_and_plot_csps_and_stock(data, inputs)

    assert "stock_by_age" not in data
    assert "stock_year" not in data
    assert not result["stock_values"].empty


def test_invalid_survival_source_raises_clear_error(tmp_path):
    """Unknown survival source names should fail before the model calculation."""
    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "unknown_source",
    }
    config["data"]["output_path"] = str(tmp_path / "outputs")

    with pytest.raises(ValueError, match="Invalid survival_rates.source"):
        load_data_and_prepare_inputs(INPUT_DIR, config=config)


def test_alternative_survival_source_requires_file(tmp_path):
    """Alternative empirical/parameter sources must specify an input file."""
    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "empirical",
    }
    config["data"]["output_path"] = str(tmp_path / "outputs")

    with pytest.raises(ValueError, match="survival_rates.file must be provided"):
        load_data_and_prepare_inputs(INPUT_DIR, config=config)


def test_missing_alternative_survival_file_raises_clear_error(tmp_path):
    """A configured alternative survival file must exist."""
    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "parameters",
        "file": "file_that_does_not_exist.csv",
    }
    config["data"]["output_path"] = str(tmp_path / "outputs")

    with pytest.raises(FileNotFoundError, match="Alternative survival input file"):
        load_data_and_prepare_inputs(INPUT_DIR, config=config)


def test_wg_parameters_require_gaussian_parameters(tmp_path):
    """WG rows must include k, mu, and sigma in addition to Weibull parameters."""
    parameter_file = tmp_path / "incomplete_wg_parameters.csv"
    pd.DataFrame(
        {
            "geo country": ["Example Country"],
            "gamma (Weibull)": [15.0],
            "beta (Weibull)": [3.0],
            "distribution": ["WG"],
        }
    ).to_csv(parameter_file, index=False)

    config = deepcopy(BASE_CONFIG)
    config["survival_rates"] = {
        "grouping": ["geo country"],
        "source": "parameters",
        "file": str(parameter_file.resolve()),
    }
    config["data"]["output_path"] = str(tmp_path / "outputs")

    with pytest.raises(ValueError, match="WG parameter rows require"):
        load_data_and_prepare_inputs(INPUT_DIR, config=config)
