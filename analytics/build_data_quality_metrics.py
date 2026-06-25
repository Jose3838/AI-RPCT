from __future__ import annotations

import csv
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

DATASETS = [
    "feature_store.csv",
    "forecast_dataset.csv",
    "forecast_engine_v1_output.csv",
    "forecast_explanations.csv",
]

COLUMNS = [
    "dataset",
    "row_count",
    "column_count",
    "status",
]


def metrics(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return (
        len(rows),
        len(reader.fieldnames or []),
    )


def main():
    rows = []

    for dataset in DATASETS:
        path = ROOT / "data" / dataset

        row_count, column_count = metrics(path)

        rows.append(
            {
                "dataset": dataset,
                "row_count": str(row_count),
                "column_count": str(column_count),
                "status": "ok",
            }
        )

    data_path = ROOT / "data" / "data_quality_metrics.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "metadata"
        / "data_quality_metrics.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="data quality metric records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
