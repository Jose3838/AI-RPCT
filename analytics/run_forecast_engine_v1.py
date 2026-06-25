from __future__ import annotations

import csv
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "forecast_dataset.csv"

COLUMNS = [
    "forecast_id",
    "forecast_record_id",
    "provider_id",
    "entity_id",
    "rule_based_signal",
    "forecast_class",
    "confidence_level",
    "governance_status",
    "notes",
]


def load_forecast_dataset():
    with INPUT_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify(row):
    capacity_status = row["capacity_status"]
    availability_level = row["availability_level"]

    if capacity_status == "available" and availability_level == "high":
        return "stable_supply_signal", "monitor_only"

    if capacity_status == "limited" or availability_level in {"low", "medium"}:
        return "capacity_watch_signal", "watch"

    if capacity_status == "unavailable":
        return "capacity_risk_signal", "watch"

    return "unknown_signal", "monitor_only"


def main():
    input_rows = load_forecast_dataset()

    rows = []

    for idx, row in enumerate(input_rows, start=1):
        signal, forecast_class = classify(row)

        rows.append(
            {
                "forecast_id": f"fcst{idx:06d}",
                "forecast_record_id": row["forecast_record_id"],
                "provider_id": row["provider_id"],
                "entity_id": row["entity_id"],
                "rule_based_signal": signal,
                "forecast_class": forecast_class,
                "confidence_level": "not_applicable",
                "governance_status": "non_production_no_true_labels",
                "notes": "Rule-based prototype. No ML training, no accuracy claim, no production promotion.",
            }
        )

    data_path = ROOT / "data" / "forecast_engine_v1_output.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "forecast"
        / "forecast_engine_v1_output.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="forecast engine v1 output records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
