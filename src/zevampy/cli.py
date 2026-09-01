"""Provide the command-line interface for running and validating the ZEVAMPY model."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import argparse

from zevampy.config import load_config
from zevampy.load_data_and_prepare_inputs import load_data_and_prepare_inputs
from zevampy.run_model import run_model


def validate_inputs(config_path=None, input_path=None, output_path=None):
    """
    Validate ZEVAMPY input data and configuration without running the model.

    This function loads the model configuration and input datasets and executes
    the existing input and configuration validation checks. It does not clean
    output directories, calculate vehicle stock, generate figures, run
    historical validation, or perform sensitivity analysis.

    Parameters:
        config_path (str, optional):
            Path to a YAML configuration file.

        input_path (str, optional):
            Optional input folder override.

        output_path (str, optional):
            Optional output folder override. No outputs are generated during
            input validation, but the value is retained in the configuration.

    Returns:
        None
    """
    config = load_config(config_path)

    data_config = config.setdefault("data", {})

    input_path = input_path or data_config.get("input_path", "inputs")
    output_path = output_path or data_config.get("output_path", "outputs")

    data_config["input_path"] = input_path
    data_config["output_path"] = output_path

    load_data_and_prepare_inputs(
        input_path=input_path,
        config=config,
    )

    print("Input validation successful.")


def main():
    """
    Run the command-line interface for the ZEVAMPY model.

    This function parses optional command-line arguments that allow users to:
    - Provide a custom configuration YAML file.
    - Override the default input data directory.
    - Override the default output directory.
    - Validate inputs without running the full modeling workflow.


    Command-line arguments:
        --config : str, optional
            Path to a YAML configuration file containing model settings.

        --input : str, optional
            Path to the folder containing input datasets.

        --output : str, optional
            Path to the folder where model outputs will be saved.
        --validate-inputs : flag
            Validate input files and configuration, then exit without running
            the full model.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="ZEVAMPY: Zero-Emission Vehicle Adoption Model"
    )

    parser.add_argument(
        "--config",
        default=None,
        help="Path to config YAML file"
    )

    parser.add_argument(
        "--input",
        default=None,
        help="Override input data folder"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Override output folder"
    )

    parser.add_argument(
        "--validate-inputs",
        action="store_true",
        help="Validate input files and configuration without running the model",
    )

    args = parser.parse_args()

    if args.validate_inputs:
        validate_inputs(
            config_path=args.config,
            input_path=args.input,
            output_path=args.output,
        )
        return

    run_model(
        config_path=args.config,
        input_path=args.input,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()