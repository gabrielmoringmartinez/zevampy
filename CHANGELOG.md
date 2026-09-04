<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR), Gabriel Möring-Martínez
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Changelog

All notable changes to this project will be documented in this file, following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and semantic versioning.

## [Unreleased]

## [2.0.0] – 2026-09-04

ZEVAMPY 2.0.0 is a major refactoring of the software from its original research-application-oriented implementation into a more reusable and configurable vehicle stock turnover framework. The release introduces a generalized survival-rate architecture, powertrain-specific survival assumptions, an independently modelled total fleet denominator, improved command-line workflows, and substantially expanded testing and documentation.

### Added

- Added three configurable survival-rate input pathways:
  - `stock_by_age`, deriving empirical survival rates from age-resolved vehicle stock data before fitting cumulative survival probability (CSP) curves
  - `empirical`, using user-supplied empirical survival rates before CSP fitting
  - `parameters`, using user-supplied fitted CSP parameters directly
- Added support for survival-rate grouping by:
  - country
  - country and powertrain
- Added powertrain-specific survival assumptions, including dedicated survival curves for `Total` and selected powertrains when country-and-powertrain grouping is used.
- Added an independently modelled `Total` fleet used as the denominator for powertrain stock shares, so explicitly modelled powertrains do not need to exhaustively represent the complete vehicle market.
- Added configurable logical input-file mappings, removing reliance on fixed input filenames.
- Added CLI input validation through `--validate-inputs`.
- Added configurable logging and `--log-level` support.
- Added generic historical validation for a configurable validation powertrain.
- Added a second minimal example demonstrating country-and-powertrain-specific survival assumptions.
- Added direct `pytest` and coverage configuration in `pyproject.toml`.
- Added validation for contiguous stock-by-age sequences before survival-rate fitting.
- Added a root MIT `LICENSE` file alongside REUSE-compliant file-level licensing.
- Added an AI usage disclosure to the JOSS paper.

### Changed

- Refactored the survival-rate configuration into the `survival_rates` section with explicit source, grouping, CSP horizon, and source-specific file settings.
- Refactored stock-share calculation so that total fleet stock is calculated independently from total registrations and selected powertrain stocks are treated as subsets of that fleet.
- Registration shares for explicitly modelled powertrains may now sum to less than one; unmodelled technologies remain implicitly represented within the total fleet.
- Generalized the historical validation workflow to use the configured validation powertrain and the same configured survival assumptions as the main model.
- Standardized generated CSV files to comma-separated values with decimal points while retaining compatibility with legacy input formatting.
- Improved input validation and error messages, including explicit failure when required survival groups are missing.
- Improved CSP fitting and documentation of Weibull and Weibull-Gaussian (WG) distributions and their model-selection logic.
- Updated the CLI, configuration examples, documentation, and model outputs to match the generalized architecture.
- Updated CI to install the project from `pyproject.toml` and run tests directly with `pytest`.
- Updated package and citation metadata for the generalized ZEVAMPY framework.
- Expanded and revised the README and JOSS paper to describe configurable survival sources, grouping, validation, outputs, and reusable workflows.
- Updated synthetic example and test data to reduce application-specific assumptions and terminology.
- Updated project licensing to distinguish MIT-licensed software from documentation, figures, metadata, and source-specific research inputs.

### Removed

- Removed the case-specific sensitivity-analysis workflow from the core software.
- Removed the legacy `Rest of powertrains` stock category.
- Removed deprecated configuration parameters including `csp_reference_year` and `start_new_registration_year`; required historical registration coverage is now derived internally.
- Removed the separate `stock_model_requirements.txt` dependency file in favour of `pyproject.toml` as the authoritative dependency definition.
- Removed the legacy `run_tests.py` testing workflow.

### Fixed

- Fixed historical validation so that the selected validation powertrain is configurable rather than hardcoded.
- Fixed stock-share calculations to use the independently modelled total fleet as the denominator.
- Fixed survival-rate handling for country-and-powertrain groupings and missing required survival groups.
- Fixed output formatting inconsistencies in generated CSV files.
- Fixed stale repository, documentation, CI, and contributor-instruction references.
- Fixed package metadata, citation metadata, and root licensing information for the 2.0.0 release.

## [1.2.5] – 2026-05-13

### Added

- Added command-line interface (CLI) support for running ZEVAMPY through configuration files.
- Added YAML-based configuration workflow for defining modelling assumptions, input paths, and projection settings.
- Added minimal runnable example for external users.
- Added improved installation and PyPI usage documentation.
- Added reusable workflow documentation for adapting ZEVAMPY to new regions, vehicle categories, and powertrain classifications.
- Added improved validation messages and optional input-file guidance.
- Added updated JOSS paper draft reflecting the generalized ZEVAMPY framework structure.

### Changed

- Refactored documentation and README to emphasize reusable framework capabilities beyond the default European passenger-car application.
- Improved testing workflows and output validation.
- Improved package metadata and PyPI readiness.
- Improved configuration guidance and example configuration structure.
- Improved terminology and software structure for broader transportation-modelling applications.

### Fixed

- Fixed optional validation and sensitivity-analysis file handling.
- Fixed multiple documentation inconsistencies and outdated references.
- Fixed badge and repository references after repository renaming.

## [1.1.2] – 2025-07-28

### Added

- Added GitHub Actions workflow `.github/workflows/draft-pdf.yml` to automatically build the paper PDF.
- Now fully compliant with all JOSS criteria for submission.

## [1.1.1] – 2025-07-28

### Fixed

- Corrected changelog comparison links.
- Marked as JOSS-ready patch release.

## [1.1.0] – 2025-07-28

### Added

- **Automated CI/CD testing** with `test.yml`, including:
  - Scenario runs with minimal data (single country, fewer years)
  - Checks for required inputs and expected outputs
  - Other checks
- **REUSE compliance improvements**:
  - `.license` files added to input data, figures, and other files
  - Compliance badge added
- **JOSS-ready submission**:
  - `paper.md` created, with summary, statement of need, references
- **Citation metadata**:
  - `CITATION.cff` added for standard citation support
  - License section and license badges added to README
- **Documentation improvements**:
  - Updated installation instructions with tested `pyenv` and WSL flow
  - Added `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
  - `.python-version` added for `pyenv` auto-switching
- **Badges** for CI status, test coverage, and REUSE/license info

### Changed

- Minor code updates for compatibility with **Python 3.12.6**.
- Reduced future warnings during execution.
- Removed example output files from the repository for cleanliness.

## [1.0.0] – 2025-07-04

### Added

- Initial public release of the **European Passenger Car Stock Model**.
- Python model to project the future European passenger car fleet composition by powertrain until 2050.
- Support for multiple scenarios based on:
  - Empirical survival rates (2008, 2016, 2021)
  - New vehicle registration projections
- Integration of EU-cluster logic (from Möring-Martínez et al., 2024).
- Reference scenario output plots (e.g. BEV stock shares).
- Installation via `requirements.txt` and model execution script.
- Citation and licensing metadata (`CITATION.cff`, `LICENSE.md`).
- Documentation in `README.md`.

---

[Unreleased]: https://github.com/gabrielmoringmartinez/zevampy/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/gabrielmoringmartinez/zevampy/compare/v1.2.5...v2.0.0
[1.2.5]: https://github.com/gabrielmoringmartinez/zevampy/compare/v1.1.2...v1.2.5
[1.1.2]: https://github.com/gabrielmoringmartinez/zevampy/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/gabrielmoringmartinez/zevampy/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/gabrielmoringmartinez/zevampy/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/gabrielmoringmartinez/zevampy/tree/v1.0.0

