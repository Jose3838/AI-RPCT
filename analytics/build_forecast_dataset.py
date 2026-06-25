from __future__ import annotations

from pathlib import Path

from builders.csv_loader import load_csv
from builders.registry_builder import write_registry

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


def build_rows() -> list[dict[str, str]]:
    feature_rows = load_csv(FEATURE_STORE)

    rows = []

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
    write_registry(
        rows=build_rows(),
        columns=COLUMNS,
        registry_name="forecast_dataset",
        warehouse_group="forecast",
        label="forecast dataset records",
    )

if __name__ == "__main__":
    main()
