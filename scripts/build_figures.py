import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
from ownership import generate as generate_ownership

ROOT = Path(__file__).resolve().parents[1]
DATA, FIGURES = ROOT / "data", ROOT / "figures"
PAPER, INK, MUTED = "#fbfaf7", "#202c35", "#59656d"
GREEN, AMBER, BLUE = "#16625f", "#ad6830", "#426c9d"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#cbd4d6", "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": PAPER,
    "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "svg.fonttype": "path", "svg.hashsalt": "fr8-2026-10-30", "text.parse_math": False,
})


def rows(name):
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def style(ax):
    ax.grid(axis="y", color="#dce2e3", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=8)


def save(fig, name, title, description):
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / f"{name}.svg", bbox_inches="tight",
                metadata={"Date": None, "Title": title, "Description": description})
    fig.savefig(FIGURES / f"{name}.png", dpi=190, bbox_inches="tight",
                metadata={"Title": title, "Description": description})
    plt.close(fig)


def inference_cost():
    records = rows("figure1_cost_records.csv")
    fig, ax = plt.subplots(figsize=(10, 5.4))
    selected = [
        ("GPQA Diamond", 0.75, GREEN, "GPQA Diamond · 75% adjusted"),
        ("AIME (OTIS Mock)", 0.75, AMBER, "AIME (OTIS Mock) · 75% adjusted"),
        ("FrontierMath, tiers 1–3", 0.25, BLUE, "FrontierMath (tiers 1–3) · 25% adjusted"),
    ]
    for benchmark, threshold, color, label in selected:
        series = sorted((r for r in records if r["benchmark"] == benchmark
                         and float(r["threshold_adjusted_accuracy"]) == threshold), key=lambda r: r["date"])
        dates = [datetime.fromisoformat(r["date"]) for r in series]
        costs = [float(r["cost_usd_per_task"]) for r in series]
        ax.step(dates, costs, where="post", color=color, linewidth=2, label=label)
        ax.scatter(dates, costs, color=color, s=20, zorder=3)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylabel("USD per question · logarithmic scale", labelpad=12)
    ax.set_title("The cost of a fixed benchmark score keeps falling", loc="left", pad=70)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.02), frameon=False, fontsize=10)
    style(ax)
    fig.text(0.12, -0.035, "Source: Epoch AI (September 2026). Thresholds use chance-adjusted accuracy; distinct tasks.", color=MUTED, fontsize=9)
    save(fig, "01-inference-cost", "Cheaper benchmark performance",
         "Cost records at fixed chance-adjusted accuracy, in USD per benchmark question. Logarithmic y-axis.")


def demand():
    records = rows("figure2_electricity.csv")
    historical = [(int(r["year"]), float(r["historical_twh"])) for r in records if r["historical_twh"]]
    forecast = [(int(r["year"]), float(r["base_case_twh"])) for r in records if r["base_case_twh"]]
    fig, ax = plt.subplots(figsize=(10, 5.3))
    cutoff = historical[-1][0]
    projected_rows = [r for r in records if r["base_case_twh"]]
    ax.fill_between([cutoff] + [int(r["year"]) for r in projected_rows],
                    [historical[-1][1]] + [float(r["case_low_twh"]) for r in projected_rows],
                    [historical[-1][1]] + [float(r["case_high_twh"]) for r in projected_rows],
                    color=BLUE, alpha=0.12, label="IEA scenario range")
    ax.plot(*zip(*historical), color=GREEN, linewidth=2.5, marker="o", markersize=4, label="Historical estimates")
    projection = [historical[-1]] + [point for point in forecast if point[0] > cutoff]
    ax.plot(*zip(*projection), color=BLUE, linewidth=2.5, linestyle="--", label="IEA central projection")
    for year, value in [historical[-1], next(p for p in forecast if p[0] == 2030)]:
        color = GREEN if year <= cutoff else BLUE
        ax.scatter([year], [value], color=color, zorder=3)
        ax.annotate(f"{value:,.0f} TWh", (year, value), xytext=(0, 13), textcoords="offset points",
                    ha="center", color=color, fontweight="bold")
    ax.set_title("The physical footprint expands", loc="left", pad=25)
    ax.set_ylabel("Global data-centre electricity · TWh/year", labelpad=12)
    ax.set_ylim(bottom=0)
    ax.set_xlim(historical[0][0] - 0.3, forecast[-1][0] + 0.3)
    ax.set_xticks([2020, 2025, 2030, 2035])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.legend(loc="upper left", frameon=False)
    style(ax)
    fig.text(0.12, -0.035, "Source: IEA (2026). All data centres, not AI alone. Projection is a scenario, not an observed outcome.", color=MUTED, fontsize=9)
    save(fig, "02-demand", "Growing electricity demand",
         "Global data-centre electricity demand: historical estimates and the IEA central projection in TWh per year.")


