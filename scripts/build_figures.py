import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA, FIGURES = ROOT / "data", ROOT / "figures"
PAPER, INK, MUTED = "#000000", "#ffffff", "#8f8f8f"
GREEN, AMBER, BLUE = "#b8ded9", "#d7bda0", "#a9bed7"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#333333", "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": PAPER,
    "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "svg.fonttype": "path", "svg.hashsalt": "fr8-2026-10-30", "text.parse_math": False,
})


def rows(name):
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def style(ax):
    ax.grid(axis="y", color="#222222", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=8)


def save(fig, name, title, description):
    FIGURES.mkdir(exist_ok=True)
    svg_path = FIGURES / f"{name}.svg"
    fig.savefig(svg_path, bbox_inches="tight",
                metadata={"Date": None, "Title": title, "Description": description})
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
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
    ax.set_ylabel("Dollars per question · logarithmic scale", labelpad=12)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.02), frameon=False, fontsize=10)
    style(ax)
    save(fig, "01-inference-cost", "Cheaper benchmark performance",
         "Cost records at fixed chance-adjusted accuracy, in US dollars per benchmark question. Logarithmic y-axis.")


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
        ax.annotate(f"{value:,.0f}", (year, value), xytext=(0, 13), textcoords="offset points",
                    ha="center", color=color, fontweight="bold")
    ax.set_ylabel("Electricity demand · terawatt-hours per year", labelpad=12)
    ax.set_ylim(bottom=0)
    ax.set_xlim(historical[0][0] - 0.3, forecast[-1][0] + 0.3)
    ax.set_xticks([2020, 2025, 2030, 2035])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.legend(loc="upper left", frameon=False)
    style(ax)
    save(fig, "02-demand", "Growing electricity demand",
         "Global data-centre electricity demand: historical estimates and the IEA central projection in terawatt-hours per year.")


def scarcity():
    records = rows("figure3_capacity_vacancy.csv")
    dates = [datetime.fromisoformat(r["period_end"]) for r in records]
    labels = [date.strftime("%B\n%Y") for date in dates]
    capacity = [float(r["inventory_mw"]) / 1000 for r in records]
    vacancy = [float(r["vacancy_pct"]) for r in records]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"wspace": 0.32})
    axes[0].bar(dates, capacity, color=GREEN, width=95)
    axes[0].set_title("Inventory · gigawatts", loc="left", pad=18)
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
    save(fig, "03-scarcity", "Supply and scarcity",
         "Reported data-centre inventory and vacancy in eight primary U.S. markets, H2 2023 through H1 2026.")


def hardware_longevity():
    events = {row["event_id"]: row for row in rows("figure4_hardware_longevity.csv")}
    introduction = events["architecture_introduced"]
    disclosure = events["renewal_disclosed"]
    endpoint = events["contract_endpoint"]
    start, renewal, end = [int(event["event_year"]) for event in (introduction, disclosure, endpoint)]
    term = int(disclosure["contract_term_years"])

    fig, ax = plt.subplots(figsize=(10, 3.0))
    ax.plot([start, renewal], [0, 0], color="#555555", linewidth=3, solid_capstyle="butt")
    ax.plot([renewal, end], [0, 0], color=GREEN, linewidth=8, solid_capstyle="butt")
    for event, year, color in [(introduction, start, MUTED), (disclosure, renewal, GREEN), (endpoint, end, GREEN)]:
        ax.scatter(year, 0, s=95, color=color, edgecolor=PAPER, linewidth=1.5, zorder=3)
        ax.annotate(event["label"], (year, 0), xytext=(0, 28), textcoords="offset points",
                    ha="center", va="bottom", color=color, fontsize=11)
        ax.annotate(str(year), (year, 0), xytext=(0, -22), textcoords="offset points",
                    ha="center", va="top", color=color, fontsize=13, fontweight="bold")
    ax.text((renewal + end) / 2, -0.55,
            f"{term}-year renewal\nAt typical 1-year pricing", ha="center", va="top",
            color=GREEN, fontsize=11, linespacing=1.5)
    ax.set_xlim(start - 0.9, end + 1.0)
    ax.set_ylim(-1.0, 0.8)
    ax.axis("off")
    save(fig, "04-ownership", "A100 architecture and contract timeline",
         "A100 architecture introduced in 2020; a three-year renewal disclosed in 2026 extends into 2029. "
         "The highlighted interval is a year-level illustration, not exact contract dates or the age of individual GPUs.")


if __name__ == "__main__":
    inference_cost()
    demand()
    scarcity()
    hardware_longevity()
