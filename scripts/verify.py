import csv
import hashlib
import json
import re
from pathlib import Path

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

for name in ("index.md", "README.md"):
    for target in re.findall(r'\]\(([^)]+)\)', (ROOT / name).read_text()):
        if target.startswith(("https://", "http://", "#")):
            continue
        local = target.split("#")[0]
        if local.endswith(".html"):
            local = local[:-5] + ".md"
        assert (ROOT / local).exists(), (name, target)
assert len(list((ROOT / "figures").glob("*.svg"))) == 3
assert len(re.findall(r'!\[', (ROOT / "index.md").read_text())) == 3
print("PASS: source hashes, cost records, observation/forecast split, and local links")
