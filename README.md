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
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSES/MIT.txt)

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
- [Testing](#-testing)
- [Acknowledgements](#-acknowledgements)
- [Authorship](#-authorship)
- [Citation](#-citation)
- [License](#-license)
- [Contacts](#%EF%B8%8F-contacts)

## 🔋 About

ZEVAMPY is an open-source Python framework for modelling vehicle fleet evolution using empirical survival rates and new vehicle registration scenarios. The framework estimates cumulative survival probability (CSP) curves, calculates vehicle stock by powertrain, and projects future fleet composition over user-defined time horizons.

Although ZEVAMPY was originally developed and validated for European passenger-car fleets, it is designed to be reusable for other countries, powertrain categories, and projection periods when suitable stock and registration data are available. Survival rates can be estimated at different aggregation levels, including country-level, powertrain-level, or combined country–powertrain groupings.

The repository includes a default European passenger-car application based on country-specific survival rates and registration scenarios for EU-27 countries and Norway. The methodological foundations draw on the transport-demand modelling framework presented in [Möring-Martínez et al., 2024](https://doi.org/10.1016/j.trd.2024.104372) and on the empirical survival-rate methodology described in [Held et al., 2021](https://doi.org/10.1186/s12544-020-00464-0). The framework has been applied to analyse future BEV fleet evolution in Europe in [Möring-Martínez et al., 2025](https://doi.org/10.1016/j.trd.2025.104945).

<div align="center">
  <img src="battery_electric_vehicle_stock_shares_eu_27_and_norway_up_to_2050_model_reference_scenario_.png" alt="Process Diagram" width="600" style="margin-bottom: 5px;">
  <p style="margin-top: 0;"><b>Figure 1:</b> Example output from ZEVAMPY showing projected BEV stock shares for EU-27 countries and Norway up to 2050 using country-specific empirical survival rates.</p>
</div>

## 📜 Statement of need

Vehicle fleet models are used to explore how passenger-car fleets evolve under different technology, policy, and market assumptions. However, many existing tools are difficult to reproduce, not openly available, or tightly coupled to a specific dataset or case study.

ZEVAMPY addresses this gap by providing a reusable and modular Python framework for vehicle stock modelling. It separates the modelling workflow into transparent components for data loading, survival-rate estimation, CSP fitting, stock calculation, validation, plotting, and sensitivity analysis. This structure allows users to adapt the framework to different countries, powertrain classifications, vehicle categories, and time horizons.


**Core features**

- **Flexible stock projections:**  
  Users can project vehicle fleet composition by powertrain using custom registration scenarios and user-defined projection periods.

- **Empirical survival-rate estimation:**  
  Survival rates can be estimated from stock and registration data at different years and aggregation levels, including country-level, powertrain-level, or combined country–powertrain groupings.

- **CSP fitting and stock modelling:**  
  The framework fits cumulative survival probability curves and combines them with new registration data to estimate future vehicle stock.

- **Reusable and extensible design:**  
  The model can be coupled with external transportation models or scenario datasets, enabling applications beyond the default European passenger-car case.

- **Research-oriented analysis workflows:**  
  The repository includes example workflows for validation, sensitivity analysis, and comparative scenario exploration based on alternative survival-rate and registration assumptions.

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

Input and output directories are configured through `data.input_path` and `data.output_path`. Input filenames are also configurable through `data.files`. The filenames listed below are therefore default filenames, not fixed requirements.

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

The historical registration period must be sufficiently long to represent the configured CSP horizon. The relationship between registration history and `model.csp_available_years` is described in the Configuration reference.

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

Contains vehicle stock resolved by vehicle age and is used to estimate empirical cumulative survival probability (CSP) curves.

For the default country-level survival-rate configuration, the dataset must contain at least:

```text
geo country;vehicle age;number of registered vehicles
```

Additional dimensions are required when survival rates are estimated at a more detailed level. For example, country- and powertrain-specific survival rates require:

```text
geo country;vehicle age;powertrain;number of registered vehicles
```

The required dimensions are determined by `survival_rates.grouping`.

The default filename can be changed through `data.files.stock_by_age`.

##### CSP stock reference year

- Logical input key: `stock_year`
- Default filename: `2_2_A_1_stock_year.csv`

Defines the stock reference year associated with the stock-by-age data used for CSP estimation.

The general CSP reference year can be configured through:

```yaml
model:
  csp_reference_year: 2021
```

However, stock-by-age data for individual countries may originate from neighbouring years such as 2020 or 2022. The `stock_year` dataset identifies the actual stock reference year associated with each country or dataset.

The default filename can be changed through `data.files.stock_year`.

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

#### Optional historical-CSP sensitivity datasets

The historical-CSP sensitivity analysis is used to assess how assumptions about vehicle survival affect the projected vehicle stock.

The empirical survival rates estimated from the current stock-by-age data can be compared with older CSP parameters reported in the literature or, where suitable data are available, with empirical survival rates estimated from an earlier stock reference year.

This allows users to investigate how changes in vehicle survival and fleet turnover over time influence long-term stock projections. 

The corresponding historical-CSP datasets are required only when the historical-CSP sensitivity analysis is enabled.

##### Historical CSP parameters

- Logical input key: `historical_csp_parameters`
- Default filename: `5_1_oguchi_2008_survival_rate_parameters.csv`

Contains historical CSP parameter values used by the historical-CSP sensitivity analysis.

The default filename can be changed through `data.files.historical_csp_parameters`.

##### Historical survival rates

- Logical input key: `historical_survival_rates`
- Default filename: `5_2_held_2016_survival_rates.csv`

Contains historical survival-rate data used by the historical-CSP sensitivity analysis.

The default filename can be changed through `data.files.historical_survival_rates`.

These datasets are required when both the sensitivity-analysis workflow and its historical-CSP component are enabled:

```yaml
model:
  sensitivity_analysis: true
  historical_csp: true
```

They are not required for a basic ZEVAMPY run or for sensitivity analyses that do not use the historical-CSP component.

### Configuration file
`config.yaml` is the main user-facing configuration file for ZEVAMPY. It controls input and output paths, selected countries and powertrains, simulation years, Cumulative Survival Probability (CSP) settings, optional validation and sensitivity-analysis workflows, and survival-rate grouping.

A complete example configuration file is provided with the default ZEVAMPY example dataset.

#### Configuration reference

The main ZEVAMPY settings are defined in `config.yaml`.

```yaml
data:
  input_path: inputs
  output_path: outputs

  files:
    country_clusters: 0_country_clusters.csv
    registration_shares: 1_1_new_registrations_by_fuel_type_clusters.csv
    historical_registrations: 1_2_A_2_historical_new_registrations_data_passenger_cars.csv
    projected_registrations: 1_3_new_registrations_projected.csv
    stock_by_age: 2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv
    stock_year: 2_2_A_1_stock_year.csv
    validation_registration_shares: 4_1_eafo_ev_new_registration_shares.csv
    validation_stock_shares: 4_2_eafo_ev_stock_shares.csv
    historical_csp_parameters: 5_1_oguchi_2008_survival_rate_parameters.csv
    historical_survival_rates: 5_2_held_2016_survival_rates.csv

model:
  start_new_registration_year: 1970
  first_stock_year: 2014
  end_year: 2050
  csp_reference_year: 2021
  csp_available_years: 45
  historical_validation: false
  sensitivity_analysis: false
  historical_csp: false

geography:
  countries:
  use_clusters: true

powertrains:

survival_rates:
  grouping:
    - geo country
```

##### Data settings

| Setting | Default | Description |
|---|---|---|
| `data.input_path` | `inputs` | Directory containing the CSV input datasets. The path can also be overridden from the command line using `--input`. |
| `data.output_path` | `outputs` | Directory in which generated CSV files and figures are stored. The path can also be overridden from the command line using `--output`. |
| `data.files` | ZEVAMPY default filenames | Maps each logical input dataset to its CSV filename. Users may override individual filenames. Entries that are omitted fall back to the corresponding default filename. |

The following keys can be configured under `data.files`:
 - `country_clusters`
 - `registration_shares`
 - `historical_registrations`
 - `projected_registrations`
 - `stock_by_age`
 - `stock_year`
 - `validation_registration_shares`
 - `validation_stock_shares`
 - `historical_csp_parameters`
 - `historical_survival_rates`
 
Only filenames that differ from the defaults need to be specified. Unspecified filenames automatically fall back to the corresponding ZEVAMPY default filename.
  
##### Model years and CSP settings

| Setting | Default | Description |
|---|---|---|
| `model.start_new_registration_year` | `1970` | First year of historical new-registration data considered when reconstructing vehicle cohorts and calculating stock. Earlier start years provide information for older vehicle cohorts. |
| `model.first_stock_year` | `2014` | First year for which vehicle stock is calculated and included in the model output. |
| `model.end_year` | Last year available in projected registrations | Final year of the stock simulation. In the default European example this is explicitly set to `2050`. |
| `model.csp_reference_year` | `2021` | Reference year associated with the empirical cumulative survival probability (CSP) data used for stock modelling. Country-specific stock reference years can be provided through the `stock_year` input dataset. |
| `model.csp_available_years` | `45` | Number of vehicle-age years represented by the CSP curve and therefore the maximum survival horizon considered when calculating surviving vehicle cohorts. |

The available registration history must be long enough to cover the configured CSP horizon. ZEVAMPY therefore requires:

```text
(first_stock_year - start_new_registration_year) + 1 >= csp_available_years 
```

For example, the default configuration uses registrations from 1970, starts the stock calculation in 2014, and represents 45 years of the CSP curve. 

A value of approximately 45 years is recommended for passenger-car applications. If `csp_available_years` is set below 45, ZEVAMPY issues a warning because truncating the survival curve can omit older surviving vehicle cohorts and consequently underestimate absolute vehicle stock.

##### Optional analysis settings

| Setting | Default | Description |
|---|---|---|
| `model.historical_validation` | `false` | Enables comparison of modelled historical stock and stock shares with external historical validation data. Additional validation input datasets are required when enabled. |
| `model.sensitivity_analysis` | `false` | Enables the optional sensitivity-analysis workflow. |
| `model.historical_csp` | `false` | Enables the historical-CSP component of the sensitivity analysis. This option is relevant when `sensitivity_analysis` is enabled and requires the corresponding historical CSP input datasets. |

These optional analyses are disabled in the basic configuration. Their required input datasets and generated outputs are described separately below.

##### Geography settings

| Setting | Default | Description |
|---|---|---|
| `geography.countries` | EU-27 + Norway | Countries included in the simulation. If the list is empty, ZEVAMPY uses its predefined European country set. Countries that are not available in the supplied input data are omitted. Custom countries that are not part of the default set must be explicitly listed in `geography.countries`. |
| `geography.use_clusters` | `true` | Determines whether the country-cluster mapping is used for projected powertrain registration shares. When enabled, the configured `country_clusters` input file is required. When disabled, an available cluster file is ignored. |

A custom country selection can be provided as:
```yaml
geography:
  countries:
    - Germany
    - France 
  use_clusters: true
```

If `countries` is left empty, the predefined default country set consists of the EU-27 countries and Norway.

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

A subset can be specified explicitly: 
```yaml
powertrains:
  - BEV
  - Gasoline
  - Diesel
```
Selected powertrains must exist in the corresponding input data.

When only a subset of the available powertrains is selected, the remaining registration shares are represented by the residual category `Rest of powertrains`. For stock-by-age data with powertrain-specific survival rates, non-selected powertrains are likewise aggregated into this residual category.

Custom powertrain categories that are not part of the default set must be explicitly listed in `powertrains`.

##### Survival-rate grouping

`survival_rates.grouping` defines the dimensions for which empirical survival rates and CSP curves are estimated.

The default configuration estimates one survival curve per country:

```yaml
survival_rates:
  grouping:
    - geo country
```

Country- and powertrain-specific survival rates can instead be estimated with:

```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```
Every dimension listed under `survival_rates.grouping` must also be available in the stock-by-age input dataset.

For country-level survival rates, the stock-by-age input data must include at least:

```text
geo country;vehicle age;number of registered vehicles
```

For country- and powertrain-specific survival rates, the stock-by-age input data must include at least:

```text
geo country;vehicle age;powertrain;number of registered vehicles
```

If the configured grouping requires a dimension that is not available in the stock-by-age dataset, ZEVAMPY raises an input-validation error before the model calculation proceeds.

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
  - Diesel

model:
  start_new_registration_year: 1970
  first_stock_year: 2014
  end_year: 2050
  csp_reference_year: 2021
  csp_available_years: 45
  historical_validation: false
  historical_csp: false
  sensitivity_analysis: true

survival_rates:
  grouping:
    - geo country
```
To estimate survival rates by both country and powertrain, use:
```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```
This requires stock-by-age input data that also contains a `powertrain` column.

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

Input validation does not calculate vehicle stock, generate figures, perform historical model validation, or run sensitivity analyses.

#### 🚀 Quick start example

A minimal runnable example is available in:

[`examples/minimal_example/`](https://github.com/gabrielmoringmartinez/zevampy/tree/main/examples/minimal_example)

You can download the example inputs and configuration files directly from the repository and run:

```bash
zevampy --config config.yaml
```


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
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSES/MIT.txt)

This project is REUSE compliant and licensed under multiple open licenses depending on content type:

- **Source code, tests, configuration files, and synthetic example/test data**: [MIT License](LICENSES/MIT.txt)
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
