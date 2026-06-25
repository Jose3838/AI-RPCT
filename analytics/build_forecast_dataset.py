from __future__ import annotations

from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

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

ROWS = [
    {
        "forecast_record_id": "forecast000001",
        "feature_id": "feat000001",
        "provider_id": "prov000004",
        "entity_id": "gpu_nvidia_h100",
        "vendor": "NVIDIA",
        "architecture": "Hopper",
        "software_stack": "CUDA",
        "capacity_status": "available",
        "availability_level": "high",
    },
    {
        "forecast_record_id": "forecast000002",
        "feature_id": "feat000002",
        "provider_id": "prov000005",
        "entity_id": "gpu_nvidia_a100",
        "vendor": "NVIDIA",
        "architecture": "Ampere",
        "software_stack": "CUDA",
        "capacity_status": "limited",
        "availability_level": "medium",
    },
]


def main():
    data_path = ROOT / "data" / "forecast_dataset.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "forecast"
        / "forecast_dataset.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=ROWS,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(ROWS),
        label="forecast dataset records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
