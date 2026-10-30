import csv
import hashlib
import json
import math
import re
from pathlib import Path

from ownership import breakeven, load_assumptions, npv

ROOT = Path(__file__).resolve().parents[1]


def read_csv(name):
    with (ROOT / "data" / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


provenance = json.loads((ROOT / "data/figure1_figure2_sources.json").read_text())
for figure in ("figure1", "figure2"):
    for kind in ("raw", "clean"):
        entry = provenance[figure]
        path = ROOT / "data" / entry[f"{kind}_file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry[f"{kind}_file_sha256"], path

records = read_csv("figure1_cost_records.csv")
assert len(records) == 40
groups = {}
for row in records:
    assert float(row["cost_usd_per_task"]) > 0
    assert float(row["run_adjusted_accuracy"]) >= float(row["threshold_adjusted_accuracy"])
    groups.setdefault((row["benchmark"], row["threshold_adjusted_accuracy"]), []).append(row)
for group in groups.values():
    ordered = sorted(group, key=lambda row: row["date"])
    costs = [float(row["cost_usd_per_task"]) for row in ordered]
    assert all(a >= b for a, b in zip(costs, costs[1:]))

records = read_csv("figure2_electricity.csv")
assert [int(row["year"]) for row in records] == list(range(2020, 2036))
for row in records:
    if int(row["year"]) <= 2025:
        assert row["historical_twh"] and not row["base_case_twh"] and row["status"] == "historical estimate"
    else:
        assert row["base_case_twh"] and not row["historical_twh"] and row["status"] == "projection"
        assert float(row["case_low_twh"]) <= float(row["base_case_twh"]) <= float(row["case_high_twh"]) + 0.100001

inputs = load_assumptions()
for life in inputs["maximum_productive_lives_years"]:
    r = inputs["discount_rate"]
    annuity = sum((1 + r) ** -year for year in range(1, life + 1))
    expected = (inputs["initial_capex"] + inputs["annual_fixed_cost"] * annuity - inputs["salvage_value"] * (1 + r) ** -life) / (
        (inputs["year_one_full_utilization_revenue"] - inputs["annual_full_utilization_variable_cost"]) * annuity)
    calculated, _ = breakeven(inputs, 0, life)
    assert math.isclose(calculated, expected, abs_tol=1e-10)

previous_by_life = {}
for row in read_csv("figure4_breakeven.csv"):
    life = int(row["maximum_life_years"])
    change = float(row["annual_rental_price_change"])
    threshold = float(row["breakeven_utilization"])
    duration = int(row["optimal_operating_years"])
    assert 1 <= duration <= life
    assert abs(npv(inputs, threshold, change, duration)) < 1e-6
    assert npv(inputs, threshold * 0.99, change, duration) < 0
    assert npv(inputs, threshold * 1.01, change, duration) > 0
    assert threshold <= previous_by_life.get(life, math.inf) + 1e-9
    previous_by_life[life] = threshold
    for longer in inputs["maximum_productive_lives_years"]:
        if longer > life:
            assert breakeven(inputs, change, longer)[0] <= threshold + 1e-9

for name in ("index.md", "sources.md"):
    for target in re.findall(r'\]\(([^)]+)\)', (ROOT / name).read_text()):
        if target.startswith(("https://", "http://", "#")):
            continue
        local = target.split("#")[0]
        if local.endswith(".html"):
            local = local[:-5] + ".md"
        assert (ROOT / local).exists(), (name, target)
assert len(list((ROOT / "figures").glob("*.svg"))) == 4
assert len(list((ROOT / "figures").glob("*.png"))) == 4
assert len(re.findall(r'!\[', (ROOT / "index.md").read_text())) == 4
print("PASS: source hashes, cost records, observation/forecast split, independent annuity checks, model sensitivity, and local links")
