from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "software_id",
    "software_stack",
    "vendor",
    "version",
    "release_year",
    "lifecycle_status",
    "source_id",
]

ROWS = [
    {
        "software_id": "sw000001",
        "software_stack": "CUDA",
        "vendor": "NVIDIA",
        "version": "12.3",
        "release_year": "2023",
        "lifecycle_status": "historical",
        "source_id": "cuda_docs",
    },
    {
        "software_id": "sw000002",
        "software_stack": "CUDA",
        "vendor": "NVIDIA",
        "version": "13.0 Update 1",
        "release_year": "2025",
        "lifecycle_status": "historical",
        "source_id": "cuda_docs",
    },
    {
        "software_id": "sw000003",
        "software_stack": "ROCm",
        "vendor": "AMD",
        "version": "7.0",
        "release_year": "2025",
        "lifecycle_status": "current",
        "source_id": "rocm_docs",
    },
    {
        "software_id": "sw000004",
        "software_stack": "oneAPI",
        "vendor": "Intel",
        "version": "2024.2",
        "release_year": "2024",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
    },
    {
        "software_id": "sw000005",
        "software_stack": "SynapseAI",
        "vendor": "Intel",
        "version": "1.20",
        "release_year": "2025",
        "lifecycle_status": "current",
        "source_id": "intel_products",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "unified_software_stack_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "metadata"
        / "unified_software_stack_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} unified software stack records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
