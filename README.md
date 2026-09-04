<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez

SPDX-License-Identifier: CC-BY-SA-4.0
-->

![zevampy Banner](fk_stock_model_banner.png)

[![PyPI version](https://img.shields.io/pypi/v/zevampy.svg)](https://pypi.org/project/zevampy/)
[![Latest release](https://img.shields.io/github/v/release/gabrielmoringmartinez/zevampy)](https://github.com/gabrielmoringmartinez/zevampy/releases)
[![Dependency](https://img.shields.io/badge/dependency-Python-orange)](https://www.python.org/)

[![CI](https://github.com/gabrielmoringmartinez/zevampy/actions/workflows/test.yml/badge.svg)](https://github.com/gabrielmoringmartinez/zevampy/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/gabrielmoringmartinez/zevampy/graph/badge.svg?token=Z1RUTSJLSY)](https://codecov.io/github/gabrielmoringmartinez/zevampy)

[![REUSE status](https://api.reuse.software/badge/github.com/gabrielmoringmartinez/zevampy)](https://api.reuse.software/info/github.com/gabrielmoringmartinez/zevampy)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

<a href="https://github.com/gabrielmoringmartinez/zevampy">
  <img src="https://raw.githubusercontent.com/gabrielmoringmartinez/zevampy/main/dlr_logo.png"
       align="right"
       height="120"
       width="120"
       alt="EU-ZEVAM logo" />
</a>

# 🚗 ZEVAMPY: Zero-Emission Vehicle Adoption Model in Python
**A flexible Python framework for vehicle stock modelling, fleet survival analysis, and zero-emission vehicle adoption projections**

**ZEVAMPY estimates future vehicle fleet composition by powertrain using empirical survival rates and vehicle registration scenarios.**


## Table of Contents
- [About](#-about)
- [Statement of need](#-statement-of-need)
- [Recommended skills](#-recommended-skills)
- [Installation](#-installation)
- [Survival-rate input formats](#survival-rate-input-formats)
- [Model outputs](#model-outputs)
- [CSP fitting: Weibull and WG](#csp-fitting-weibull-and-wg)
- [Historical validation](#historical-validation)
- [Testing](#-testing)
- [Acknowledgements](#-acknowledgements)
- [Authorship](#-authorship)
- [Citation](#-citation)
- [License](#-license)
- [Contacts](#%EF%B8%8F-contacts)

## 🔋 About

ZEVAMPY is an open-source Python framework for modelling vehicle fleet evolution using empirical survival rates and new vehicle registration scenarios. The framework estimates cumulative survival probability (CSP) curves, calculates vehicle stock by powertrain, and projects future fleet composition over user-defined time horizons.

Although ZEVAMPY was originally developed and validated for European passenger-car fleets, it is designed to be reusable for other countries, powertrain categories, and projection periods when suitable stock and registration data are available. Survival rates can be estimated at different aggregation levels, including country-level or combined country–powertrain groupings.

The repository includes a default European passenger-car application based on country-specific survival rates and registration scenarios for EU-27 countries and Norway. The methodological foundations draw on the transport-demand modelling framework presented in [Möring-Martínez et al., 2024](https://doi.org/10.1016/j.trd.2024.104372) and on the empirical survival-rate methodology described in [Held et al., 2021](https://doi.org/10.1186/s12544-020-00464-0). The framework has been applied to analyse future BEV fleet evolution in Europe in [Möring-Martínez et al., 2025](https://doi.org/10.1016/j.trd.2025.104945).

<div align="center">
  <img src="battery_electric_vehicle_stock_shares_eu_27_and_norway_up_to_2050_model_reference_scenario_.png" alt="Process Diagram" width="600" style="margin-bottom: 5px;">
  <p style="margin-top: 0;"><b>Figure 1:</b> Example output from ZEVAMPY showing projected BEV stock shares for EU-27 countries and Norway up to 2050 using country-specific empirical survival rates.</p>
</div>

## 📜 Statement of need

Vehicle fleet models are used to explore how passenger-car fleets evolve under different technology, policy, and market assumptions. However, many existing tools are difficult to reproduce, not openly available, or tightly coupled to a specific dataset or case study.

ZEVAMPY addresses this gap by providing a reusable and modular Python framework for vehicle stock modelling. It separates the modelling workflow into transparent components for data loading, survival-rate estimation, CSP fitting, stock calculation, validation, and plotting. This structure allows users to adapt the framework to different countries, powertrain classifications, vehicle categories, time horizons, and alternative survival assumptions.


**Core features**

- **Flexible stock projections:**  
  Users can project vehicle fleet composition by powertrain using custom registration scenarios and user-defined projection periods.

- **Empirical survival-rate estimation:**  
  Survival rates can be estimated from stock and registration data at different years and aggregation levels, including country-level or combined country–powertrain groupings.

- **CSP fitting and stock modelling:**  
  The framework fits cumulative survival probability curves and combines them with new registration data to estimate future vehicle stock.

- **Reusable and extensible design:**  
  The model can be coupled with external transportation models or scenario datasets, enabling applications beyond the default European passenger-car case.

- **Research-oriented analysis workflows:**  
  The framework supports historical validation and comparative scenario exploration based on alternative survival-rate and registration assumptions.

**Contribution to the state of the art**

Unlike many fleet-modelling tools, ZEVAMPY is open source, modular, and designed for reuse. It enables transparent analysis of how vehicle registrations and survival rates influence future fleet composition. While the default application focuses on European battery-electric passenger cars, the framework can be adapted to other regions, powertrain groups, and modelling horizons when the required input data are available.

**Explorative, not prescriptive**

ZEVAMPY does not optimize fleet composition. Instead, it helps users explore how different assumptions about vehicle registrations and fleet turnover affect future stock shares. This makes it useful for researchers, policymakers, and analysts who want to assess long-term fleet dynamics under alternative scenarios.

## 🔧 Recommended skills

ZEVAMPY is implemented in Python. While no programming skills are strictly required to configure and run the model, experience with transportation modeling and Python is beneficial. Developers wishing to modify the model's functionality or enhance its capabilities should have at least a basic understanding of Python.

## 📦 Installation

ZEVAMPY can be installed in two ways:

1. **As a user**: install the released package from PyPI.
2. **As a developer**: clone the repository and install it in editable mode.

### Requirements

ZEVAMPY requires:

- Python 3.12 or later
- `pip`
- input datasets in CSV format
- a YAML configuration file defining model settings and file paths

The package has primarily been developed and tested on Windows 10/11 using WSL2 Ubuntu. It should also work on Linux and macOS, but these systems have not yet been fully tested.

---

### What users need

To run ZEVAMPY, users provide a set of CSV input files together with a YAML configuration file describing the modelling setup.

Input and output directories are configured through `data.input_path` and `data.output_path`. Core and validation filenames are configurable through `data.files`, while survival-source-specific filenames are configured through `survival_rates.files`. The filenames listed below are therefore default filenames, not fixed requirements.

#### Required input datasets

##### Country clusters (optional)

- Logical input key: `country_clusters`
- Default filename: `0_country_clusters.csv`

Defines optional country clusters used to reduce the number of independent registration forecasts required. Countries assigned to the same cluster use the corresponding cluster-level projected powertrain registration shares.

This dataset is required only when country clustering is enabled:

```yaml
geography:
  use_clusters: true
```

If clustering is not required, it can be disabled with:

```yaml
geography:
  use_clusters: false
```

The default filename can be changed through `data.files.country_clusters`.

##### Historical and projected registration shares by powertrain

- Logical input key: `registration_shares`
- Default filename: `1_1_new_registrations_by_fuel_type_clusters.csv`

Contains historical and projected new-vehicle registration shares by powertrain for the defined countries or clusters.

The default filename can be changed through `data.files.registration_shares`.

##### Historical total vehicle registrations

- Logical input key: `historical_registrations`
- Default filename: `1_2_A_2_historical_new_registrations_data_passenger_cars.csv`

Contains historical absolute new-vehicle registrations by country.

The historical registration period must be sufficiently long to represent the configured CSP horizon. The relationship between registration history and `survival_rates.csp_available_years` is described in the Configuration reference.

The default filename can be changed through `data.files.historical_registrations`.

##### Projected total vehicle registrations

- Logical input key: `projected_registrations`
- Default filename: `1_3_new_registrations_projected.csv`

Contains projected total new-vehicle registrations by country for future years.

The last available year in this dataset determines the maximum available simulation horizon unless an earlier `model.end_year` is configured.

The default filename can be changed through `data.files.projected_registrations`.

##### Stock-by-age data

- Logical input key: `stock_by_age`
- Default filename: `2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv`

Contains vehicle stock resolved by vehicle age and is used when `survival_rates.source: stock_by_age` to derive empirical survival rates before fitting CSP curves.

For the default country-level survival grouping, the dataset must contain at least:

```text
geo country;vehicle age;number of registered vehicles
```

For country- and powertrain-specific survival rates, it must contain at least:

```text
geo country;powertrain;vehicle age;number of registered vehicles
```

In the powertrain-specific case, the survival input also contains a `Total` group representing the complete fleet. `Total` is used to calculate the stock-share denominator independently from the explicitly modelled technologies.

The filename can be changed through `survival_rates.files.stock_by_age`. This dataset is required only for the `stock_by_age` survival source.

##### Stock reference year for stock-by-age data

- Logical input key: `stock_year`
- Default filename: `2_2_A_1_stock_year.csv`

Defines the observation year associated with the stock-by-age data used to derive empirical survival rates. A reference year can be provided once per country or, when using country- and powertrain-specific survival rates, separately for each country-powertrain group. Country-level reference years are applied to all powertrains in that country.

The filename can be changed through `survival_rates.files.stock_year`. This dataset is required only for the `stock_by_age` survival source. There is no separate `csp_reference_year` setting in the current configuration.

---

#### Optional validation datasets

The historical-validation workflow is used to assess the model results against observed historical data. This provides a plausibility check for the stock-modelling approach before applying it to long-term projections.

For example, when projecting the future stock of electric vehicles or hydrogen-powered vehicles up to 2050, the first modelled years can be compared with available historical stock data. This helps users evaluate whether the model reproduces the observed market development before interpreting the long-term projection. 

The corresponding validation datasets are required only when `model.historical_validation` is enabled.

##### Historical registration shares for validation

- Logical input key: `validation_registration_shares`
- Default filename: `4_1_eafo_ev_new_registration_shares.csv`

Contains historical observed registration-share data used by the historical model-validation workflow.

The default filename can be changed through `data.files.validation_registration_shares`.

##### Historical stock shares for validation
- Logical input key: `validation_stock_shares`
- Default filename: `4_2_eafo_ev_stock_shares.csv`

Contains historical stock-share data used to compare modelled vehicle-stock shares with observed values.

The default filename can be changed through `data.files.validation_stock_shares`.

These datasets are required only when:

```yaml
model:
  historical_validation: true
```

They are not required for a basic stock-model run when historical validation is disabled.

### Configuration file

`config.yaml` is the main user-facing configuration file for ZEVAMPY. It controls input and output paths, selected countries and powertrains, simulation years, historical validation, and how survival assumptions are supplied and grouped.

A complete configuration matching the current default workflow is:

```yaml
data:
  input_path: inputs
  output_path: outputs

  files:
    country_clusters: 0_country_clusters.csv
    registration_shares: 1_1_new_registrations_by_fuel_type_clusters.csv
    historical_registrations: 1_2_A_2_historical_new_registrations_data_passenger_cars.csv
    projected_registrations: 1_3_new_registrations_projected.csv
    validation_registration_shares: 4_1_eafo_ev_new_registration_shares.csv
    validation_stock_shares: 4_2_eafo_ev_stock_shares.csv

model:
  first_stock_year: 2014
  end_year: 2050
  historical_validation: false
  validation_powertrain: BEV

geography:
  countries:
  use_clusters: true

powertrains:

survival_rates:
  source: stock_by_age
  grouping:
    - geo country
  csp_available_years: 45
  files:
    stock_by_age: 2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv
    stock_year: 2_2_A_1_stock_year.csv
```

#### Configuration reference

##### Data settings

| Setting | Default | Description |
|---|---|---|
| `data.input_path` | `inputs` | Directory containing the CSV input datasets. It can also be overridden with the CLI option `--input`. |
| `data.output_path` | `outputs` | Directory in which generated CSV files and figures are stored. It can also be overridden with `--output`. |
| `data.files` | ZEVAMPY default filenames | Optional mapping from logical core/validation datasets to filenames. Individual entries may be overridden without redefining the complete mapping. |

The configurable keys under `data.files` are:

- `country_clusters`
- `registration_shares`
- `historical_registrations`
- `projected_registrations`
- `validation_registration_shares`
- `validation_stock_shares`

Survival-source files are not configured under `data.files`; they belong under `survival_rates.files`.

##### Model settings

| Setting | Default | Description |
|---|---|---|
| `model.first_stock_year` | `2014` | First stock year included in the simulation output. |
| `model.end_year` | Last year available in projected registrations when omitted | Final year of the stock simulation. The repository configuration explicitly uses `2050`. |
| `model.historical_validation` | `false` | Enables historical model validation. When enabled, both validation datasets under `data.files` are required. |
| `model.validation_powertrain` | `BEV` | Powertrain whose historical registration and stock shares are evaluated when validation is enabled. It must be among the explicitly selected model powertrains. |

The start year of historical registrations is not configured manually. ZEVAMPY derives the earliest required cohort from `model.first_stock_year` and `survival_rates.csp_available_years`. For `stock_by_age`, an earlier stock reference year can extend the required registration history further backwards. ZEVAMPY raises an error if the selected countries do not have sufficient historical registration coverage.

##### Geography settings

| Setting | Default | Description |
|---|---|---|
| `geography.countries` | EU-27 + Norway | Countries included in the simulation. If left empty, ZEVAMPY uses its predefined EU-27 + Norway set. The required input and survival data must cover the selected/default countries; otherwise the model reports the missing coverage. |
| `geography.use_clusters` | `true` | If `true`, registration shares are assigned through the configured country-cluster mapping. If `false`, the registration-share input must contain country-specific shares. |

A custom country selection can be provided as:

```yaml
geography:
  countries:
    - Germany
    - France
  use_clusters: true
```

##### Powertrain settings

If `powertrains` is left empty, ZEVAMPY uses its predefined powertrain set:

```text
BEV
CNG
Diesel
FCEV
G-HEV
G-PHEV
Gasoline
LPG
D-HEV
```

A subset can be selected explicitly:

```yaml
powertrains:
  - BEV
  - Gasoline
```

The selected technologies are modelled individually. Their registration shares may sum to less than 1 because the total market is supplied independently through the historical and projected total-registration datasets. Non-selected technologies therefore do not need to be reconstructed as a residual category. They remain represented implicitly in the independently modelled complete fleet.

`Total` is a reserved model-generated powertrain label and must not be listed under `powertrains` or supplied in the registration-share input.

##### Survival-rate settings

| Setting | Default | Description |
|---|---|---|
| `survival_rates.source` | `stock_by_age` | Defines how survival assumptions enter the model. Supported values are `stock_by_age`, `empirical`, and `parameters`. |
| `survival_rates.grouping` | `[geo country]` | Dimensions defining one survival curve. The current examples support country-level and country-plus-powertrain grouping. |
| `survival_rates.csp_available_years` | `45` | Number of vehicle-age years represented by the CSP and therefore the maximum cohort age included in stock calculation. Values below 45 trigger a warning because older surviving cohorts may be truncated. |
| `survival_rates.files` | Source dependent | Maps survival-source-specific logical inputs to filenames. |

The three survival sources are configured as follows.

**Derive survival rates from stock-by-age data:**

```yaml
survival_rates:
  source: stock_by_age
  grouping:
    - geo country
  csp_available_years: 45
  files:
    stock_by_age: 2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv
    stock_year: 2_2_A_1_stock_year.csv
```

For `stock_by_age`, `stock_by_age` and `stock_year` have built-in default filenames and may be overridden under `survival_rates.files`.

**Fit CSP curves from user-supplied empirical survival rates:**

```yaml
survival_rates:
  source: empirical
  grouping:
    - geo country
  csp_available_years: 45
  files:
    empirical: empirical_survival_rates.csv
```

For `empirical`, `survival_rates.files.empirical` is required.

**Use previously fitted or externally supplied CSP parameters:**

```yaml
survival_rates:
  source: parameters
  grouping:
    - geo country
  csp_available_years: 45
  files:
    parameters: csp_parameters.csv
```

For `parameters`, `survival_rates.files.parameters` is required.

Country- and powertrain-specific survival assumptions are selected by adding `powertrain` to the grouping:

```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```

In this mode, survival inputs must contain separate assumptions for each explicitly modelled country-powertrain combination and for `Total`. The `Total` survival curve is used with total registrations to calculate the complete fleet stock, which forms the denominator of technology stock shares. Missing required survival groups cause a clear input/model validation error rather than an implicit fallback.

---

### Survival-rate input formats

ZEVAMPY supports three alternative ways of supplying vehicle survival assumptions. All three sources ultimately provide cumulative survival probability (CSP) curves that are applied to registration cohorts in the stock calculation, but they differ in how much preprocessing and curve fitting ZEVAMPY performs internally.

| `survival_rates.source` | User supplies | ZEVAMPY performs | `stock_year` required? |
|---|---|---|---|
| `stock_by_age` | Age-resolved vehicle stock and the corresponding stock reference year | Derives empirical survival rates, fits CSP curves, and calculates stock | Yes |
| `empirical` | Empirical survival rates by vehicle age | Fits CSP curves and calculates stock | No |
| `parameters` | Fitted Weibull or WG parameters | Generates CSP curves directly and calculates stock | No |

Survival input files support both semicolon-separated CSV files with decimal commas and standard comma-separated CSV files with decimal points.

#### Survival grouping

`survival_rates.grouping` defines which observations share one survival curve.

For one survival curve per country:

```yaml
survival_rates:
  grouping:
    - geo country
```

In this mode, the survival input contains no `powertrain` column. The country-specific CSP is applied to the independently modelled `Total` fleet and to each selected powertrain in that country.

For separate curves by country and powertrain:

```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```

In this mode, the survival input must contain a `powertrain` column and must provide survival assumptions for every selected powertrain and for `Total`. `Total` is required because its CSP is applied to total registrations to calculate the complete fleet stock used as the denominator of technology stock shares.

For example, if the model explicitly represents BEV and Gasoline, the required survival groups for one country are:

```text
Example Country / Total
Example Country / BEV
Example Country / Gasoline
```

`Total` is only used in survival inputs and model outputs. It must not be added to the registration-share input or to the `powertrains` list in `config.yaml`; total registrations are already supplied independently through the historical and projected total-registration datasets.

#### `stock_by_age`: derive empirical survival rates from fleet stock

With:

```yaml
survival_rates:
  source: stock_by_age
```

ZEVAMPY derives empirical survival rates from age-resolved stock and historical registration cohorts before fitting the CSP curves.

For country-level grouping, the stock-by-age file requires:

```text
geo country;vehicle age;number of registered vehicles
Example Country;1;3000000
Example Country;2;2990000
Example Country;3;2980000
```

The corresponding stock-reference-year file requires:

```text
geo country;stock year of empirical csp data
Example Country;2021
```

For country-plus-powertrain grouping, the stock-by-age file contains one age profile for `Total` and for every explicitly modelled powertrain:

```text
geo country;powertrain;vehicle age;number of registered vehicles
Example Country;Total;1;2999652
Example Country;Total;2;2997215
Example Country;BEV;1;198000
Example Country;BEV;2;185000
Example Country;Gasoline;1;2500000
Example Country;Gasoline;2;2450000
```

Stock reference years may be supplied once per country and applied to every powertrain in that country:

```text
geo country;stock year of empirical csp data
Example Country;2021
```

or separately for each country-powertrain survival group:

```text
geo country;powertrain;stock year of empirical csp data
Example Country;Total;2021
Example Country;BEV;2021
Example Country;Gasoline;2021
```

Group-specific reference years are useful when age-resolved stock data for different technologies originate from different observation years.

For each survival group, ZEVAMPY aligns stock age with the historical registration cohort according to:

```text
registration cohort year = stock reference year - vehicle age + 1
```

and calculates the empirical survival rate as:

```text
survival rate = registered vehicles in the stock of a certain vehicle age
                ----------------------------------------------------------
                new registrations of the corresponding year
```

With country-level grouping, total registrations are used for this calculation. With country-plus-powertrain grouping, each powertrain stock cohort is matched to registrations of the same powertrain, while `Total` is matched to total registrations.

Only vehicle ages up to `survival_rates.csp_available_years` are used in the CSP workflow. Within each configured survival group, the stock-by-age input must contain exactly one row for each consecutive integer vehicle age starting at `1`. The available sequence may end before `csp_available_years`; ZEVAMPY uses the available observations for fitting and generates the fitted CSP curve over the configured horizon. Input rows are ordered internally by vehicle age before fitting.

#### `empirical`: supply survival rates directly

With:

```yaml
survival_rates:
  source: empirical
  files:
    empirical: empirical_survival_rates.csv
```

ZEVAMPY skips the stock-by-age derivation step and fits CSP curves directly to user-supplied empirical survival rates.

For country-level grouping, the required columns are:

```text
geo country;vehicle age;survival rate
Example Country;1;1,0000
Example Country;2;0,9967
Example Country;3;0,9933
...
```

For country-plus-powertrain grouping:

```text
geo country;powertrain;vehicle age;survival rate
Example Country;Total;1;0,9999
Example Country;Total;2;0,9991
...
Example Country;BEV;1;0,9990
Example Country;BEV;2;0,9930
...
Example Country;Gasoline;1;0,9999
Example Country;Gasoline;2;0,9995
...
```

Each survival group must contain exactly one value for every integer vehicle age from `1` through `csp_available_years`.

Empirical survival rates must be numeric, finite, and non-negative. Values greater than `1` are intentionally allowed. This can occur, for example, when imports cause the number of vehicles from a cohort present in a country's stock to exceed the number of originally newly registered vehicles domestically in that country.

A separate stock-reference-year file is not required for this source because the empirical survival-by-age relationship has already been derived before it is supplied to ZEVAMPY.

#### `parameters`: supply fitted CSP parameters

With:

```yaml
survival_rates:
  source: parameters
  files:
    parameters: csp_parameters.csv
```

ZEVAMPY skips both empirical survival-rate derivation and parameter fitting. It generates the CSP curves directly from the supplied distribution parameters and then performs the cohort stock calculation.

For a Weibull curve, the required columns are:

```text
geo country;gamma (Weibull);beta (Weibull);distribution
Example Country;21,13;2,99;Weibull
```

For country-plus-powertrain grouping, add the `powertrain` column and provide one row for each required survival group, including `Total`:

```text
geo country;powertrain;gamma (Weibull);beta (Weibull);distribution
Example Country;Total;18,31;3,00;Weibull
Example Country;BEV;10,27;3,00;Weibull
Example Country;Gasoline;17,41;3,00;Weibull
```

The `distribution` column accepts `Weibull` or `WG`. All rows require `gamma (Weibull)` and `beta (Weibull)`. Rows using `WG` additionally require:

```text
k (Import-Gaussian)
mu (Import-Gaussian)
sigma (Import-Gaussian)
```

For example:

```text
geo country;gamma (Weibull);beta (Weibull);k (Import-Gaussian);mu (Import-Gaussian);sigma (Import-Gaussian);distribution
Example Country;18,0;3,0;2,0;5,0;30,0;WG
```

`gamma (Weibull)` and `beta (Weibull)` must be greater than zero, and `sigma (Import-Gaussian)` must be greater than zero for WG rows. There must be exactly one parameter row per configured survival group.

Parameter files produced by previous ZEVAMPY runs may also contain fit diagnostics such as R-squared values and additional output columns. These are allowed but are not required to regenerate CSP curves from the `parameters` source.

A stock-reference-year file is not required for supplied parameters because the CSP is already expressed as a function of vehicle age.

#### Choosing a survival source

The three inputs represent alternative entry points into the same stock-turnover workflow:

```text
stock_by_age  -> empirical survival rates -> fitted CSP parameters -> CSP curves -> stock
empirical     -----------------------------> fitted CSP parameters -> CSP curves -> stock
parameters    -----------------------------------------------------> CSP curves -> stock
```

`stock_by_age` is appropriate when age-resolved fleet stock and historical registrations are available and the empirical survival relationship should be derived inside ZEVAMPY. `empirical` is useful when survival rates have already been estimated externally or in a previous analysis. `parameters` is useful for reproducing previously fitted survival assumptions, applying literature-based parameters, or running alternative survival scenarios without refitting the curves.

### Model outputs

A standard model run writes the main registration and stock results to the configured `data.output_path`. Generated CSV outputs use comma separators and decimal points.

| Output file | Description |
|---|---|
| `1_1_absolute_registrations.csv` | Total new-vehicle registrations by country and year, combining historical and projected total-registration inputs over the modelled cohort period. |
| `1_2_registrations_by_powertrain.csv` | Registrations of the explicitly modelled powertrains, calculated from total registrations and registration shares. It also contains the internally generated `Total` rows used for complete-fleet stock calculation. |
| `3_1_stock_data_including_vehicle_age.csv` | Calculated vehicle stock by country, stock year, vehicle age, year of first registration, and powertrain, including `Total`. |
| `3_2_stock_shares.csv` | Stock by country, stock year, and powertrain together with the corresponding share of the independently modelled `Total` fleet. `Total` therefore has a share of `1`. |

Additional `2_*` files describe the empirical survival rates, fitted CSP parameters, and fitted CSP curves when the selected survival source performs fitting. These are documented in the next section. Optional historical-validation outputs use the `4_*` prefix and are documented under [Historical validation](#historical-validation).

---

### CSP fitting: Weibull and WG

When `survival_rates.source` is `stock_by_age` or `empirical`, ZEVAMPY fits two candidate cumulative survival probability (CSP) curves to every configured survival group: a Weibull survival curve and a Weibull-Gaussian (`WG`) curve. The selected curve is then used in the cohort stock calculation. When `survival_rates.source: parameters` is used, no fitting or model selection is performed; ZEVAMPY applies the `distribution` and parameters supplied by the user.

#### Weibull survival curve

The Weibull CSP implemented in ZEVAMPY is:

$$
S_W(a)=\exp\left[-\left(\frac{a}{\gamma}\right)^\beta
\left(\Gamma\left(1+\frac{1}{\beta}\right)\right)^\beta\right],
$$

where $a$ is vehicle age, $\gamma$ is the mean vehicle lifetime in the implemented parameterization, $\beta$ controls the shape of the survival curve, and $\Gamma(\cdot)$ is the gamma function.

This parameterization differs slightly from the conventional Weibull scale-parameter notation: the gamma-function term is included so that `gamma (Weibull)` corresponds to the mean lifetime rather than the conventional Weibull scale parameter. Larger `gamma` values therefore shift fleet turnover toward older vehicle ages, while `beta` controls how gradually or sharply retirement occurs around the characteristic lifetime.

#### Weibull-Gaussian (`WG`) curve

Empirical cohort survival rates can deviate from a monotonically decreasing Weibull curve. In particular, imported used vehicles can increase the number of vehicles of a given cohort present in a country relative to the number originally registered there, so empirical survival rates may exceed 1. ZEVAMPY therefore also fits a Weibull-Gaussian curve:

$$
S_{WG}(a)=S_W(a)+\delta\exp\left[-\frac{1}{2}\left(\frac{a-\mu}{\sigma}\right)^2\right],
$$

with

$$
\delta=\frac{k}{\sqrt{2\pi}\sigma}.
$$

The Gaussian component provides an additional age-dependent contribution on top of the Weibull survival curve. Its parameters are:

| Output column | Meaning |
|---|---|
| `k (Import-Gaussian)` | Scaling parameter controlling the overall magnitude of the Gaussian component. |
| `mu (Import-Gaussian)` | Vehicle age at which the Gaussian component is centred. |
| `sigma (Import-Gaussian)` | Standard deviation controlling the width of the Gaussian component across vehicle ages. |
| `delta (Import-Gaussian)` | Derived peak amplitude, calculated as `k / (sqrt(2*pi) * sigma)`. It is reported as a diagnostic output and is not required when supplying WG parameters through `source: parameters`. |

The Weibull parameters `gamma` and `beta` are fitted first. ZEVAMPY then holds those Weibull parameters fixed and optimizes the Gaussian parameters `k`, `mu`, and `sigma` for the WG candidate curve.

#### Fit quality and distribution selection

For both candidate curves, ZEVAMPY reports an R-squared value calculated as:

$$
R^2 = 1 - \frac{\sum_a (S_{model}(a)-S_{empirical}(a))^2}
{\sum_a (S_{empirical}(a)-\overline{S}_{empirical})^2}.
$$

The relevant output columns are:

| Output column | Meaning |
|---|---|
| `r squared (Weibull)` | Fit quality of the Weibull curve. |
| `r squared (Weibull and Import-Gaussian)` | Fit quality of the WG curve. |
| `distribution` | Curve selected for the stock calculation: `Weibull` or `WG`. |

ZEVAMPY deliberately favours the simpler Weibull curve unless the WG fit provides a meaningful improvement. `WG` is selected only when its R-squared is at least `0.025` higher than the Weibull R-squared. Otherwise `Weibull` is retained:

```text
if R2_Weibull + 0.025 > R2_WG:
    distribution = Weibull
else:
    distribution = WG
```

This threshold prevents the additional Gaussian component from being selected for only marginal improvements in fit.

#### CSP fitting outputs

When ZEVAMPY performs fitting, the main CSP outputs are:

- `2_1_optimum_parameters_csp_curves.csv`: one row per survival group containing the fitted Weibull parameters, Gaussian parameters, both R-squared values, and the selected `distribution`.
- `2_2_empirical_survival_rates.csv`: the empirical survival-rate observations used for fitting.
- `2_3_fitted_CSP_curves.csv`: fitted CSP values by vehicle age for both candidate curves, together with the selected distribution for each survival group.

The principal columns in `2_1_optimum_parameters_csp_curves.csv` are:

| Column | Interpretation |
|---|---|
| `gamma (Weibull)` | Mean vehicle lifetime in years in the ZEVAMPY Weibull parameterization. |
| `beta (Weibull)` | Weibull shape parameter. |
| `r squared (Weibull)` | Weibull fit quality. |
| `k (Import-Gaussian)` | Magnitude parameter of the Gaussian component. |
| `mu (Import-Gaussian)` | Centre age of the Gaussian component. |
| `sigma (Import-Gaussian)` | Width of the Gaussian component. |
| `delta (Import-Gaussian)` | Derived peak amplitude of the Gaussian component. |
| `r squared (Weibull and Import-Gaussian)` | WG fit quality. |
| `distribution` | Distribution selected for the stock calculation. |

`2_3_fitted_CSP_curves.csv` contains `survival rate Weibull` and `survival rate WG`. Both candidate curves are retained in the output for transparency, but the stock calculation uses only the curve identified by `distribution` for each survival group. If users supply Weibull-only parameters through `source: parameters`, WG values are not required and may be empty in this output.

---

### Historical validation

Historical validation is an optional workflow for comparing modelled stock shares with observed historical stock shares before interpreting long-term projections. It is enabled through:

```yaml
model:
  historical_validation: true
  validation_powertrain: BEV
```

`validation_powertrain` selects the technology evaluated by the validation workflow. It can be changed, for example, to `FCEV` or another explicitly modelled powertrain when corresponding validation data are available. The selected validation powertrain must be included in the modelled `powertrains`.

Historical validation is independent of the selected survival source. It can therefore be used with CSP curves derived from `stock_by_age`, fitted from `empirical` survival rates, or generated from supplied `parameters`.

#### Required validation inputs

When `model.historical_validation: true`, two additional datasets are required.

**Observed registration shares** (`data.files.validation_registration_shares`) must contain:

```text
geo country;time;powertrain;relative sales
Example Country;2018;BEV;0,020
Example Country;2019;BEV;0,035
Example Country;2020;BEV;0,060
```

**Observed stock shares** (`data.files.validation_stock_shares`) must contain:

```text
geo country;stock year;powertrain;share
Example Country;2018;BEV;0,004
Example Country;2019;BEV;0,007
Example Country;2020;BEV;0,012
```

Shares are supplied as fractions between `0` and `1`. The files may contain several powertrains, but the validation workflow filters them to `model.validation_powertrain`.

The validation period is determined automatically from the years for which modelled and observed stock-share data overlap for the selected powertrain.

#### Validation Step 1: observed registrations and configured CSP curves

The first validation step replaces the modelled registration share of the selected validation powertrain with its observed historical registration share. Absolute total registrations remain unchanged, and the model-generated `Total` registration series continues to represent the complete market.

When other technologies are explicitly modelled, their shares are adjusted only as required to keep the represented registration shares internally consistent. The stock is then recalculated using the **same configured CSP curves** as in the normal model run.

Conceptually:

```text
observed registration share of validation powertrain
                         +
             total registrations
                         +
             configured CSP curves
                         |
                         v
              recalculated stock share
                         |
                         v
             observed stock-share data
```

This comparison primarily evaluates the stock-turnover and survival assumptions conditional on the observed registration history. If the model cannot reproduce the observed stock development even when historical registration shares are supplied, the remaining discrepancy is associated mainly with the stock-turnover representation and its input assumptions rather than with the registration-share scenario.

#### Validation Step 2: modelled registrations and configured CSP curves

The second validation step compares the stock shares from the original model run directly with the observed stock shares. The original modelled registration trajectory is therefore retained.

Conceptually:

```text
modelled registration trajectory
              +
      configured CSP curves
              |
              v
      modelled stock share
              |
              v
    observed stock-share data
```

This step evaluates the combined effect of the registration trajectory and the survival/stock-turnover assumptions. Comparing Step 1 with Step 2 therefore helps distinguish discrepancies related primarily to the registration trajectory from those that remain when observed registrations are used.

#### Powertrain-specific survival rates

Historical validation also supports:

```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```

In this case, the selected validation powertrain is recalculated using its dedicated CSP curve, while `Total` continues to use the dedicated total-fleet CSP. The observed stock share is consequently compared against:

```text
stock of validation powertrain / independently modelled Total stock
```

This preserves the same total-fleet denominator used in the normal stock-share calculation.

#### RMSE and validation outputs

For both validation steps, ZEVAMPY generates a comparison figure across countries and calculates the root mean squared error (RMSE) between modelled and observed stock shares:

$$
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_{t=1}^{n}\left(s_{t}^{\mathrm{model}}-s_{t}^{\mathrm{observed}}\right)^2},
$$

where $s_t$ is the stock share in validation year $t$. Because stock shares are represented as fractions, an RMSE of `0.01` corresponds to approximately one percentage point.

For `validation_powertrain: BEV`, the RMSE outputs follow the pattern:

```text
4_1_rmse_validation_step_1_bev_all_countries.csv
4_2_rmse_validation_step_2_bev_all_countries.csv
```

and the corresponding figures are written to the configured `outputs/figures/` directory, for example:

```text
validation_step_1_actual_bev_registrations_and_configured_csp_curves_all_countries.pdf
validation_step_2_modelled_bev_registrations_and_configured_csp_curves_all_countries.pdf
```

The filenames are generated dynamically from `validation_powertrain` when another technology is selected.

When historical validation is disabled:

```yaml
model:
  historical_validation: false
```

the validation datasets are not required and no validation plots or RMSE files are generated.

---

### Installation for users

Use this option if you want to run ZEVAMPY without modifying the source code.

#### 1. Create and activate a virtual environment

```bash
python -m venv venv
```
On Windows PowerShell:
```powershell
venv\Scripts\Activate.ps1
```
On Linux/macOS/WSL:
```bash
source venv/bin/activate
```
#### 2. Install ZEVAMPY from PyPI
```bash
pip install zevampy
```
#### 3. Prepare your input folder
Create a project folder containing:
```bash
my_zevampy_project/
├── config.yaml
├── inputs/
└── outputs/
```
The `inputs` folder should contain the required CSV input files.
#### 4. Configure the model
Edit `config.yaml` to define the model setup, for example:

```yaml
data:
  input_path: inputs
  output_path: outputs

geography:
  countries:
    - Germany
    - France
  use_clusters: true

powertrains:
  - BEV
  - Gasoline

model:
  first_stock_year: 2014
  end_year: 2050
  historical_validation: false
  validation_powertrain: BEV

survival_rates:
  source: stock_by_age
  grouping:
    - geo country
  csp_available_years: 45
  files:
    stock_by_age: 2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv
    stock_year: 2_2_A_1_stock_year.csv
```

To estimate and apply survival rates separately by country and powertrain, add `powertrain` to `survival_rates.grouping`. The corresponding survival input must then contain the selected powertrains plus `Total` for the complete-fleet denominator.

#### 5. Run ZEVAMPY
```bash
zevampy --config config.yaml
```
Alternatively:
```bash
python -m zevampy.cli --config config.yaml
```

##### Validate inputs before running the model

ZEVAMPY can validate the input datasets and configuration without running the complete modelling workflow:
```bash
zevampy --config config.yaml --validate-inputs
```
Alternatively:
```bash
python -m zevampy.cli --config config.yaml --validate-inputs
```

The validation checks the availability and consistency of the required input files and model configuration, including selected powertrains, survival-rate dimensions, and the registration history required for CSP estimation.

If all checks are successful, ZEVAMPY reports:

```text
Input validation successful.
```

Input validation does not calculate vehicle stock, generate figures, or perform historical model validation.

#### 🚀 Examples

Two self-contained runnable examples are included in the repository:

- [`examples/minimal_example/`](https://github.com/gabrielmoringmartinez/zevampy/tree/main/examples/minimal_example) demonstrates country-level survival rates shared by the complete fleet and the selected powertrains.
- [`examples/minimal_example_powertrain_survival/`](https://github.com/gabrielmoringmartinez/zevampy/tree/main/examples/minimal_example_powertrain_survival) demonstrates separate survival rates for `Total`, BEV, and Gasoline, including the independently modelled complete-fleet denominator.

Each example contains ready-to-run configurations for all three supported survival sources: `stock_by_age`, `empirical`, and `parameters`. The README inside each example folder describes the inputs and commands in more detail.


### Installation for developers
Use this option if you want to modify the codebase or contribute to ZEVAMPY.
#### 1. Clone the repository
```bash
git clone https://github.com/gabrielmoringmartinez/zevampy.git
cd zevampy
```
#### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
On Windows PowerShell:
```bash
venv\Scripts\Activate.ps1
```
On Linux/macOS/WSL:
```bash
source venv/bin/activate
```
#### 3. Install the package in editable mode
Install ZEVAMPY together with the development testing dependencies:
```bash
pip install -e ".[test]"
```
This installs ZEVAMPY in editable mode together with pytest and pytest-cov.
#### 4. Run the model locally
```bash
zevampy --config config.yaml
```
or:
```bash
python -m zevampy.cli --config config.yaml
```
---
### Adapting ZEVAMPY to new use cases

ZEVAMPY separates model logic from input datasets and configuration settings, allowing users to adapt the framework to new applications without modifying the core source code.

ZEVAMPY is designed to be reusable beyond the default European passenger-car case.

Users can adapt:
- Countries or regions through `geography.countries`
- Powertrains through the `powertrains` list
- Projection horizon through `model.end_year`
- Input and output folders through the `data` section
- Input filenames through `data.files`
- Survival-rate grouping through `survival_rates.grouping`

For example, to model country- and powertrain-specific survival rates:
```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```
The input stock-by-age file must then include at least:
```text
geo country;vehicle age;powertrain;number of registered vehicles
```
For country-level survival rates only, the stock-by-age input file should include:
```text
geo country;vehicle age;number of registered vehicles
```
This makes it possible to extend ZEVAMPY to additional countries, powertrain categories, vehicle classes, or projection horizons when suitable input data are available.

## 🧪 Testing
[![CI](https://github.com/gabrielmoringmartinez/zevampy/actions/workflows/test.yml/badge.svg)](https://github.com/gabrielmoringmartinez/zevampy/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/gabrielmoringmartinez/zevampy/graph/badge.svg?token=Z1RUTSJLSY)](https://codecov.io/github/gabrielmoringmartinez/zevampy)

This repository includes automated tests to verify input-data consistency, model execution, output generation, and command-line functionality.

Install the package together with the testing dependencies:
```bash
pip install -e ".[test]"
```
Run the complete test suite from the repository root with:
```bash
pytest
```
Pytest and coverage settings are defined in `pyproject.toml`. Coverage is measured for the zevampy package only.

### Run a specific test

A specific test file can be executed directly, for example:

```bash
pytest tests/test_5_validate_inputs_cli.py
```
The test suite uses temporary output directories where appropriate so that test-generated model results do not overwrite normal ZEVAMPY outputs.

## 🤝 Acknowledgements

Development of the Zero-Emission Vehicle Adoption Model in Python (ZEVAMPY) was funded through the NDC ASPECTS project, which received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No. 101003866.

Additional support for this research was provided through the MoDa project of the German Aerospace Center (DLR).

The authors gratefully acknowledge all contributors, collaborators, and reviewers who supported the development and testing of the model.

## ✍️ Authorship

ZEVAMPY was developed by [Gabriel Möring-Martínez](https://orcid.org/0009-0003-4380-3081) at the DLR's Institute of Vehicle concepts. Special thanks to the DLR members [Stephan Schmid](https://orcid.org/0000-0002-3081-8749), [Isheeka Dasgupta](https://www.linkedin.com/in/isheeka644/), [Murat Senzeybek](https://orcid.org/0000-0003-1769-3539) and [Samuel Hasselwander](https://orcid.org/0000-0002-0805-9061) for their contributions to the model conceptualization and development.

Additional thanks to [Fabia Miorelli](https://orcid.org/0000-0001-5095-5401) for contributions that improved the reusability and software engineering practices of ZEVAMPY.

## 📝 Citation

If you use ZEVAMPY in academic work, please cite the software publication below.

### Software citation

Möring-Martínez, G. (2026). "ZEVAMPY: Zero-Emission Vehicle Adoption Model in Python." *Journal of Open Source Software*, XX(XXX), XXXX. [doi:XX.XXXXX/joss.XXXXX](doi:XX.XXXXX/joss.XXXXX), [https://doi:XX.XXXXX/joss.XXXXX](https://doi:XX.XXXXX/joss.XXXXX)
```bibtex
@article{MoringMartinez2025ZEVAMPY,
  author = {M{\"o}ring-Martínez, Gabriel},
  title = {{ZEVAMPY}: Zero-Emission Vehicle Adoption Model in {Python}},
  year = {2026},
  doi = {10.21105/joss.XXXXX},
  url = {https://doi.org/XX.XXXXX/joss.XXXXX},
  journal = {Journal of Open Source Software},
  volume = {X},
  number = {X},
  pages = {X},
  publisher = {The Open Journal}
}
```

### Related research article

The following article presents an early scientific application of the modelling framework and discusses the impact of fleet turnover on vehicle electrification in Europe:

Möring-Martínez, G., Senzeybek, M., Hasselwander, S., & Schmid, S. (2025). Quantifying the impact of fleet turnover on electric vehicle uptake in Europe. Transportation Research Part D: Transport and Environment, 147, 104945. [https://doi.org/10.1016/j.trd.2025.104945](https://doi.org/10.1016/j.trd.2025.104945)

```bibtex
@article{MoringMartinez2025TRD,
  author = {Gabriel M{\"o}ring-Mart{\'i}nez and Murat Senzeybek and Samuel Hasselwander and Stephan Schmid},
  year = {2025},
  title = {Quantifying the impact of fleet turnover on electric vehicle uptake in Europe},
  url = {https://www.sciencedirect.com/science/article/pii/S1361920925003554},
  pages = {104945},
  volume = {147},
  issn = {13619209},
  journal = {Transportation Research Part D: Transport and Environment},
  doi = {10.1016/j.trd.2025.104945}
}
```
You can also find machine-readable citation metadata in the [CITATION.cff](https://github.com/gabrielmoringmartinez/zevampy/blob/main/CITATION.cff) file for use with GitHub’s citation button, Zotero, and other citation tools.

## 📃 License

[![REUSE status](https://api.reuse.software/badge/github.com/gabrielmoringmartinez/zevampy)](https://api.reuse.software/info/github.com/gabrielmoringmartinez/zevampy)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

The ZEVAMPY software is licensed under the [MIT License](LICENSE). Other repository content, such as documentation, figures, and research datasets, may use different licenses as described below.

This project is REUSE compliant and uses file-level licensing depending on content type:

- **Source code, tests, configuration files, and synthetic example/test data**: [MIT License](LICENSE)
- **Documentation and original figures**: [CC BY SA 4.0](LICENSES/CC-BY-SA-4.0.txt)
- **Minor metadata**: [CC0-1.0](LICENSES/CC0-1.0.txt) where indicated
- **Research input datasets**: Licensed individually according to their respective sources. See the file-level SPDX/REUSE metadata and [LICENSE.md](./LICENSE.md) for details.

For full licensing details and exceptions, see the [LICENSE.md](./LICENSE.md) file.

## 🗨️ Contacts

For questions, collaborations, or support related to ZEVAMPY, please contact:

- **Email:** [gabriel.moeringmartinez@dlr.de](mailto:gabriel.moeringmartinez@dlr.de)
- **DLR Institute of Vehicle Concepts:** https://www.dlr.de/en/fk

Follow the DLR Institute of Vehicle Concepts on LinkedIn for updates and publications:

[![LinkedIn](https://img.shields.io/badge/subscribe-white.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYTIuMDYyIDIuMDYyIDAgMCAxLTIuMDYzLTIuMDY1IDIuMDY0IDIuMDY0IDAgMSAxIDIuMDYzIDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiIGZpbGw9IiMwQTY2QzIiLz48cGF0aCBzdHlsZT0iZmlsbDojZmZmO3N0cm9rZS13aWR0aDouMDIwOTI0MSIgZD0iTTQuOTE3IDcuMzc3YTIuMDUyIDIuMDUyIDAgMCAxLS4yNC0zLjk0OWMxLjEyNS0uMzg0IDIuMzM5LjI3NCAyLjY1IDEuNDM3LjA2OC4yNS4wNjguNzY3LjAwMSAxLjAxYTIuMDg5IDIuMDg5IDAgMCAxLTEuNjIgMS41MSAyLjMzNCAyLjMzNCAwIDAgMS0uNzktLjAwOHoiLz48cGF0aCBzdHlsZT0iZmlsbDojZmZmO3N0cm9rZS13aWR0aDouMDIwOTI0MSIgZD0iTTQuOTE3IDcuMzc3YTIuMDU2IDIuMDU2IDAgMCAxLTEuNTItMi42NyAyLjA0NyAyLjA0NyAwIDAgMSAzLjQxOS0uNzU2Yy4yNC4yNTQuNDIuNTczLjUxMi45MDguMDY1LjI0LjA2NS43OCAwIDEuMDItLjA1MS4xODYtLjE5Ny41MDQtLjMuNjUyLS4wOS4xMzItLjMxLjM2Mi0uNDQzLjQ2NC0uNDYzLjM1Ny0xLjEuNTAzLTEuNjY4LjM4MlpNMy41NTcgMTQuNzJWOS4wMDhoMy41NTd2MTEuNDI0SDMuNTU3Wk05LjM1MyAxNC43MlY5LjAwOGgzLjQxMXYuNzg1YzAgLjYxNC4wMDUuNzg0LjAyNi43ODMuMDE0IDAgLjA3LS4wNzMuMTI0LS4xNjIuNTI0LS44NjUgMS41MDgtMS40NzggMi42NS0xLjY1LjI3NS0uMDQyIDEtLjA0NyAxLjMzMi0uMDA5Ljc5LjA5IDEuNDUxLjMxNiAxLjk0LjY2NC4yMi4xNTcuNTU3LjQ5My43MTQuNzEzLjQyLjU5Mi42OSAxLjQxMi44MDggMi40NjQuMDc0LjY2My4wODQgMS4yMTUuMDg1IDQuNTc4djMuMjU4aC0zLjUzNnYtMi45ODZjMC0yLjk3LS4wMS0zLjQ3NC0uMDc0LTMuOTA4LS4wOS0uNjA2LS4zMTQtMS4wODItLjYzNC0xLjM0Mi0uMzk1LS4zMjItMS4wMjktLjQzNy0xLjcwMy0uMzA5LS44NTguMTYzLTEuMzU1Ljc1LTEuNTIzIDEuNzk3LS4wNzYuNDcxLS4wODQuODQ1LS4wODQgMy44MzR2Mi45MTRIOS4zNTN6Ii8+PC9zdmc+)](https://www.linkedin.com/showcase/dlr-institut-fuer-fahrzeugkonzepte/posts/?feedView=all)

[Back to top](#top)
