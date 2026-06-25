from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "accelerator_id",
    "hardware_id",
    "entity_id",
    "vendor",
    "accelerator_type",
    "product_family",
    "architecture",
    "compute_api",
    "generation",
    "launch_year",
    "status",
    "source_id",
]

ROWS = [
    {
        "accelerator_id": "acc000001",
        "hardware_id": "hw000001",
        "entity_id": "gpu_amd_instinct_mi100",
        "vendor": "AMD",
        "accelerator_type": "GPU",
        "product_family": "AMD Instinct",
        "architecture": "CDNA",
        "compute_api": "ROCm",
        "generation": "MI100",
        "launch_year": "2020",
        "status": "active",
        "source_id": "amd_products",
    },
    {
        "accelerator_id": "acc000002",
        "hardware_id": "hw000002",
        "entity_id": "gpu_amd_instinct_mi300x",
        "vendor": "AMD",
        "accelerator_type": "GPU",
        "product_family": "AMD Instinct",
        "architecture": "CDNA3",
        "compute_api": "ROCm",
        "generation": "MI300",
        "launch_year": "2023",
        "status": "active",
        "source_id": "amd_products",
    },
    {
        "accelerator_id": "acc000003",
        "hardware_id": "hw000003",
        "entity_id": "gpu_intel_max_1100",
        "vendor": "Intel",
        "accelerator_type": "GPU",
        "product_family": "Intel Data Center GPU Max",
        "architecture": "Ponte Vecchio / Xe-HPC",
        "compute_api": "oneAPI",
        "generation": "Max Series",
        "launch_year": "2023",
        "status": "active",
        "source_id": "intel_products",
    },
    {
        "accelerator_id": "acc000004",
        "hardware_id": "hw000004",
        "entity_id": "gpu_intel_gaudi2",
        "vendor": "Intel",
        "accelerator_type": "AI Accelerator",
        "product_family": "Intel Gaudi",
        "architecture": "Gaudi2",
        "compute_api": "SynapseAI",
        "generation": "Gaudi",
        "launch_year": "2022",
        "status": "active",
        "source_id": "intel_newsroom",
    },
    {
        "accelerator_id": "acc000005",
        "hardware_id": "hw000005",
        "entity_id": "gpu_intel_gaudi3",
        "vendor": "Intel",
        "accelerator_type": "AI Accelerator",
        "product_family": "Intel Gaudi",
        "architecture": "Gaudi3",
        "compute_api": "SynapseAI",
        "generation": "Gaudi",
        "launch_year": "2024",
        "status": "active",
        "source_id": "intel_newsroom",
    },
    {
        "accelerator_id": "acc000006",
        "hardware_id": "hw000006",
        "entity_id": "gpu_nvidia_tesla_k80",
        "vendor": "NVIDIA",
        "accelerator_type": "GPU",
        "product_family": "Tesla",
        "architecture": "Kepler",
        "compute_api": "CUDA",
        "generation": "Kepler",
        "launch_year": "2014",
        "status": "active",
        "source_id": "nvidia_products",
    },
    {
        "accelerator_id": "acc000007",
        "hardware_id": "hw000007",
        "entity_id": "gpu_nvidia_v100",
        "vendor": "NVIDIA",
        "accelerator_type": "GPU",
        "product_family": "Tesla",
        "architecture": "Volta",
        "compute_api": "CUDA",
        "generation": "Volta",
        "launch_year": "2017",
        "status": "active",
        "source_id": "nvidia_products",
    },
    {
        "accelerator_id": "acc000008",
        "hardware_id": "hw000008",
        "entity_id": "gpu_nvidia_a100",
        "vendor": "NVIDIA",
        "accelerator_type": "GPU",
        "product_family": "Data Center",
        "architecture": "Ampere",
        "compute_api": "CUDA",
        "generation": "Ampere",
        "launch_year": "2020",
        "status": "active",
        "source_id": "nvidia_products",
    },
    {
        "accelerator_id": "acc000009",
        "hardware_id": "hw000009",
        "entity_id": "gpu_nvidia_h100",
        "vendor": "NVIDIA",
        "accelerator_type": "GPU",
        "product_family": "Data Center",
        "architecture": "Hopper",
        "compute_api": "CUDA",
        "generation": "Hopper",
        "launch_year": "2022",
        "status": "active",
        "source_id": "nvidia_products",
    },
    {
        "accelerator_id": "acc000010",
        "hardware_id": "hw000010",
        "entity_id": "gpu_nvidia_b200",
        "vendor": "NVIDIA",
        "accelerator_type": "GPU",
        "product_family": "Data Center",
        "architecture": "Blackwell",
        "compute_api": "CUDA",
        "generation": "Blackwell",
        "launch_year": "2024",
        "status": "active",
        "source_id": "nvidia_products",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "unified_accelerator_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "metadata"
        / "unified_accelerator_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} unified accelerator records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
