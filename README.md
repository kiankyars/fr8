# fr8

[Read the memo](https://kiankyars.github.io/fr8/). Edit [index.md](index.md) to update the page.

## Figure 1

Fixed benchmark performance. [Epoch AI — Luke Emberson and David Roodman](https://epoch.ai/publications/the-plunging-price-of-thought) · [Data](data/figure1_cost_records.csv).

## Figure 2

Global electricity consumption for all data centres; 2026–2035 values are projections. [International Energy Agency (IEA)](https://www.iea.org/data-and-statistics/charts/electricity-consumption-by-data-centres-2020-2035) · [Data](data/figure2_electricity.csv).

## Figure 3

Inventory and vacancy in eight United States markets. [Data and reports from Coldwell Banker Richard Ellis (CBRE)](data/figure3_capacity_vacancy.csv). Vacancy measures leasing availability.

## Hardware evidence

A100 introduction and contract renewal. [Data and primary sources](data/hardware_longevity.csv). Evidence supporting section 4; generation age does not establish individual chips' operating ages.

## Reproduce

```sh
python3 -m venv .venv
.venv/bin/python -m pip install matplotlib==3.10.7
.venv/bin/python scripts/prepare_data.py
.venv/bin/python scripts/build_figures.py
.venv/bin/python scripts/verify.py
```

[Provenance and hashes](data/figure1_figure2_sources.json). Epoch and IEA data and adapted figures retain [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Other sources, fr8.so styling and brand assets, and bundled fonts retain their original rights and licenses.
