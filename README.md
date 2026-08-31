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

#### Required input datasets

At the current stage, ZEVAMPY expects the following filenames inside the folder defined by `data.input_path` in `config.yaml`. The input-folder path can be modified, but the filenames are currently fixed.

##### Country clusters (optional)
- `inputs/0_country_clusters.csv`: 

Defines optional country clusters used to reduce the number of independent registration forecasts required. Countries assigned to the same cluster are assumed to share the same projected powertrain registration shares.

This file is optional and can be disabled in `config.yaml` by setting:

```yaml
geography:
  use_clusters: false
```

---

##### Historical and projected vehicle registrations by powertrain

- `inputs/1_1_new_registrations_by_fuel_type_clusters.csv`

Contains historical and projected vehicle-registration shares by powertrain for the defined countries or clusters.

---

##### Historical total vehicle registrations

- `inputs/1_2_A_2_historical_new_registrations_data_passenger_cars.csv`

Contains historical absolute vehicle-registration numbers by country up to the latest available historical year.

---
##### Projected total vehicle registrations

- `inputs/1_3_new_registrations_projected.csv`

Contains projected total vehicle-registrations for future years up to the selected simulation horizon.

---

##### Stock-by-age datasets

- `inputs/2_1_A_1_age_resolved_data_passenger_car_stock_fleet.csv`

Contains the vehicle stock resolved by vehicle age. This dataset is used to estimate empirical cumulative survival probability (CSP) curves.

The dataset can optionally include additional dimensions such as:
- `geo country`
- `powertrain`

This allows empirical survival rates to be estimated at different aggregation levels.

Meaningful survival-rate estimation and subsequent stock projections require sufficiently high goodness-of-fit values for the fitted CSP curves (e.g., high R² values in `outputs/2_1_optimum_parameters_csp_curves.csv`).

---

##### CSP reference year

- `inputs/2_2_A_1_stock_year.csv`

Defines the reference year associated with the stock-by-age dataset used for CSP estimation.

For example, the configuration file `config.yaml` may define:
```yaml
csp_reference_year: 2021
```
However, some countries may only provide stock-by-age data for neighbouring years such as 2020 or 2022. This file specifies the actual stock-reference year used for each country or dataset during CSP estimation.

---

##### Optional validation and sensitivity-analysis datasets
Files in the default inputs beginning with:
- `4_*`
- `5_*`

are optional and mainly used for:
- historical validation,
- sensitivity analysis,
- and reproduction of the default European case study.

These files are not required for running custom ZEVAMPY applications.

---

### Configuration file
- `config.yaml`

The configuration file acts as the main user interface of ZEVAMPY and controls the complete modelling workflow. It defines:
- input and output paths
- countries or regions
  - If `countries` is left empty, all available countries found in the input datasets are used.
- powertrains
  - If `powertrains` is left empty, all available powertrain categories found in the input datasets are used.
- projection horizon
- Cumulative Survival Probability (CSP) settings
- validation settings
- and optional sensitivity-analysis options.

A complete example configuration file is provided with the default ZEVAMPY example dataset.

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
---

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
```bash
pip install -e .
```
If you keep a separate requirements file for development tools, install it as well:
```bash
pip install -r stock_model_requirements.txt
```
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
- Countries or regions by changing the geography.countries section in config.yaml
- Powertrains by changing the powertrains list
- Projection horizon by changing model.end_year
- Input and output folders through the data section
- Survival-rate grouping through survival_rates.grouping

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

This repository includes unit tests to ensure consistent and reliable behavior of ZEVAMPY.

To run all tests:

```bash
python run_tests.py
```
This will:

- Discover and execute all tests in the `tests/` folder using `pytest`
- Print outputs to the terminal
- Save generated model outputs in the `outputs/` folder
- Exit with a status code indicating success or failure

### Optional: Run a specific test

To run an individual test, modify the `run_tests.py` script. For example:
```
# Uncomment and adapt one of the lines below in run_tests.py

# Syntax:
# sys.exit(pytest.main(["tests/test_file.py::test_function"]))

# Example:
# sys.exit(pytest.main(["tests/test_4_model_runs_on_minimal_input_single_country.py::test_model_runs_on_minimal_input"]))
```
**Note:** The tests assume the Python environment is already set up and all required dependencies are installed:
```bash
pip install -r stock_model_requirements.txt
```
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
