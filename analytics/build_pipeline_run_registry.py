from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "run_id",
    "pipeline_version",
    "run_timestamp_utc",
    "status",
    "datasets_generated",
]

ROWS = [
    {
        "run_id": "run000001",
        "pipeline_version": "1.0",
        "run_timestamp_utc": datetime.now(UTC).isoformat(),
        "status": "success",
        "datasets_generated": "feature_store.csv;forecast_dataset.csv;forecast_engine_v1_output.csv;forecast_explanations.csv",
    },
]


def main():
    data_path = ROOT / "data" / "pipeline_run_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "metadata"
        / "pipeline_run_registry.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=ROWS,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(ROWS),
        label="pipeline run records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
