from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "entity_id",
    "vendor",
    "product_name",
    "architecture",
    "launch_year",
    "compute_api",
    "status",
    "source_id",
]

ROWS = [
    {
        "entity_id": "gpu_nvidia_tesla_k80",
        "vendor": "NVIDIA",
        "product_name": "Tesla K80",
        "architecture": "Kepler",
        "launch_year": "2014",
        "compute_api": "CUDA",
        "status": "historical",
        "source_id": "nvidia_products",
    },
    {
        "entity_id": "gpu_nvidia_v100",
        "vendor": "NVIDIA",
        "product_name": "Tesla V100",
        "architecture": "Volta",
        "launch_year": "2017",
        "compute_api": "CUDA",
        "status": "historical",
        "source_id": "nvidia_products",
    },
    {
        "entity_id": "gpu_nvidia_a100",
        "vendor": "NVIDIA",
        "product_name": "A100",
        "architecture": "Ampere",
        "launch_year": "2020",
        "compute_api": "CUDA",
        "status": "historical",
        "source_id": "nvidia_products",
    },
    {
        "entity_id": "gpu_nvidia_h100",
        "vendor": "NVIDIA",
        "product_name": "H100",
        "architecture": "Hopper",
        "launch_year": "2022",
        "compute_api": "CUDA",
        "status": "current",
        "source_id": "nvidia_products",
    },
    {
        "entity_id": "gpu_nvidia_b200",
        "vendor": "NVIDIA",
        "product_name": "B200",
        "architecture": "Blackwell",
        "launch_year": "2024",
        "compute_api": "CUDA",
        "status": "current",
        "source_id": "nvidia_products",
    },
]


def write_csv(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():

    data_path = ROOT / "data" / "nvidia_historical_gpu_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "nvidia"
        / "nvidia_historical_gpu_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} NVIDIA GPU records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
