import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def write(name, records):
    with (DATA / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0])
        writer.writeheader()
        writer.writerows(records)


def prepare():
    with (DATA / "raw/figure1_epoch_cost_records.csv").open(newline="") as handle:
        records = [{
            "benchmark": row["benchmark"],
            "threshold_adjusted_accuracy": row["level"],
            "date": row["date"],
            "model": row["model_label"],
            "cost_usd_per_task": row["cost"],
            "run_adjusted_accuracy": row["acc"],
        } for row in csv.DictReader(handle)]
    write("figure1_cost_records.csv", records)
    records = []
    with (DATA / "raw/figure2_iea_electricity.csv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            historical = row["Historical"] != "null"
            records.append({
                "year": row[""],
                "historical_twh": row["Historical"] if historical else "",
                "base_case_twh": "" if historical else row["Base case"],
                "case_low_twh": "" if historical else row["Blank"],
                "case_high_twh": "" if historical else round(float(row["Blank"]) + float(row["Case range"]), 1),
                "status": "historical estimate" if historical else "projection",
            })
    write("figure2_electricity.csv", records)


if __name__ == "__main__":
    prepare()
