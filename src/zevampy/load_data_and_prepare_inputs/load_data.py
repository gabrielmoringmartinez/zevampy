"""Load and validate input datasets used by the ZEVAMPY model."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import warnings
from pathlib import Path

from zevampy.load_data_and_prepare_inputs.dimension_names import *

DEFAULT_INPUT_FILES = {
    "country_clusters": "0_country_clusters.csv",
    "registration_shares": "1_1_new_registrations_by_fuel_type_clusters.csv",
    "historical_registrations": "1_2_A_2_historical_new_registrations_data_passenger_cars.csv",
    "projected_registrations": "1_3_new_registrations_projected.csv",
    "stock_by_age": "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv",
    "stock_year": "2_2_A_1_stock_year.csv",
    "validation_registration_shares": "4_1_eafo_ev_new_registration_shares.csv",
    "validation_stock_shares": "4_2_eafo_ev_stock_shares.csv",
    "historical_csp_parameters": "5_1_oguchi_2008_survival_rate_parameters.csv",
    "historical_survival_rates": "5_2_held_2016_survival_rates.csv",
}


def load_data(input_dir, historical_validation_active=True, sensitivity_analysis_active=True,
              historical_csp_active=True, use_clusters_active=True, powertrains=None, survival_grouping=None,
              input_files=None):
    """
    Load datasets required for modeling vehicle stock shares and performing CSP-based simulations.

    This function reads input CSV files containing:
    - Historical and projected vehicle registrations.
    - Vehicle stock-by-age data.
    - Country cluster information.
    - Validation datasets.
    - Historical CSP sensitivity datasets.

    The function also validates:
    - Required file availability.
    - Powertrain consistency.
    - Survival-rate grouping compatibility.
    - Required stock-by-age dimensions.

    Parameters:
        input_dir (str):
            Path to the directory containing input CSV files.

        historical_validation_active (bool, optional):
            Whether validation datasets should be loaded.

        sensitivity_analysis_active (bool, optional):
            Whether sensitivity-analysis datasets should be loaded.

        historical_csp_active (bool, optional):
            Whether historical CSP datasets should be loaded.

        use_clusters_active (bool, optional):
            Whether country clustering should be used.

        powertrains (list[str] | None, optional):
            Selected powertrain categories to include.

        survival_grouping (list[str] | None, optional):
            Dimensions used for survival-rate estimation.

        input_files (dict[str, str] | None, optional):
            Mapping of logical input dataset names to CSV filenames.
            Unspecified filenames fall back to the default ZEVAMPY filenames.

    Returns:
        tuple:
            - dict:
                Dictionary containing loaded datasets as pandas DataFrames.
            - int:
                Maximum year found in the projected registrations dataset.
    """
    input_dir = Path(input_dir)

    input_files = {
        **DEFAULT_INPUT_FILES,
        **(input_files or {}),
    }
    # --- Check folder exists ---
    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input directory '{input_dir}' does not exist.\n\n"
            "Possible causes:\n"
            "- The configured input path is incorrect.\n"
            "- The input folder has not been created yet.\n\n"
            "How to fix:\n"
            "1) Create the input folder and add the required CSV files.\n"
            "2) Or update 'data.input_path' in config.yaml.\n"
            "3) Or pass the correct path via '--input'.\n"
        )

    # --- Required files ---
    required_model_files = [
        input_files["registration_shares"],
        input_files["historical_registrations"],
        input_files["projected_registrations"],
        input_files["stock_by_age"],
        input_files["stock_year"],
    ]

    cluster_file = input_files["country_clusters"]

    required_validation_files = [
        input_files["validation_registration_shares"],
        input_files["validation_stock_shares"],
    ]

    required_historical_csp_files = [
        input_files["historical_csp_parameters"],
        input_files["historical_survival_rates"],
    ]

    # --- Check files ---
    check_required_files(input_dir, required_model_files, "running the model")

    if historical_validation_active:
        check_required_files(
            input_dir,
            required_validation_files,
            "validation against historical data",
            hint=(
                "If validation data are not available or validation is not needed, "
                "disable it in config.yaml by setting:\n\n"
                "model:\n"
                "  historical_validation: false"
            ),
        )

    if sensitivity_analysis_active and historical_csp_active:
        check_required_files(
            input_dir,
            required_historical_csp_files,
            "historical CSP sensitivity analysis",
            hint=(
                "If historical CSP sensitivity analysis is not needed, "
                "disable it in config.yaml by setting:\n\n"
                "model:\n"
                "  historical_csp: false"
            ),
        )

    if use_clusters_active:
        check_required_files(input_dir, [cluster_file], "country clustering")
    if not use_clusters_active and (input_dir / cluster_file).exists():
        warnings.warn(
            f"'{cluster_file}' was found in '{input_dir}' but will not be used "
            "because 'use_clusters' is set to False.",
            UserWarning
        )

    # --- Load always-needed data ---
    if use_clusters_active:
        clusters = pd.read_csv(input_dir / cluster_file, sep=";", decimal=",")
    else:
        clusters = None
    registration_shares_by_cluster = pd.read_csv(
        input_dir / input_files["registration_shares"],
        sep=";", decimal=","
    )
    if powertrains:
        validate_powertrains_in_data(
            registration_shares_by_cluster,
            powertrains,
            "registration shares by cluster"
        )

        registration_shares_by_cluster = add_rest_of_powertrains_from_selected_shares(
            registration_shares_by_cluster,
            powertrains,
            relative_sales_dim,
            "registration shares by cluster",
        )
    historical_registrations = pd.read_csv(
        input_dir / input_files["historical_registrations"],
        sep=";", decimal=","
    )
    registrations_projected = pd.read_csv(
        input_dir / input_files["projected_registrations"],
        sep=";", decimal=","
    )

    max_year = registrations_projected["time"].max()

    stock_by_age = pd.read_csv(
        input_dir / input_files["stock_by_age"],
        sep=";", decimal=","
    )

    if survival_grouping is None:
        survival_grouping = [country_dim]

    if survival_grouping == [country_dim] and powertrain_dim in stock_by_age.columns:
        raise ValueError(
            "Invalid stock-by-age input data.\n\n"
            "The current configuration estimates survival rates only by country:\n"
            "survival_rates:\n"
            "  grouping:\n"
            "    - geo country\n\n"
            "However, the stock-by-age input file contains a 'powertrain' column.\n\n"
            "How to fix:\n"
            "- Remove the 'powertrain' column from the stock-by-age input file, and\n"
            "- provide total stock by country and vehicle age only:\n"
            "  geo country;vehicle age;number of registered vehicles\n\n"
            "If you want country- and powertrain-specific survival rates, use:\n"
            "survival_rates:\n"
            "  grouping:\n"
            "    - geo country\n"
            "    - powertrain"
        )

    required_stock_columns = set(
        survival_grouping + [age_dim, number_registered_vehicles_dim]
    )

    missing_columns = required_stock_columns - set(stock_by_age.columns)

    if missing_columns:
        raise ValueError(
            "Invalid stock-by-age input data.\n\n"
            "The current configuration requires survival rates to be estimated by:\n"
            f"{survival_grouping}\n\n"
            "However, the stock-by-age input file does not contain all required columns.\n\n"
            f"Missing columns in 2_1 stock-by-age input file: {sorted(missing_columns)}\n\n"
            "How to fix:\n"
            "- If you want country-level survival rates only, use:\n"
            "  survival_rates:\n"
            "    grouping:\n"
            "      - geo country\n\n"
            "- If you want survival rates by country and powertrain, the 2_1 input file must contain:\n"
            "  geo country;vehicle age;powertrain;number of registered vehicles\n\n"
            "- If you later add vehicle size to the grouping, the 2_1 input file must also contain "
            "a corresponding vehicle size column."
        )

    if powertrains and survival_grouping and powertrain_dim in survival_grouping:
        stock_by_age = aggregate_stock_by_selected_powertrains(
            stock_by_age,
            powertrains,
            "stock by age"
        )

    if powertrain_dim in survival_grouping:
        registration_powertrains = set(
            registration_shares_by_cluster[powertrain_dim].dropna().unique()
        )
        stock_powertrains = set(
            stock_by_age[powertrain_dim].dropna().unique()
        )

        missing_stock_powertrains = registration_powertrains - stock_powertrains

        if missing_stock_powertrains:
            warnings.warn(
                "Some powertrain categories exist in the registration shares but not in the "
                "stock-by-age input data.\n\n"
                f"Missing from stock-by-age data: {sorted(missing_stock_powertrains)}\n\n"
                "Survival rates cannot be estimated for these categories, so stock will not "
                "be calculated for them. Total stock by country may therefore be incomplete.",
                UserWarning
            )

    if survival_grouping is None:
        survival_grouping = [country_dim]

    required_stock_columns = set(
        survival_grouping + [age_dim, number_registered_vehicles_dim]
    )

    missing_columns = required_stock_columns - set(stock_by_age.columns)

    if missing_columns:
        raise ValueError(
            "Invalid stock-by-age input data.\n\n"
            f"Missing columns: {sorted(missing_columns)}\n\n"

            f"Survival rates are configured to be estimated by: {survival_grouping}\n"
            "However, the input data does not contain all required dimensions.\n\n"

            "Note:\n"
            "- Country-level survival rates can always be estimated.\n"
            "- Additional detail (e.g. powertrain) requires disaggregated stock-by-age data.\n\n"

            "How to fix:\n"
            f"- Remove {sorted(missing_columns)} from the survival grouping in config.yaml\n"
            "  OR\n"
            f"- Provide stock-by-age data including: {sorted(required_stock_columns)}\n"
        )

    stock_year = pd.read_csv(
        input_dir / input_files["stock_year"],
        sep=";", decimal=","
    )

    data = {
        "clusters": clusters,
        "registration_shares_by_cluster": registration_shares_by_cluster,
        "historical_registrations": historical_registrations,
        "registrations_projected": registrations_projected,
        "stock_by_age": stock_by_age,
        "stock_year": stock_year,
    }

    # --- Optional: validation data ---
    if historical_validation_active:
        data["actual_bev_registration_shares"] = pd.read_csv(
            input_dir / input_files["validation_registration_shares"],
            sep=";", decimal=","
        )
        data["actual_bev_stock_shares"] = pd.read_csv(
            input_dir / input_files["validation_stock_shares"],
            sep=";", decimal=","
        )

    # --- Optional: sensitivity data ---
    if sensitivity_analysis_active and historical_csp_active:
        data["optimum_parameters_2008"] = pd.read_csv(
            input_dir / input_files["historical_csp_parameters"],
            sep=";", decimal=","
        )
        data["survival_rates_2016"] = pd.read_csv(
            input_dir / input_files["historical_survival_rates"],
            sep=";", decimal=","
        )

    return data, max_year


"""
Check that all required input files exist.
"""


def check_required_files(input_dir, files, purpose, hint=None):
    """
    Check that all required input files exist.

    Parameters:
        input_dir (Path):
            Directory containing the input files.

        files (list[str]):
            List of required file names.

        purpose (str):
            Description of the modeling step requiring the files.

    Raises:
        FileNotFoundError:
            If one or more required files are missing.
    """
    missing = [file for file in files if not (input_dir / file).exists()]

    if missing:
        message = (
                f"Missing input files for {purpose} in '{input_dir}':\n\n"
                + "\n".join(f"- {file}" for file in missing)
                + "\n\nCheck that the files exist and that their names are spelled correctly."
        )

        if hint:
            message += f"\n\n{hint}"

        raise FileNotFoundError(message)



"""
Validate that selected powertrains exist in the dataset.
"""


def validate_powertrains_in_data(df, selected_powertrains, dataset_name):
    """
    Validate that selected powertrains exist in the input dataset.

    The function checks whether all user-selected powertrain categories
    are available in the provided dataset. It also warns if additional
    powertrain categories exist in the dataset but are not selected.

    Parameters:
        df (pandas.DataFrame):
            Input dataset containing a powertrain column.

        selected_powertrains (list[str]):
            Powertrain categories selected by the user.

        dataset_name (str):
            Name of the dataset used for error and warning messages.

    Raises:
        ValueError:
            If one or more selected powertrains are not found in the dataset.

    Warns:
        UserWarning:
            If unused powertrain categories exist in the dataset.
    """
    available_powertrains = set(df[powertrain_dim].dropna().unique())
    selected_powertrains = set(selected_powertrains)

    missing_powertrains = selected_powertrains - available_powertrains

    if missing_powertrains:
        raise ValueError(
            f"Invalid powertrain configuration for {dataset_name}.\n\n"
            f"Selected powertrains not found in input data: {sorted(missing_powertrains)}\n"
            f"Available powertrains are: {sorted(available_powertrains)}"
        )

    unused_powertrains = available_powertrains - selected_powertrains

    if unused_powertrains:
        warnings.warn(
            f"The following powertrains exist in {dataset_name} but are not selected "
            f"and will be ignored: {sorted(unused_powertrains)}",
            UserWarning
        )


REST_POWERTRAIN = "Rest of powertrains"
SHARE_TOLERANCE = 1e-3

"""
Add a residual powertrain category from remaining shares.
"""


def add_rest_of_powertrains_from_selected_shares(
        df,
        selected_powertrains,
        share_column,
        dataset_name,
):
    """
    Add a residual powertrain category from remaining shares.

    The function keeps the selected powertrain categories and computes
    an additional category representing the remaining share not covered
    by the selected powertrains. The residual category is labeled
    `REST_POWERTRAIN`.

    Parameters:
        df (pandas.DataFrame):
            Input dataset containing powertrain shares.

        selected_powertrains (list[str]):
            Powertrain categories selected by the user.

        share_column (str):
            Name of the column containing share values.

        dataset_name (str):
            Name of the dataset used for error messages.

    Returns:
        pandas.DataFrame:
            DataFrame containing the selected powertrains and the
            additional residual powertrain category.

    Raises:
        ValueError:
            If selected powertrains are missing from the dataset or if
            selected shares exceed 1 for any group.
    """
    df = df.copy()
    selected_powertrains = list(selected_powertrains)

    available_powertrains = set(df[powertrain_dim].dropna().unique())
    missing_powertrains = set(selected_powertrains) - available_powertrains

    if missing_powertrains:
        raise ValueError(
            f"Invalid powertrain configuration for {dataset_name}.\n\n"
            f"Selected powertrains not found in input data: {sorted(missing_powertrains)}\n"
            f"Available powertrains are: {sorted(available_powertrains)}"
        )

    selected_df = df[df[powertrain_dim].isin(selected_powertrains)].copy()

    group_cols = [
        col for col in selected_df.columns
        if col not in [powertrain_dim, share_column]
    ]

    selected_sum = (
        selected_df
        .groupby(group_cols, as_index=False)[share_column]
        .sum()
        .rename(columns={share_column: "_selected_share_sum"})
    )

    rest_df = selected_sum.copy()
    rest_df[powertrain_dim] = REST_POWERTRAIN
    rest_df[share_column] = 1 - rest_df["_selected_share_sum"]

    if (rest_df[share_column] < -SHARE_TOLERANCE).any():
        raise ValueError(
            f"Invalid shares in {dataset_name}.\n\n"
            "Selected powertrain shares exceed 1 for at least one group."
        )

    rest_df[share_column] = rest_df[share_column].clip(lower=0)
    rest_df = rest_df[group_cols + [powertrain_dim, share_column]]

    result = pd.concat([selected_df, rest_df], ignore_index=True)

    return result


"""
Aggregate non-selected powertrains into a residual category.
"""


def aggregate_stock_by_selected_powertrains(df, selected_powertrains, dataset_name):
    """
    Aggregate non-selected powertrains into a residual category.

    The function replaces all powertrains that are not explicitly selected
    with the residual category `REST_POWERTRAIN`. The stock values of the
    non-selected powertrains are then aggregated by summing the number of
    registered vehicles across all remaining grouping dimensions.

    Parameters:
        df (pandas.DataFrame):
            Input stock-by-age dataset containing powertrain categories.

        selected_powertrains (list[str]):
            Powertrain categories selected by the user.

        dataset_name (str):
            Name of the dataset used for error messages.

    Returns:
        pandas.DataFrame:
            Aggregated DataFrame in which all non-selected powertrains are
            combined into the residual category `REST_POWERTRAIN`.

    Raises:
        ValueError:
            If selected powertrains are not found in the input dataset.
    """
    df = df.copy()
    selected_powertrains = list(selected_powertrains)

    available_powertrains = set(df[powertrain_dim].dropna().unique())
    missing_powertrains = set(selected_powertrains) - available_powertrains

    if missing_powertrains:
        raise ValueError(
            f"Invalid powertrain configuration for {dataset_name}.\n\n"
            f"Selected powertrains not found in input data: {sorted(missing_powertrains)}\n"
            f"Available powertrains are: {sorted(available_powertrains)}"
        )

    df[powertrain_dim] = df[powertrain_dim].where(
        df[powertrain_dim].isin(selected_powertrains),
        REST_POWERTRAIN
    )

    group_cols = [
        col for col in df.columns
        if col != number_registered_vehicles_dim
    ]

    return (
        df.groupby(group_cols, as_index=False)[number_registered_vehicles_dim]
        .sum()
    )
