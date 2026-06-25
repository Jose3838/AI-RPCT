from __future__ import annotations

import csv
from datetime import datetime, UTC
from pathlib import Path

from builders.csv_writer import (
    print_registry_result,
    write_registry_csv,
)

ROOT = Path(__file__).resolve().parents[1]

FORECAST_OUTPUT = ROOT / "data" / "forecast_engine_v1_output.csv"

COLUMNS = [
    "summary_id",
    "run_timestamp_utc",
    "forecast_output_rows",
    "governance_status",
    "ml_training_allowed",
    "production_promotion_allowed",
]


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def main():
    rows = [
        {
            "summary_id": "forecast_summary_000001",
            "run_timestamp_utc": datetime.now(UTC).isoformat(),
            "forecast_output_rows": str(count_rows(FORECAST_OUTPUT)),
            "governance_status": "non_production_no_true_labels",
            "ml_training_allowed": "false",
            "production_promotion_allowed": "false",
        }
    ]

    data_path = ROOT / "data" / "forecast_run_summary.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "forecast"
        / "forecast_run_summary.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="forecast run summary records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
