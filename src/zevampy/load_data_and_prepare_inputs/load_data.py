"""Load and validate input datasets used by the ZEVAMPY model."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import pandas as pd
import numpy as np
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
}

VALID_SURVIVAL_SOURCES = {
    survival_source_stock_by_age_label,
    survival_source_empirical_label,
    survival_source_parameters_label,
}


def load_data(
    input_dir,
    historical_validation_active=False,
    validation_powertrain="BEV",
    use_clusters_active=True,
    powertrains=None,
    survival_grouping=None,
    survival_source=survival_source_stock_by_age_label,
    survival_source_file=None,
    input_files=None,
):
    """Load and validate datasets required by the configured model workflow."""
    input_dir = Path(input_dir)
    survival_grouping = survival_grouping or [country_dim]

    if survival_source not in VALID_SURVIVAL_SOURCES:
        raise ValueError(
            f"Invalid survival_rates.source '{survival_source}'. "
            f"Supported values are: {sorted(VALID_SURVIVAL_SOURCES)}"
        )

    input_files = {**DEFAULT_INPUT_FILES, **(input_files or {})}

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input directory '{input_dir}' does not exist.\n\n"
            "Create the input folder, update 'data.input_path' in config.yaml, "
            "or pass the correct path via '--input'."
        )

    required_model_files = [
        input_files["registration_shares"],
        input_files["historical_registrations"],
        input_files["projected_registrations"],
    ]
    if survival_source == survival_source_stock_by_age_label:
        required_model_files.extend([
            input_files["stock_by_age"],
            input_files["stock_year"],
        ])

    check_required_files(input_dir, required_model_files, "running the model")

    cluster_file = input_files["country_clusters"]
    if use_clusters_active:
        check_required_files(input_dir, [cluster_file], "country clustering")
    elif (input_dir / cluster_file).exists():
        warnings.warn(
            f"'{cluster_file}' was found in '{input_dir}' but will not be used "
            "because 'use_clusters' is set to False.",
            UserWarning,
        )

    if historical_validation_active:
        check_required_files(
            input_dir,
            [
                input_files["validation_registration_shares"],
                input_files["validation_stock_shares"],
            ],
            "validation against historical data",
            hint=(
                "If validation data are not available or validation is not needed, "
                "set model.historical_validation to false."
            ),
        )

    if survival_source != survival_source_stock_by_age_label:
        if not survival_source_file:
            raise ValueError(
                f"survival_rates.file must be provided when survival_rates.source is '{survival_source}'."
            )
        source_path = Path(survival_source_file)
        if not source_path.is_absolute():
            source_path = input_dir / source_path
        if not source_path.exists():
            raise FileNotFoundError(
                f"Alternative survival input file '{source_path}' does not exist."
            )
    else:
        source_path = None

    # Core registration inputs.
    clusters = (
        pd.read_csv(input_dir / cluster_file, sep=";", decimal=",")
        if use_clusters_active
        else None
    )
    registration_shares_by_cluster = pd.read_csv(
        input_dir / input_files["registration_shares"], sep=";", decimal=","
    )

    if powertrains:
        validate_powertrains_in_data(
            registration_shares_by_cluster,
            powertrains,
            "registration shares by cluster",
        )
        registration_shares_by_cluster = add_rest_of_powertrains_from_selected_shares(
            registration_shares_by_cluster,
            powertrains,
            relative_sales_dim,
            "registration shares by cluster",
        )

    historical_registrations = pd.read_csv(
        input_dir / input_files["historical_registrations"], sep=";", decimal=","
    )
    registrations_projected = pd.read_csv(
        input_dir / input_files["projected_registrations"], sep=";", decimal=","
    )
    max_year = registrations_projected[time_dim].max()

    data = {
        clusters_label: clusters,
        registration_shares_by_cluster_label: registration_shares_by_cluster,
        historical_registrations_label: historical_registrations,
        registrations_projected_label: registrations_projected,
    }

    # Survival assumptions are loaded according to the selected source.
    if survival_source == survival_source_stock_by_age_label:
        stock_by_age = pd.read_csv(
            input_dir / input_files["stock_by_age"], sep=";", decimal=","
        )
        stock_year = pd.read_csv(
            input_dir / input_files["stock_year"], sep=";", decimal=","
        )
        _validate_stock_by_age(stock_by_age, survival_grouping)

        if powertrains and powertrain_dim in survival_grouping:
            stock_by_age = aggregate_stock_by_selected_powertrains(
                stock_by_age,
                powertrains,
                "stock by age",
            )

        _warn_if_survival_powertrains_missing(
            registration_shares_by_cluster,
            stock_by_age,
            survival_grouping,
            "stock-by-age input data",
        )
        data[stock_by_age_label] = stock_by_age
        data[stock_year_label] = stock_year

    elif survival_source == survival_source_empirical_label:
        alternative_survival_rates = pd.read_csv(source_path, sep=";", decimal=",")
        _validate_empirical_survival_rates(alternative_survival_rates, survival_grouping)
        _warn_if_survival_powertrains_missing(
            registration_shares_by_cluster,
            alternative_survival_rates,
            survival_grouping,
            "alternative empirical survival-rate data",
        )
        data[alternative_survival_rates_label] = alternative_survival_rates

    elif survival_source == survival_source_parameters_label:
        alternative_csp_parameters = pd.read_csv(source_path, sep=";", decimal=",")
        _validate_csp_parameters(alternative_csp_parameters, survival_grouping)
        _warn_if_survival_powertrains_missing(
            registration_shares_by_cluster,
            alternative_csp_parameters,
            survival_grouping,
            "alternative CSP-parameter data",
        )
        data[alternative_csp_parameters_label] = alternative_csp_parameters

    # Optional historical validation data.
    if historical_validation_active:
        validation_registration_shares = pd.read_csv(
            input_dir / input_files["validation_registration_shares"],
            sep=";",
            decimal=",",
        )
        validation_stock_shares = pd.read_csv(
            input_dir / input_files["validation_stock_shares"],
            sep=";",
            decimal=",",
        )

        available_registration_powertrains = set(
            validation_registration_shares[powertrain_dim].dropna().unique()
        )
        available_stock_powertrains = set(
            validation_stock_shares[powertrain_dim].dropna().unique()
        )
        if validation_powertrain not in available_registration_powertrains:
            raise ValueError(
                f"Validation powertrain '{validation_powertrain}' is not available "
                "in the validation registration-share dataset.\n"
                f"Available powertrains are: {sorted(available_registration_powertrains)}"
            )
        if validation_powertrain not in available_stock_powertrains:
            raise ValueError(
                f"Validation powertrain '{validation_powertrain}' is not available "
                "in the validation stock-share dataset.\n"
                f"Available powertrains are: {sorted(available_stock_powertrains)}"
            )

        data[validation_registration_shares_label] = validation_registration_shares
        data[validation_stock_shares_label] = validation_stock_shares

    return data, max_year


def _validate_stock_by_age(stock_by_age, survival_grouping):
    if survival_grouping == [country_dim] and powertrain_dim in stock_by_age.columns:
        raise ValueError(
            "Invalid stock-by-age input data: the configured survival grouping is country-only, "
            "but the stock-by-age file contains a powertrain column. Remove the powertrain column "
            "or include 'powertrain' in survival_rates.grouping."
        )

    required_columns = set(survival_grouping + [age_dim, number_registered_vehicles_dim])
    missing_columns = required_columns - set(stock_by_age.columns)
    if missing_columns:
        raise ValueError(
            "Invalid stock-by-age input data. "
            f"Missing columns: {sorted(missing_columns)}. "
            f"Required columns are: {sorted(required_columns)}."
        )


def _validate_empirical_survival_rates(survival_rates, survival_grouping):
    required_columns = set(survival_grouping + [age_dim, survival_rate_dim])
    missing_columns = required_columns - set(survival_rates.columns)
    if missing_columns:
        raise ValueError(
            "Invalid alternative empirical survival-rate data. "
            f"Missing columns: {sorted(missing_columns)}. "
            f"Required columns are: {sorted(required_columns)}."
        )
    if survival_rates[survival_rate_dim].isna().any():
        raise ValueError("Alternative empirical survival-rate data contain missing survival-rate values.")
    if not pd.api.types.is_numeric_dtype(survival_rates[survival_rate_dim]):
        raise ValueError("Alternative empirical survival rates must contain numeric values.")
    if not np.isfinite(survival_rates[survival_rate_dim]).all():
        raise ValueError("Alternative empirical survival rates must contain only finite values.")
    if (survival_rates[survival_rate_dim] < 0).any():
        raise ValueError("Alternative empirical survival rates must be non-negative.")


def _validate_csp_parameters(parameters, survival_grouping):
    required_columns = set(
        survival_grouping + [gamma_weibull_dim, beta_weibull_dim, distribution_dim]
    )
    missing_columns = required_columns - set(parameters.columns)
    if missing_columns:
        raise ValueError(
            "Invalid alternative CSP-parameter data. "
            f"Missing columns: {sorted(missing_columns)}. "
            f"Required columns are: {sorted(required_columns)}."
        )

    invalid_distributions = set(parameters[distribution_dim].dropna().unique()) - {
        weibull_label,
        weibull_gaussian_label,
    }
    if invalid_distributions:
        raise ValueError(
            f"Unknown CSP distribution labels: {sorted(invalid_distributions)}. "
            f"Supported values are '{weibull_label}' and '{weibull_gaussian_label}'."
        )

    if parameters[gamma_weibull_dim].isna().any() or parameters[beta_weibull_dim].isna().any():
        raise ValueError("Alternative CSP parameters require non-missing Weibull gamma and beta values.")
    if (parameters[gamma_weibull_dim] <= 0).any() or (parameters[beta_weibull_dim] <= 0).any():
        raise ValueError("Weibull gamma and beta parameters must be greater than zero.")

    wg_rows = parameters[parameters[distribution_dim] == weibull_gaussian_label]
    if not wg_rows.empty:
        required_wg = [k_weibull_gaussian_dim, mu_weibull_gaussian_dim, sigma_weibull_gaussian_dim]
        missing_wg_columns = [column for column in required_wg if column not in parameters.columns]
        if missing_wg_columns:
            raise ValueError(
                "WG parameter rows require the following additional columns: "
                f"{missing_wg_columns}."
            )
        if wg_rows[required_wg].isna().any().any():
            raise ValueError("WG parameter rows require non-missing k, mu, and sigma values.")
        if (wg_rows[sigma_weibull_gaussian_dim] <= 0).any():
            raise ValueError("WG sigma parameters must be greater than zero.")

    duplicated = parameters.duplicated(subset=survival_grouping, keep=False)
    if duplicated.any():
        duplicate_groups = parameters.loc[duplicated, survival_grouping].drop_duplicates().to_dict(orient="records")
        raise ValueError(
            "Alternative CSP-parameter data must contain exactly one row per survival group. "
            f"Duplicate groups: {duplicate_groups}"
        )


def _warn_if_survival_powertrains_missing(registration_shares, survival_data, survival_grouping, dataset_name):
    if powertrain_dim not in survival_grouping or powertrain_dim not in survival_data.columns:
        return

    registration_powertrains = set(registration_shares[powertrain_dim].dropna().unique())
    survival_powertrains = set(survival_data[powertrain_dim].dropna().unique())
    missing_powertrains = registration_powertrains - survival_powertrains
    if missing_powertrains:
        warnings.warn(
            f"Some powertrain categories exist in the registration shares but not in {dataset_name}. "
            f"Missing survival assumptions for: {sorted(missing_powertrains)}. "
            "Absolute stock can still be calculated for available powertrains, but total stock shares may be incomplete.",
            UserWarning,
        )


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
