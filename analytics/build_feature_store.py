from __future__ import annotations

from pathlib import Path

from builders.csv_loader import index_by, load_csv
from builders.csv_writer import (
    print_registry_result,
    write_registry_csv,
)

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "feature_id",
    "provider_id",
    "entity_id",
    "vendor",
    "hardware_type",
    "architecture",
    "software_stack",
    "capacity_status",
    "availability_level",
]

CAPACITY = ROOT / "data" / "historical_capacity_registry.csv"
RELATIONSHIPS = ROOT / "data" / "provider_relationship_registry.csv"
PROVIDERS = ROOT / "data" / "provider_entity_registry.csv"
ACCELERATORS = ROOT / "data" / "unified_accelerator_registry.csv"


def build_features() -> list[dict[str, str]]:
    capacity_rows = load_csv(CAPACITY)
    relationship_index = index_by(load_csv(RELATIONSHIPS), "relationship_id")
    provider_index = index_by(load_csv(PROVIDERS), "entity_id")
    accelerator_index = index_by(load_csv(ACCELERATORS), "entity_id")

    rows: list[dict[str, str]] = []

    for idx, capacity in enumerate(capacity_rows, start=1):
        relationship = relationship_index[capacity["relationship_id"]]
        provider = provider_index[relationship["provider_entity_id"]]
        target_entity_id = relationship["target_entity_id"]

        if target_entity_id not in accelerator_index:
            continue

        accelerator = accelerator_index[target_entity_id]

        rows.append(
            {
                "feature_id": f"feat{idx:06d}",
                "provider_id": provider["provider_id"],
                "entity_id": accelerator["entity_id"],
                "vendor": accelerator["vendor"],
                "hardware_type": accelerator["accelerator_type"],
                "architecture": accelerator["architecture"],
                "software_stack": accelerator["compute_api"],
                "capacity_status": capacity["capacity_status"],
                "availability_level": capacity["availability_level"],
            }
        )

    return rows


def main():
    rows = build_features()

    data_path = ROOT / "data" / "feature_store.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "feature_store"
        / "feature_store.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="feature records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
