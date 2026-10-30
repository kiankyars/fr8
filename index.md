---
title: Cheap intelligence, scarce infrastructure
description: Four figures testing the case for owning the infrastructure behind cheap intelligence.
---

fr8 is bullish on the future of compute. In a future where intelligence is abundant and cheap, the durable advantage is owning the means of production.
{: .thesis }

The quantitative case has four links: cheaper capability, greater physical demand, scarce capacity, and returns to owners. The evidence supports the first three to different degrees. The fourth depends on what is owned, what it costs, and how long it remains productive.

## 1. Intelligence gets cheaper

The relevant price is the cost of achieving a fixed result. Epoch's September 2026 analysis estimates that this cost fell roughly **13-fold per year** across its selected benchmarks since 2023. Figure 1 shows the cheapest observed configurations at three fixed performance thresholds. These are benchmark results; they do not measure the cost of every useful real-world task.

[![Figure 1: Cost per question at fixed benchmark performance, in US dollars on a logarithmic scale.](figures/01-inference-cost.svg)](figures/01-inference-cost.svg)

**Figure 1.** Cost records at fixed, chance-adjusted accuracy. Each series represents a different task, so their price levels are not directly comparable. A 75% adjusted GPQA score corresponds to 81.25% raw accuracy. [Source](https://epoch.ai/publications/the-plunging-price-of-thought) · [Data and method](sources.html#figure-1)
{: .caption }

## 2. The physical footprint grows

Cheaper output can coexist with more infrastructure. The IEA estimates that global data-centre electricity consumption reached **485 TWh in 2025**. Its central projection reaches **945 TWh in 2030** in the chart data. The IEA separately reports that electricity consumption by AI-focused data centres grew **50% in 2025**. Increasing usage and more demanding tasks can outweigh efficiency improvements; these aggregate series do not establish how much growth lower prices caused.

[![Figure 2: Global data-centre electricity demand, with historical estimates separated from the IEA central projection.](figures/02-demand.svg)](figures/02-demand.svg)

**Figure 2.** All data centres, including non-AI workloads. Dashed values are projections; the shaded scenario range is not a confidence interval. Electricity measures the physical footprint, not useful computation. [Source chart](https://www.iea.org/data-and-statistics/charts/electricity-consumption-by-data-centres-2020-2035) · [Data and method](sources.html#figure-2)
{: .caption }

## 3. New supply has not eliminated scarcity

In CBRE's eight primary North American data-centre markets, reported inventory rose from **5.17 GW at the end of 2023 to 10.90 GW in mid-2026**, while vacancy fell from **3.7% to 1.4%**. This is evidence of a tight leasing market despite substantial construction. It does not show that every proposed site will be needed, or that today's scarcity will persist through another building cycle.

[![Figure 3: Data-centre inventory and vacancy in CBRE's eight primary North American markets.](figures/03-scarcity.svg)](figures/03-scarcity.svg)

**Figure 3.** Inventory and vacancy describe leasable data-centre capacity. Vacancy is not GPU utilization or electrical load. Geography and the ability to deliver power matter; these eight markets are not the global market. [Source](https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026) · [Data and method](sources.html#figure-3)
{: .caption }

## 4. Ownership must survive the economics

Scarcity only helps an owner if revenue covers operating costs, capital recovery, and the required return. Figure 4 holds starting economics constant and varies rental-price erosion and productive life. With flat prices, the illustrative five-year asset needs **59% utilization** to recover its cost and earn 10%; the three-year asset needs **86%**. These are model outputs, not observed returns.

[![Figure 4: A sensitivity analysis of infrastructure ownership economics under different utilization and pricing assumptions.](figures/04-ownership.svg)](figures/04-ownership.svg)

**Figure 4.** All inputs are assumptions. Curves give the minimum utilization required to clear a 10% return; values above 100% are infeasible. Early retirement is allowed, so longer physical life stops helping when continued operation becomes uneconomic. [Inputs and method](sources.html#figure-4)
{: .caption }

The strongest version of the thesis is ownership of capacity that stays useful and costly to replicate: deliverable power, suitable sites, and infrastructure with durable customer demand. GPUs, buildings, grid access, and generation have different replacement cycles and economics. Growing demand supports investigating them; it does not establish attractive returns at any purchase price.

The thesis weakens if efficiency overtakes usage growth, new supply removes scarcity, or falling prices and replacement spending absorb the owner's cash flow. The remaining work is to establish which assets retain an advantage under those conditions.

*Sources checked 30 October 2026. [Sources, assumptions, and reproduction instructions](sources.html).*
