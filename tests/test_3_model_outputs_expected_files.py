# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.run_model import run_model


def test_model_outputs_expected_files(tmp_path):
    """
    Test that the main ZEVAMPY model runs successfully and produces all expected output files.

    This test:
    - Runs the model using a temporary output directory.
    - Checks that the output directory is created.
    - Verifies that all expected CSV files are generated.
    - Verifies that all expected PDF figures are generated.

    Args:
        tmp_path (Path):
            Temporary directory provided by pytest for isolated test outputs.

    Raises:
        AssertionError:
            If the output directory, figures directory, or any expected
            CSV or PDF output file is missing.
    """
    # Clean up any old outputs
    output_dir = tmp_path / "outputs"

    run_model(
        config_path="config.yaml",
        output_path=str(output_dir),
    )

    expected_csv_files = [
        "1_1_absolute_registrations.csv",
        "1_2_registrations_by_powertrain.csv",
        "2_1_optimum_parameters_csp_curves.csv",
        "2_2_empirical_survival_rates.csv",
        "2_3_fitted_CSP_curves.csv",
        "3_1_stock_data_including_vehicle_age.csv",
        "3_2_stock_shares.csv",
    ]

    assert output_dir.exists(), "Output folder was not created"
    actual_csv_files = {
        path.name
        for path in output_dir.glob("*.csv")
    }

    missing_csv = [
        filename
        for filename in expected_csv_files
        if filename not in actual_csv_files
    ]

    assert not missing_csv, (
        f"Missing expected CSV output files: {missing_csv}"
    )

    expected_pdf_files = [
        "stock_shares_model_reference_scenario_BEV.pdf",
        "stock_shares_model_reference_scenario_Gasoline.pdf",
    ]

    figures_dir = output_dir / "figures"

    assert figures_dir.exists(), (
        "Output figures folder was not created"
    )

    actual_pdf_files = {
        path.name
        for path in figures_dir.glob("*.pdf")
    }

    missing_pdfs = [
        filename
        for filename in expected_pdf_files
        if filename not in actual_pdf_files
    ]

    assert not missing_pdfs, (
        f"Missing expected PDF output files: {missing_pdfs}"
    )