def scarcity():
    records = rows("figure3_capacity_vacancy.csv")
    dates = [datetime.fromisoformat(r["period_end"]) for r in records]
    labels = [r["period"].replace(" ", "\n") for r in records]
    capacity = [float(r["inventory_mw"]) / 1000 for r in records]
    vacancy = [float(r["vacancy_pct"]) for r in records]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"wspace": 0.32})
    fig.suptitle("Capacity more than doubled; vacancy still fell", x=0.12, ha="left", fontsize=15, fontweight="bold", y=1.1)
    fig.text(0.12, 1.01, "CBRE's eight primary U.S. wholesale-colocation markets", color=MUTED, fontsize=11)
    axes[0].bar(dates, capacity, color=GREEN, width=95)
    axes[0].set_title("Inventory · GW", loc="left", pad=18)
    axes[0].set_ylim(0, 12.5)
    for date, value in zip(dates, capacity):
        axes[0].text(date, value + 0.28, f"{value:.2f}", ha="center", fontsize=11, fontweight="bold")
    axes[1].plot(dates, vacancy, color=AMBER, linewidth=2, marker="o", markersize=7)
    axes[1].set_title("Vacancy · % of inventory", loc="left", pad=18)
    axes[1].set_ylim(0, 4.8)
    axes[1].yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    for date, value in zip(dates, vacancy):
        axes[1].text(date, value + 0.2, f"{value:g}%", ha="center", fontsize=11, fontweight="bold")
    for ax in axes:
        ax.set_xticks(dates, labels)
        style(ax)
        ax.tick_params(axis="x", labelsize=9)
    fig.text(0.12, -0.08, "Source: CBRE report snapshots, 2023–26. Vacancy describes leasing, not hardware utilization.", color=MUTED, fontsize=9)
    save(fig, "03-scarcity", "Supply and scarcity",
         "Reported data-centre inventory and vacancy in eight primary U.S. markets, H2 2023 through H1 2026.")


def ownership():
    records = generate_ownership()
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.axhspan(100, 160, color="#dce2e3", alpha=0.5)
    ax.axhline(100, color=MUTED, linewidth=1, linestyle=":")
    for life, color, line in [(3, AMBER, "-"), (5, BLUE, "-"), (10, GREEN, "-"), (20, "#835d8a", "--")]:
        series = [r for r in records if r["maximum_life_years"] == life]
        ax.plot([100 * r["annual_rental_price_change"] for r in series],
                [100 * r["breakeven_utilization"] for r in series],
                label=f"{life}-year maximum life", color=color, linewidth=2.3, linestyle=line)
    ax.text(-28, 148, "Above 100%: cannot recover capital at the required return", fontsize=10, color=MUTED)
    ax.set_title("Long life helps only while cash flows remain valuable", loc="left", pad=54)
    ax.text(0, 1.05, "ILLUSTRATIVE MODEL · required utilization to earn a 10% return", transform=ax.transAxes,
            color=MUTED, fontsize=11)
    ax.set_xlabel("Annual change in realized rental price", labelpad=12)
    ax.set_ylabel("Break-even utilization", labelpad=12)
    ax.set_ylim(0, 160)
    ax.set_xlim(-30, 5)
    ax.set_xticks([-30, -20, -10, 0, 5])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:+g}%" if value else "0%"))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.legend(loc="lower left", frameon=False, fontsize=10, ncol=2)
    style(ax)
    fig.text(0.12, -0.07, "Assumed per $100 invested: year-one revenue $60 and variable cost $10 at full use; fixed cost $3/year.\nZero residual value; early retirement allowed. Single capital cycle. Not observed asset-class returns.",
             fontsize=9, color=MUTED, linespacing=1.65)
    save(fig, "04-ownership", "Conditional ownership economics",
         "Illustrative break-even utilization by annual rental-price change and maximum productive life. Values above 100 percent are infeasible.")


if __name__ == "__main__":
    inference_cost()
    demand()
    scarcity()
    ownership()
