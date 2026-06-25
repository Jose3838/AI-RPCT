from __future__ import annotations

from pathlib import Path

from builders.registry_builder import write_registry

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

def main():
    write_registry(
        rows=ROWS,
        columns=COLUMNS,
        registry_name="feature_store",
        warehouse_group="feature_store",
        label="feature records",
    )


if __name__ == "__main__":
    main()
