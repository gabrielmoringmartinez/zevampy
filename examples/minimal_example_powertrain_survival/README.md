<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Powertrain-specific survival example

This example demonstrates ZEVAMPY for one synthetic country using **country- and powertrain-specific survival rates**. Separate survival assumptions are provided for the complete `Total` fleet, BEV, and Gasoline vehicles.

The survival grouping is:

```yaml
survival_rates:
  grouping:
    - geo country
    - powertrain
```

The survival inputs therefore contain the groups:

- `Example Country / Total`
- `Example Country / BEV`
- `Example Country / Gasoline`

`Total` represents the complete fleet. Its survival curve is applied to total registrations to calculate total vehicle stock, which is used as the denominator of the BEV and Gasoline stock shares.

`Total` is **not** included in the registration-share input and is **not** listed under `powertrains` in the configuration. The BEV and Gasoline registration shares do not need to sum to 1 because the remaining technologies are represented implicitly in the independently modelled total fleet.

The example contains three ready-to-run configurations:

- `config.yaml` — derives empirical survival rates from age-resolved stock data (`source: stock_by_age`).
- `config_empirical.yaml` — fits CSP curves from pre-calculated empirical survival rates (`source: empirical`).
- `config_parameters.yaml` — generates CSP curves directly from supplied fitted parameters (`source: parameters`).

## Run the example

Open a terminal in this directory and run one of:

```bash
python -m zevampy.cli --config config.yaml
python -m zevampy.cli --config config_empirical.yaml
python -m zevampy.cli --config config_parameters.yaml
```

To validate an input configuration without running the stock model:

```bash
python -m zevampy.cli --config config.yaml --validate-inputs
```

Generated model outputs are written to `outputs/`.

The input data and survival assumptions are synthetic. They are designed to illustrate the powertrain-specific survival workflow and the independent `Total` fleet denominator.
