---
title: Sources & methods
description: Source data, definitions, assumptions, and reproduction instructions for the compute memo.
---

[Read the memo](./). Sources were retrieved on **30 October 2026**. Historical estimates, projections, and illustrative calculations are kept distinct. The figures can be downloaded as SVG or PNG; every plotted value is in the linked CSVs.

## Figure 1

**Luke Emberson and David Roodman, Epoch AI, [The plunging price of thought](https://epoch.ai/publications/the-plunging-price-of-thought), 22 September 2026.**

[Clean data](data/figure1_cost_records.csv) · [Original CSV](data/raw/figure1_epoch_cost_records.csv) · [SVG](figures/01-inference-cost.svg) · [PNG](figures/01-inference-cost.png)

The original [Figure 2 dataset](https://raw.githubusercontent.com/droodman/inference-cost/9163c17ee7217b9f09ac51bcc71ed64c18c04bc8/output/slides/Figure%202.csv) is pinned to upstream commit `9163c17ee7217b9f09ac51bcc71ed64c18c04bc8`. All 40 rows are retained; the chart selects GPQA Diamond at 75%, AIME (OTIS Mock) at 75%, and FrontierMath tiers 1–3 at 25% chance-adjusted accuracy.

Costs are USD per benchmark question, including reasoning-token usage. Dates follow the source's model/price-version dates, not evaluation dates. Steps join successive sampled cost records and stop at the last observation. They assume the prior record remains available between observations. No future prices are extrapolated.

Accuracy is adjusted above guessing probability: `(raw score − chance floor) / (1 − chance floor)`. The floors are 0.25 for GPQA, 0.001 for AIME, and zero for FrontierMath. A 75% adjusted GPQA score therefore means 81.25% raw accuracy. Series are different tasks, not equivalent capability levels. Selected benchmarks, model coverage, benchmark overfitting, and the source's budget-truncation method limit generalization to economically useful work. Record prices are neither average customer bills nor supplier production costs.

The memo's 13-fold annual decline comes from the authors' broader statistical analysis; it is not a fitted rate from these three plotted series. Data and adapted figure: **CC BY 4.0**, credited to the authors and Epoch AI.

## Figure 2

**International Energy Agency, [Electricity consumption by data centres, 2020–2035](https://www.iea.org/data-and-statistics/charts/electricity-consumption-by-data-centres-2020-2035), updated 16 April 2026.**

[Clean data](data/figure2_electricity.csv) · [Original CSV](data/raw/figure2_iea_electricity.csv) · [SVG](figures/02-demand.svg) · [PNG](figures/02-demand.png)

The original CSV was extracted from the chart's public `data-chart-csv` HTML attribute without digitizing the image. Units are TWh per year for **all global data centres**. Values through 2025 are historical estimates; 2026–2035 are projections. The source's stacked scenario band is recovered as lower = `Blank`, upper = `Blank + Case range`. This is a scenario range, not a statistical confidence interval. Independent rounding places its upper edge 0.1 TWh below the central case in 2026–2028; the original numbers are preserved.

The exact chart values are 485.1 TWh in 2025 and 945.0 TWh in 2030. The [report summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) gives rounded values of 485 and 950 TWh and separately reports 50% growth in AI-focused data-centre electricity consumption in 2025. That AI-only growth rate is not the scope of the plotted aggregate. Data and adapted figure: **CC BY 4.0**, credited to IEA.

## Figure 3

**CBRE Research, North America Data Center Trends.**

[Data with row-level citations](data/figure3_capacity_vacancy.csv) · [SVG](figures/03-scarcity.svg) · [PNG](figures/03-scarcity.png)

| Reporting period | Inventory, MW | Vacancy | Source publication |
| --- | ---: | ---: | --- |
| H2 2023 | 5,174.1 | 3.7% | [6 March 2024](https://www.cbre.com/insights/reports/north-america-data-center-trends-h2-2023) |
| H2 2024 | 6,922.6 | 1.9% | [26 February 2025](https://www.cbre.com/insights/reports/north-america-data-center-trends-h2-2024) |
| H2 2025 | 9,432.0 | 1.4% | [25 February 2026](https://www.cbre.com/insights/books/north-america-data-center-trends-h2-2025) |
| H1 2026 | 10,903.0 | 1.4% | [27 August 2026](https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026) |

Figures were transcribed from each report's market summary. Inventory is divided by 1,000 to show GW. Period ends represent reporting snapshots, not daily measurements; the last interval is six months. The same eight primary U.S. markets are covered: Northern Virginia, Dallas–Fort Worth, Silicon Valley, Chicago, Phoenix, New York Tri-State, Atlanta, and Hillsboro. The [2023](https://www.cbre.com/press-releases/hillsboros-data-center-inventory-grows-334-since-2020) and [2024](https://www.cbre.com/press-releases/north-american-data-center-construction-hit-new-heights-in-2024-amid-surging-demand) releases enumerate this cohort.

These are successive publication snapshots, not a restated historical panel. Inventory includes AI and non-AI wholesale colocation; vacancy measures unleased capacity, not GPU utilization or metered load. Proposed projects are not counted as operating demand. Rental prices were omitted because the H2 2025 report gives conflicting levels in its summary and pricing section. CBRE retains rights in its reports; only a small factual transcription and original chart are included here.

## Figure 4

**Original illustrative calculation. All numerical inputs below are assumptions, not sourced market estimates.**

[Input assumptions](data/figure4_assumptions.json) · [Calculated values](data/figure4_breakeven.csv) · [SVG](figures/04-ownership.svg) · [PNG](figures/04-ownership.png)

| Input | Assumption |
| --- | ---: |
| Initial investment at time zero | $100 |
| Year-one revenue at full utilization | $60 |
| Annual variable cash cost at full utilization | $10 |
| Annual fixed cash cost | $3 |
| Annual required return | 10% |
| Residual value at retirement | $0 |
| Maximum operating life | 3, 5, 10, or 20 years |
| Annual rental-price change | −30% to +5% |

For constant utilization `u`, annual rental-price change `g`, and operating duration `n`:

```text
Cash flow in year t = u × [60 × (1 + g)^(t − 1) − 10] − 3
NPV = −100 + sum(cash flow_t / 1.10^t), for t = 1 through n
```

The calculation solves `NPV = 0` for utilization for each possible operating duration, then chooses the lowest threshold within the maximum life. Values above 100% mean the investment cannot clear the required return under those assumptions. With flat prices, the thresholds are 86.42%, 58.76%, 38.55%, and 29.49% for 3, 5, 10, and 20 years respectively. At a 30% annual price decline, the longer-life curves converge: retiring after five years minimizes the required utilization, which still exceeds 100%.

Cash flows arrive at year-end. All monetary amounts are in constant purchasing-power dollars; rental-price changes and the 10% required return are real rates. Operating costs stay constant; utilization and the price path are known throughout the scenario. Early retirement has no exit cost and stops operating costs immediately. The model is pre-tax and unlevered; the hurdle rate is not a borrowing rate. It excludes construction delays, utilization ramp-up, retirement liabilities, and later replacement investments. This is one capital-recovery cycle with zero residual value: accounting depreciation is not also deducted as a cash expense.

Identical starting economics isolate the effect of cash-flow duration. The curves do not estimate returns for GPUs, buildings, grid connections, or generation. Asset-specific costs, contracts, and replacement economics are needed to make that comparison. The model establishes conditional thresholds; it does not establish that actual owners earn excess returns.

## Reproduce

From the repository root, using Python 3.13:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/prepare_data.py
.venv/bin/python scripts/build_figures.py
.venv/bin/python scripts/verify.py
```

The scripts use the committed source snapshots and require no live data requests. `prepare_data.py` regenerates the two transformed datasets; CBRE observations are already a source-cited transcription. `build_figures.py` regenerates the model CSV and all four SVG/PNG pairs. Change the explicit model assumptions to test a different case. GitHub Pages renders `index.md` as the single site page. This methods document remains in the repository.

[Machine-readable provenance and hashes](data/figure1_figure2_sources.json) identify the original downloads and transformations. **Third-party data is not relicensed by this repository's CC0 dedication.** Epoch and IEA material retain [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); changes made here are the documented transformations, selection, and redrawing. The original model, prose, and scripts are CC0. No source endorses the memo's interpretation.

The page styling, logo, and favicon are adapted from [fr8.so](https://fr8.so/privacy.html) and retain their original rights. Inter and JetBrains Mono retain their SIL Open Font Licenses.
