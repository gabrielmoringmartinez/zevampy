<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Minimal example

This example demonstrates ZEVAMPY for one synthetic country using **country-level survival rates**. One survival curve is fitted for `Example Country` and is applied to the complete `Total` fleet and to the explicitly modelled powertrains, BEV and Gasoline.

The example contains three ready-to-run configurations representing the three supported survival-rate input sources:

- `config.yaml` — derives empirical survival rates from age-resolved stock data (`source: stock_by_age`).
- `config_empirical.yaml` — fits CSP curves from pre-calculated empirical survival rates (`source: empirical`).
- `config_parameters.yaml` — generates CSP curves directly from supplied fitted parameters (`source: parameters`).

All configurations use:

```yaml
survival_rates:
  grouping:
    - geo country
```

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

The input data are synthetic and are intended to demonstrate the ZEVAMPY workflow rather than reproduce a real country.
