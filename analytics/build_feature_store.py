from __future__ import annotations

from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
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

ROWS = [
    {
        "feature_id": "feat000001",
        "provider_id": "prov000004",
        "entity_id": "gpu_nvidia_h100",
        "vendor": "NVIDIA",
        "hardware_type": "GPU",
        "architecture": "Hopper",
        "software_stack": "CUDA",
        "capacity_status": "available",
        "availability_level": "high",
    },
    {
        "feature_id": "feat000002",
        "provider_id": "prov000005",
        "entity_id": "gpu_nvidia_a100",
        "vendor": "NVIDIA",
        "hardware_type": "GPU",
        "architecture": "Ampere",
        "software_stack": "CUDA",
        "capacity_status": "limited",
        "availability_level": "medium",
    },
]

data_path = ROOT / "data" / "feature_store.csv"

warehouse_path = (
    ROOT
    / "warehouse"
    / "feature_store"
    / "feature_store.csv"
)


def main():
    write_registry_csv(
        columns=COLUMNS,
        rows=ROWS,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(ROWS),
        label="feature records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
