<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR), Gabriel Möring-Martínez
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Changelog

All notable changes to this project will be documented in this file, following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and semantic versioning.

## [Unreleased]

- Improvements, bug fixes or planned features will be listed here before the next release.

## [1.2.5] – 2026-05-13

### Added

- Added command-line interface (CLI) support for running ZEVAMPY through configuration files
- Added YAML-based configuration workflow for defining modelling assumptions, input paths, and projection settings
- Added minimal runnable example for external users
- Added improved installation and PyPI usage documentation
- Added reusable workflow documentation for adapting ZEVAMPY to new regions, vehicle categories, and powertrain classifications
- Added improved validation messages and optional input-file guidance
- Added updated JOSS paper draft reflecting the generalized ZEVAMPY framework structure

### Changed

- Refactored documentation and README to emphasize reusable framework capabilities beyond the default European passenger-car application
- Improved testing workflows and output validation
- Improved package metadata and PyPI readiness
- Improved configuration guidance and example configuration structure
- Improved terminology and software structure for broader transportation-modelling applications

### Fixed

- Fixed optional validation and sensitivity-analysis file handling
- Fixed multiple documentation inconsistencies and outdated references
- Fixed badge and repository references after repository renaming


## [1.1.2] – 2025-07-28

### Added

- Added GitHub Actions workflow `.github/workflows/draft-pdf.yml` to automatically build the paper PDF
- Now fully compliant with all JOSS criteria for submission

## [1.1.1] – 2025-07-28

### Fixed

- Corrected changelog comparison links
- Marked as JOSS-ready patch release

## [1.1.0] – 2025-07-28

### Added

- **Automated CI/CD testing** with `test.yml`, including:
  - Scenario runs with minimal data (single country, fewer years)
  - Checks for required inputs and expected outputs
  - Other checks
- **REUSE compliance improvements**:
  - .license files added to input data, figures, and other files
  - Compliance badge added
- **JOSS-ready submission**:
  - `paper.md` created, with summary, statement of need, references
- **Citation metadata**:
  - `citation.cff` added for standard citation support
  - License section and license badges added to README
- **Documentation improvements**:
  - Updated installation instructions with tested `pyenv` and WSL flow
  - Added `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
  - `.python-version` added for `pyenv` auto-switching
- **Badges** for CI status, test coverage, and REUSE/license info

### Changed

- Minor code updates for compatibility with **Python 3.12.6**
- Reduced future warnings during execution
- Removed example output files from the repository for cleanliness

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

[Unreleased]: https://github.com/gabrielmoringmartinez/EU-ZEVAM
[1.0.0]: https://github.com/gabrielmoringmartinez/EU-ZEVAM/tree/v1.0.0
[1.1.0]: https://github.com/gabrielmoringmartinez/EU-ZEVAM/tree/v1.1.0
[1.1.1]: https://github.com/gabrielmoringmartinez/EU-ZEVAM/tree/v1.1.1
[1.1.2]: https://github.com/gabrielmoringmartinez/EU-ZEVAM/tree/v1.1.2

