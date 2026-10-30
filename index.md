fr8 is bullish on the future of compute. In a future where intelligence is abundant and cheap, the durable advantage is owning the means of production.
{: .thesis }

## 1. Intelligence gets cheaper

Epoch's September 2026 analysis estimates that this cost fell roughly **13-fold per year** across its selected benchmarks since 2023.

[![Figure 1: Cost per question at fixed benchmark performance.](figures/01-inference-cost.svg)](figures/01-inference-cost.svg)[Source](https://epoch.ai/publications/the-plunging-price-of-thought)

## 2. Jevon's paradox

The IEA estimates that global data-centre electricity consumption will go from **485 TWh in 2025** to **945 TWh in 2030**.

[![Figure 2: Global data-centre electricity demand, with historical estimates separated from the IEA central projection.](figures/02-demand.svg)](figures/02-demand.svg)

**Figure 2.** All data centres, including non-AI workloads. Dashed values are projections; the shaded scenario range is not a confidence interval. Electricity measures the physical footprint, not useful computation. [Source chart](https://www.iea.org/data-and-statistics/charts/electricity-consumption-by-data-centres-2020-2035) · [Data and method](https://github.com/kiankyars/fr8/blob/main/sources.md#figure-2)
{: .caption }

## 3. New supply has not eliminated scarcity

In CBRE's eight primary North American data-centre markets, reported inventory rose from **5.17 GW at the end of 2023 to 10.90 GW in mid-2026**, while vacancy fell from **3.7% to 1.4%**. This is evidence of a tight leasing market despite substantial construction. It does not show that every proposed site will be needed, or that today's scarcity will persist through another building cycle.

[![Figure 3: Data-centre inventory and vacancy in CBRE's eight primary North American markets.](figures/03-scarcity.svg)](figures/03-scarcity.svg)

**Figure 3.** Inventory and vacancy describe leasable data-centre capacity. Vacancy is not GPU utilization or electrical load. Geography and the ability to deliver power matter; these eight markets are not the global market. [Source](https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026) · [Data and method](https://github.com/kiankyars/fr8/blob/main/sources.md#figure-3)
{: .caption }

## 4. Ownership must survive the economics

Scarcity only helps an owner if revenue covers operating costs, capital recovery, and the required return. Figure 4 holds starting economics constant and varies rental-price erosion and productive life. With flat prices, the illustrative five-year asset needs **59% utilization** to recover its cost and earn 10%; the three-year asset needs **86%**. These are model outputs, not observed returns.

[![Figure 4: A sensitivity analysis of infrastructure ownership economics under different utilization and pricing assumptions.](figures/04-ownership.svg)](figures/04-ownership.svg)

**Figure 4.** All inputs are assumptions. Curves give the minimum utilization required to clear a 10% return; values above 100% are infeasible. Early retirement is allowed, so longer physical life stops helping when continued operation becomes uneconomic. [Inputs and method](https://github.com/kiankyars/fr8/blob/main/sources.md#figure-4)
{: .caption }

The strongest version of the thesis is ownership of capacity that stays useful and costly to replicate: deliverable power, suitable sites, and infrastructure with durable customer demand. GPUs, buildings, grid access, and generation have different replacement cycles and economics. Growing demand supports investigating them; it does not establish attractive returns at any purchase price.

The thesis weakens if efficiency overtakes usage growth, new supply removes scarcity, or falling prices and replacement spending absorb the owner's cash flow. The remaining work is to establish which assets retain an advantage under those conditions.

*Sources checked 30 October 2026. [Sources, assumptions, and reproduction instructions](https://github.com/kiankyars/fr8/blob/main/sources.md).*
