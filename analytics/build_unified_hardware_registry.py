from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "hardware_id",
    "entity_id",
    "vendor",
    "product_family",
    "architecture",
    "compute_api",
    "launch_year",
    "status",
    "source_id",
]

ROWS = [
    {
        "hardware_id": "hw000001",
        "entity_id": "gpu_amd_instinct_mi100",
        "vendor": "AMD",
        "product_family": "AMD Instinct",
        "architecture": "CDNA",
        "compute_api": "ROCm",
        "launch_year": "2020",
        "status": "active",
        "source_id": "amd_products",
    },
    {
        "hardware_id": "hw000002",
        "entity_id": "gpu_amd_instinct_mi300x",
        "vendor": "AMD",
        "product_family": "AMD Instinct",
        "architecture": "CDNA3",
        "compute_api": "ROCm",
        "launch_year": "2023",
        "status": "active",
        "source_id": "amd_products",
    },
    {
        "hardware_id": "hw000003",
        "entity_id": "gpu_intel_max_1100",
        "vendor": "Intel",
        "product_family": "Intel Data Center GPU Max",
        "architecture": "Ponte Vecchio / Xe-HPC",
        "compute_api": "oneAPI",
        "launch_year": "2023",
        "status": "active",
        "source_id": "intel_products",
    },
    {
        "hardware_id": "hw000004",
        "entity_id": "gpu_intel_gaudi2",
        "vendor": "Intel",
        "product_family": "Intel Gaudi",
        "architecture": "Gaudi2",
        "compute_api": "SynapseAI",
        "launch_year": "2022",
        "status": "active",
        "source_id": "intel_newsroom",
    },
    {
        "hardware_id": "hw000005",
        "entity_id": "gpu_intel_gaudi3",
        "vendor": "Intel",
        "product_family": "Intel Gaudi",
        "architecture": "Gaudi3",
        "compute_api": "SynapseAI",
        "launch_year": "2024",
        "status": "active",
        "source_id": "intel_newsroom",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "unified_hardware_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "metadata"
        / "unified_hardware_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} unified hardware records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
