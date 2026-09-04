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
    "validation_registration_shares": "4_1_eafo_ev_new_registration_shares.csv",
    "validation_stock_shares": "4_2_eafo_ev_stock_shares.csv",
}

DEFAULT_SURVIVAL_FILES = {
    "stock_by_age": "2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv",
    "stock_year": "2_2_A_1_stock_year.csv",
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
    survival_files=None,
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
    survival_files = survival_files or {}

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
        configured_survival_files = {
            **DEFAULT_SURVIVAL_FILES,
            **survival_files,
        }
        required_model_files.extend([
            configured_survival_files["stock_by_age"],
            configured_survival_files["stock_year"],
        ])
    else:
        configured_survival_files = survival_files

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

    if survival_source == survival_source_empirical_label:
        source_file = configured_survival_files.get("empirical")
        if not source_file:
            raise ValueError(
                "survival_rates.files.empirical must be provided when "
                "survival_rates.source is 'empirical'."
            )
        source_path = _resolve_input_path(input_dir, source_file)
    elif survival_source == survival_source_parameters_label:
        source_file = configured_survival_files.get("parameters")
        if not source_file:
            raise ValueError(
                "survival_rates.files.parameters must be provided when "
                "survival_rates.source is 'parameters'."
            )
        source_path = _resolve_input_path(input_dir, source_file)
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

    validate_registration_shares(
        registration_shares_by_cluster,
        "registration shares by cluster",
    )

    if powertrains:
        if total_powertrain_label in powertrains:
            raise ValueError(
                f"'{total_powertrain_label}' is generated automatically from total "
                "registrations and must not be listed under 'powertrains'."
            )
        validate_powertrains_in_data(
            registration_shares_by_cluster,
            powertrains,
            "registration shares by cluster",
        )
        registration_shares_by_cluster = filter_selected_powertrains(
            registration_shares_by_cluster,
            powertrains,
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
        stock_by_age = _read_csv(
            _resolve_input_path(input_dir, configured_survival_files["stock_by_age"])
        )
        stock_year = _read_csv(
            _resolve_input_path(input_dir, configured_survival_files["stock_year"])
        )
        _validate_stock_by_age(stock_by_age, survival_grouping)

        if powertrains and powertrain_dim in survival_grouping:
            stock_by_age = filter_powertrain_survival_groups(
                stock_by_age,
                powertrains,
            )
            if powertrain_dim in stock_year.columns:
                stock_year = filter_powertrain_survival_groups(
                    stock_year,
                    powertrains,
                )

        _validate_stock_year(stock_year, stock_by_age, survival_grouping)
        data[stock_by_age_label] = stock_by_age
        data[stock_year_label] = stock_year

    elif survival_source == survival_source_empirical_label:
        alternative_survival_rates = _read_csv(source_path)
        _validate_empirical_survival_rates(alternative_survival_rates, survival_grouping)
        data[alternative_survival_rates_label] = alternative_survival_rates

    elif survival_source == survival_source_parameters_label:
        alternative_csp_parameters = _read_csv(source_path)
        _validate_csp_parameters(alternative_csp_parameters, survival_grouping)
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



def _resolve_input_path(input_dir, file_name):
    """Resolve an input file relative to the configured input directory."""
    path = Path(file_name)
    if not path.is_absolute():
        path = input_dir / path
    if not path.exists():
        raise FileNotFoundError(f"Input file '{path}' does not exist.")
    return path


def _read_csv(file_path):
    """Read either standard CSV or semicolon/decimal-comma input files."""
    with open(file_path, "r", encoding="utf-8-sig") as stream:
        header = stream.readline()

    if ";" in header:
        return pd.read_csv(file_path, sep=";", decimal=",")
    return pd.read_csv(file_path)


def _get_stock_year_grouping(stock_year, survival_grouping):
    """Return the dimensions used to assign stock reference years.

    Stock reference years may be supplied either for the full survival group
    (for example country + powertrain) or only by country. Country-only years
    are broadcast to every powertrain in that country.
    """
    if all(dim in stock_year.columns for dim in survival_grouping):
        return list(survival_grouping)

    if country_dim in stock_year.columns:
        missing_group_dims = [
            dim for dim in survival_grouping
            if dim != country_dim and dim in stock_year.columns
        ]
        if not missing_group_dims:
            return [country_dim]

    raise ValueError(
        "Invalid stock-year input data. Stock reference years must be provided "
        f"either for every configured survival grouping dimension {survival_grouping} "
        f"or by '{country_dim}' only."
    )


def _validate_stock_year(stock_year, stock_by_age, survival_grouping):
    required_columns = {country_dim, stock_year_empirical_csp_data_dim}
    missing_columns = required_columns - set(stock_year.columns)
    if missing_columns:
        raise ValueError(
            "Invalid stock-year input data. "
            f"Missing columns: {sorted(missing_columns)}. "
            f"Required columns include: {sorted(required_columns)}."
        )

    if stock_year[stock_year_empirical_csp_data_dim].isna().any():
        raise ValueError("Stock-year input data contain missing reference-year values.")

    if not pd.api.types.is_numeric_dtype(stock_year[stock_year_empirical_csp_data_dim]):
        raise ValueError("Stock reference years must contain numeric values.")

    year_grouping = _get_stock_year_grouping(stock_year, survival_grouping)

    duplicated = stock_year.duplicated(subset=year_grouping, keep=False)
    if duplicated.any():
        duplicate_groups = (
            stock_year.loc[duplicated, year_grouping]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        raise ValueError(
            "Stock-year input data must contain exactly one reference year per "
            f"stock-year group. Duplicate groups: {duplicate_groups[:10]}"
        )

    required_groups = stock_by_age[year_grouping].drop_duplicates()
    available_groups = stock_year[year_grouping].drop_duplicates()
    missing_groups = (
        required_groups
        .merge(available_groups, on=year_grouping, how="left", indicator=True)
        .query("_merge == 'left_only'")
        .drop(columns="_merge")
    )
    if not missing_groups.empty:
        raise ValueError(
            "Stock-year input data are missing reference years for stock-by-age "
            f"groups: {missing_groups.head(10).to_dict(orient='records')}"
        )


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


SHARE_TOLERANCE = 1e-6


def validate_registration_shares(df, dataset_name):
    """Validate non-exhaustive powertrain registration-share inputs.

    Registration-share inputs may contain only the technologies that a user
    wants to model explicitly. Their shares therefore do not need to sum to
    one. Total registrations are supplied independently and the complete fleet
    is represented by the model-generated ``Total`` series.
    """
    required_columns = {powertrain_dim, relative_sales_dim}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Invalid {dataset_name}. Missing columns: {sorted(missing_columns)}."
        )

    if total_powertrain_label in set(df[powertrain_dim].dropna().astype(str)):
        raise ValueError(
            f"'{total_powertrain_label}' is a reserved model-generated powertrain label. "
            f"Do not add it to {dataset_name}; total registrations are read from the "
            "historical/projected registration inputs."
        )

    shares = pd.to_numeric(df[relative_sales_dim], errors="coerce")
    if shares.isna().any() or not np.isfinite(shares).all():
        raise ValueError(f"{dataset_name} must contain finite numeric registration shares.")
    if (shares < -SHARE_TOLERANCE).any() or (shares > 1 + SHARE_TOLERANCE).any():
        raise ValueError(
            f"Registration shares in {dataset_name} must be between 0 and 1."
        )

    grouping_candidates = [time_dim, cluster_dim, country_dim]
    grouping = [column for column in grouping_candidates if column in df.columns]
    if not grouping:
        raise ValueError(
            f"Cannot validate {dataset_name}: no time/cluster/country grouping columns were found."
        )

    share_sums = df.assign(**{relative_sales_dim: shares}).groupby(grouping)[relative_sales_dim].sum()
    invalid = share_sums[share_sums > 1 + SHARE_TOLERANCE]
    if not invalid.empty:
        examples = invalid.head(10).to_dict()
        raise ValueError(
            f"Registration shares in {dataset_name} exceed 1 for some groups. "
            f"Selected/available technologies may sum to less than 1, but never more than 1. "
            f"Examples: {examples}"
        )


def filter_selected_powertrains(df, selected_powertrains):
    """Keep only explicitly selected technologies in registration-share data."""
    return df[df[powertrain_dim].isin(selected_powertrains)].copy()


def filter_powertrain_survival_groups(df, selected_powertrains):
    """Keep selected powertrains plus the required ``Total`` survival group.

    Under powertrain-specific survival grouping, ``Total`` represents the
    complete fleet and supplies the denominator used for stock shares.
    """
    required_powertrains = set(selected_powertrains) | {total_powertrain_label}
    return df[df[powertrain_dim].isin(required_powertrains)].copy()
