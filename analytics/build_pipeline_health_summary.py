from __future__ import annotations

import csv
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

INPUTS = [
    "feature_store.csv",
    "forecast_dataset.csv",
    "forecast_engine_v1_output.csv",
    "forecast_explanations.csv",
]

COLUMNS = [
    "dataset",
    "row_count",
    "status",
]


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def main():
    rows = []

    for dataset in INPUTS:
        path = ROOT / "data" / dataset

        rows.append(
            {
                "dataset": dataset,
                "row_count": str(count_rows(path)),
                "status": "ok" if path.exists() else "missing",
            }
        )

    data_path = ROOT / "data" / "pipeline_health_summary.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "metadata"
        / "pipeline_health_summary.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="pipeline health records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
