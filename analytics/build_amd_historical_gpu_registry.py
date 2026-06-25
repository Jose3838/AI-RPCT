from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "gpu_id",
    "vendor",
    "family",
    "architecture",
    "product_name",
    "launch_date",
    "launch_year",
    "market_segment",
    "memory_type",
    "memory_gb",
    "compute_api",
    "status",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

ROWS = [
    {
        "gpu_id": "amd-instinct-mi100",
        "vendor": "AMD",
        "family": "Instinct",
        "architecture": "CDNA",
        "product_name": "AMD Instinct MI100",
        "launch_date": "2020-11-16",
        "launch_year": "2020",
        "market_segment": "Datacenter HPC / AI",
        "memory_type": "HBM2",
        "memory_gb": "32",
        "compute_api": "ROCm",
        "status": "historical_active_reference",
        "source_url": "https://ir.amd.com/news-events/press-releases/detail/981/amd-announces-worlds-fastest-hpc-accelerator-for-scientific-research",
        "source_type": "official_press_release",
        "source_confidence": "high",
        "notes": "Official AMD announcement. No pricing or performance claims stored.",
    },
    {
        "gpu_id": "amd-instinct-mi200-series",
        "vendor": "AMD",
        "family": "Instinct",
        "architecture": "CDNA2",
        "product_name": "AMD Instinct MI200 Series",
        "launch_date": "2021-11-08",
        "launch_year": "2021",
        "market_segment": "Datacenter HPC / AI",
        "memory_type": "HBM2e",
        "memory_gb": "",
        "compute_api": "ROCm",
        "status": "historical_active_reference",
        "source_url": "https://ir.amd.com/news-events/press-releases/detail/1032/new-amd-instinct-mi200-series-accelerators-bring-leadership-hpc-and-ai-performance-to-power-exascale-systems-and-more",
        "source_type": "official_press_release",
        "source_confidence": "high",
        "notes": "Series-level record. Specific SKU details should be expanded only with verified source rows.",
    },
    {
        "gpu_id": "amd-instinct-mi210",
        "vendor": "AMD",
        "family": "Instinct",
        "architecture": "CDNA2",
        "product_name": "AMD Instinct MI210",
        "launch_date": "2022-03-22",
        "launch_year": "2022",
        "market_segment": "Datacenter HPC / AI",
        "memory_type": "",
        "memory_gb": "",
        "compute_api": "ROCm",
        "status": "historical_active_reference",
        "source_url": "https://www.amd.com/en/products/accelerators/instinct/mi200/mi210.html",
        "source_type": "official_product_page",
        "source_confidence": "high",
        "notes": "AMD product page lists launch date and architecture. Memory fields intentionally left blank until registry source is added.",
    },
    {
        "gpu_id": "amd-instinct-mi300x",
        "vendor": "AMD",
        "family": "Instinct",
        "architecture": "CDNA3",
        "product_name": "AMD Instinct MI300X",
        "launch_date": "2023-12-06",
        "launch_year": "2023",
        "market_segment": "Datacenter AI / HPC",
        "memory_type": "HBM3",
        "memory_gb": "",
        "compute_api": "ROCm",
        "status": "historical_active_reference",
        "source_url": "https://www.amd.com/en/newsroom/press-releases/2023-12-6-amd-delivers-leadership-portfolio-of-data-center-a.html",
        "source_type": "official_press_release",
        "source_confidence": "high",
        "notes": "Availability announcement. No benchmark or pricing claim stored.",
    },
]

def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)

def main() -> None:
    data_path = ROOT / "data" / "amd_historical_gpu_registry.csv"
    warehouse_path = ROOT / "warehouse" / "historical" / "amd" / "amd_historical_gpu_registry.csv"
    write_csv(data_path)
    write_csv(warehouse_path)
    print(f"Wrote {len(ROWS)} AMD historical GPU registry rows.")
    print(data_path)
    print(warehouse_path)

if __name__ == "__main__":
    main()
