from __future__ import annotations

from pathlib import Path

from builders.csv_loader import load_csv
from builders.csv_writer import (
    print_registry_result,
    write_registry_csv,
)

ROOT = Path(__file__).resolve().parents[1]

FEATURE_STORE = ROOT / "data" / "feature_store.csv"

COLUMNS = [
    "forecast_record_id",
    "feature_id",
    "provider_id",
    "entity_id",
    "vendor",
    "architecture",
    "software_stack",
    "capacity_status",
    "availability_level",
]


def build_forecast_rows() -> list[dict[str, str]]:
    feature_rows = load_csv(FEATURE_STORE)

    rows: list[dict[str, str]] = []

    for idx, row in enumerate(feature_rows, start=1):
        rows.append(
            {
                "forecast_record_id": f"forecast{idx:06d}",
                "feature_id": row["feature_id"],
                "provider_id": row["provider_id"],
                "entity_id": row["entity_id"],
                "vendor": row["vendor"],
                "architecture": row["architecture"],
                "software_stack": row["software_stack"],
                "capacity_status": row["capacity_status"],
                "availability_level": row["availability_level"],
            }
        )

    return rows


def main():
    rows = build_forecast_rows()

    data_path = ROOT / "data" / "forecast_dataset.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "forecast"
        / "forecast_dataset.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="forecast dataset records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
