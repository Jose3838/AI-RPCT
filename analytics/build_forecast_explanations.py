from __future__ import annotations

import csv
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "forecast_engine_v1_output.csv"

COLUMNS = [
    "explanation_id",
    "forecast_id",
    "primary_reason",
    "secondary_reason",
    "governance_note",
]


def load_rows():
    with INPUT_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_reason(signal: str):
    if signal == "stable_supply_signal":
        return (
            "High availability observed",
            "Capacity currently available",
        )

    if signal == "capacity_watch_signal":
        return (
            "Limited availability observed",
            "Monitor provider capacity",
        )

    if signal == "capacity_risk_signal":
        return (
            "Unavailable capacity observed",
            "Investigate provider changes",
        )

    return (
        "Unknown signal",
        "Manual review recommended",
    )


def main():
    rows = []

    for idx, row in enumerate(load_rows(), start=1):
        primary, secondary = build_reason(row["rule_based_signal"])

        rows.append(
            {
                "explanation_id": f"exp{idx:06d}",
                "forecast_id": row["forecast_id"],
                "primary_reason": primary,
                "secondary_reason": secondary,
                "governance_note": (
                    "Rule-based explanation only. "
                    "No ML inference. "
                    "No accuracy claim."
                ),
            }
        )

    data_path = ROOT / "data" / "forecast_explanations.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "forecast"
        / "forecast_explanations.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="forecast explanation records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
