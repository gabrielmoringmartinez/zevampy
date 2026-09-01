"""Run the full ZEVAMPY modeling workflow."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

# Import required modules
from zevampy.load_data_and_prepare_inputs import load_data_and_prepare_inputs
from zevampy.load_data_and_prepare_inputs.ensure_clean_directory import ensure_clean_directory
from zevampy.part3_stock_calculation import calculate_and_plot_csps_and_stock
from zevampy.part4_validate_model import compare_model_and_actual_stock_results
from zevampy.part5_sensitivity_analysis import perform_sensitivity_analysis
from zevampy.config import load_config
from zevampy.load_data_and_prepare_inputs.dimension_names import *
import os
import logging

logger = logging.getLogger(__name__)


def run_model(config_path=None, input_path=None, output_path=None):
    """Run the full ZEVAMPY modeling workflow.

    Load the model configuration, prepare input data, calculate empirical
    survival rates and stock values, generate plots, optionally validate the
    results against historical data, and optionally run sensitivity analyses.

    Parameters:
        config_path (str, optional):
            Path to a YAML configuration file.
        input_path (str, optional):
            Optional input folder override.
        output_path (str, optional):
            Optional output folder override.

    Returns:
        None.
    """
    logger.info("Starting ZEVAMPY model run.")

    # Load config (or defaults)
    config = load_config(config_path)

    logger.debug(
        "Configuration loaded from %s.",
        config_path if config_path else "default configuration",
    )

    # Allow CLI override (optional)
    input_path = input_path or config["data"]["input_path"]
    output_path = output_path or config["data"]["output_path"]

    config["data"]["input_path"] = input_path
    config["data"]["output_path"] = output_path

    logger.info("Input directory: %s", input_path)
    logger.info("Output directory: %s", output_path)

    # Clean and recreate 'outputs' and 'outputs/figures'
    logger.debug("Preparing output directories.")
    ensure_clean_directory(output_path)
    ensure_clean_directory(os.path.join(output_path, 'figures'))

    # Step 1: Load data
    logger.info("Loading and validating input data.")
    data, inputs = load_data_and_prepare_inputs(input_path=input_path, config=config)

    # Step 2: Calculate and plot CSPs and stock
    logger.info("Calculating survival curves and vehicle stock.")
    csp_and_stock_calculated_data = calculate_and_plot_csps_and_stock(data, inputs)

    # Step 3: Compare model results with actual stock results
    if inputs[historical_validation_label] and inputs[survival_grouping_label] == [country_dim]:
        logger.info("Running historical model validation.")
        compare_model_and_actual_stock_results(data, csp_and_stock_calculated_data, inputs)
    elif inputs[historical_validation_label]:
        logger.info("Historical validation skipped because survival rates are not grouped only by country.")
    else:
        logger.debug("Historical validation is disabled.")

    # Step 4: Perform sensitivity analysis
    if inputs[sensitivity_analysis_label] and inputs[survival_grouping_label] == [country_dim]:
        logger.info("Running sensitivity analysis.")
        perform_sensitivity_analysis(data, csp_and_stock_calculated_data, inputs)
    elif inputs[sensitivity_analysis_label]:
        logger.info("Sensitivity analysis skipped because survival rates are not grouped only by country.")
    else:
        logger.debug("Sensitivity analysis is disabled.")

    logger.info("ZEVAMPY model run completed successfully.")


# Execute the main function when the script is run
if __name__ == "__main__":
    run_model(input_path="inputs", output_path="outputs")


