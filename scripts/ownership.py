import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_assumptions():
    return json.loads((ROOT / "data/figure4_assumptions.json").read_text())


def npv(inputs, utilization, price_change, duration):
    value = -inputs["initial_capex"]
    for year in range(1, duration + 1):
        revenue = inputs["year_one_full_utilization_revenue"] * (1 + price_change) ** (year - 1)
        cash = utilization * (revenue - inputs["annual_full_utilization_variable_cost"]) - inputs["annual_fixed_cost"]
        value += cash / (1 + inputs["discount_rate"]) ** year
    return value + inputs["salvage_value"] / (1 + inputs["discount_rate"]) ** duration


def breakeven(inputs, price_change, maximum_life):
    options = []
    for duration in range(1, maximum_life + 1):
        fixed_npv = npv(inputs, 0, price_change, duration)
        contribution = npv(inputs, 1, price_change, duration) - fixed_npv
        if contribution > 0:
            options.append((-fixed_npv / contribution, duration))
    if not options:
        raise ValueError("No positive operating contribution within the specified asset life")
    utilization, duration = min(options)
    return utilization, duration


def generate():
    inputs = load_assumptions()
    start = inputs["annual_rental_price_change_min"]
    step = inputs["annual_rental_price_change_step"]
    count = round((inputs["annual_rental_price_change_max"] - start) / step) + 1
    records = []
    for life in inputs["maximum_productive_lives_years"]:
        for index in range(count):
            change = round(start + index * step, 6)
            utilization, duration = breakeven(inputs, change, life)
            records.append({
                "maximum_life_years": life,
                "annual_rental_price_change": change,
                "breakeven_utilization": round(utilization, 10),
                "optimal_operating_years": duration,
                "feasible_at_full_utilization": utilization <= 1,
                "status": "illustrative model",
            })
    with (ROOT / "data/figure4_breakeven.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0])
        writer.writeheader()
        writer.writerows(records)
    return records


if __name__ == "__main__":
    generate()
