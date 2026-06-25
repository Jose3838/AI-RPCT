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
        "gpu_id": "intel-data-center-gpu-max-1100",
        "vendor": "Intel",
        "family": "Data Center GPU Max",
        "architecture": "Ponte Vecchio / Xe-HPC",
        "product_name": "Intel Data Center GPU Max 1100",
        "launch_date": "2023-Q2",
        "launch_year": "2023",
        "market_segment": "Datacenter HPC / AI",
        "memory_type": "HBM2e",
        "memory_gb": "48",
        "compute_api": "oneAPI",
        "status": "historical_active_reference",
        "source_url": "https://www.intel.com/content/www/us/en/products/sku/232876/intel-data-center-gpu-max-1100/specifications.html",
        "source_type": "official_product_page",
        "source_confidence": "high",
        "notes": "Intel product specification lists launch date as Q2'23. Quarter-level date retained; no day-level date inferred.",
    },
    {
        "gpu_id": "intel-gaudi2",
        "vendor": "Intel",
        "family": "Gaudi",
        "architecture": "Gaudi2",
        "product_name": "Intel Gaudi2",
        "launch_date": "2022-05-10",
        "launch_year": "2022",
        "market_segment": "Datacenter AI Training",
        "memory_type": "",
        "memory_gb": "",
        "compute_api": "SynapseAI",
        "status": "historical_active_reference",
        "source_url": "https://download.intel.com/newsroom/2022/corporate/vision/Habana-Gaudi2-Launch-Fact-Sheet.pdf",
        "source_type": "official_fact_sheet",
        "source_confidence": "high",
        "notes": "Launch date from Intel/Habana fact sheet. Memory fields intentionally blank until a registry source is added.",
    },
    {
        "gpu_id": "intel-gaudi3-announcement",
        "vendor": "Intel",
        "family": "Gaudi",
        "architecture": "Gaudi3",
        "product_name": "Intel Gaudi 3 AI Accelerator",
        "launch_date": "2024-04-09",
        "launch_year": "2024",
        "market_segment": "Datacenter AI Training / Inference",
        "memory_type": "",
        "memory_gb": "",
        "compute_api": "SynapseAI",
        "status": "announced_reference",
        "source_url": "https://www.intc.com/news-events/press-releases/detail/1689/intel-unleashes-enterprise-ai-with-gaudi-3-ai-open-systems",
        "source_type": "official_press_release",
        "source_confidence": "high",
        "notes": "Announcement record. Kept separate from later September 2024 launch record.",
    },
    {
        "gpu_id": "intel-gaudi3-launch",
        "vendor": "Intel",
        "family": "Gaudi",
        "architecture": "Gaudi3",
        "product_name": "Intel Gaudi 3 AI Accelerator",
        "launch_date": "2024-09-24",
        "launch_year": "2024",
        "market_segment": "Datacenter AI Training / Inference",
        "memory_type": "",
        "memory_gb": "",
        "compute_api": "SynapseAI",
        "status": "launched_reference",
        "source_url": "https://newsroom.intel.com/artificial-intelligence/next-generation-ai-solutions-xeon-6-gaudi-3",
        "source_type": "official_newsroom",
        "source_confidence": "high",
        "notes": "Official Intel newsroom launch record. No benchmark or pricing claims stored.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "intel_historical_gpu_registry.csv"
    warehouse_path = ROOT / "warehouse" / "historical" / "intel" / "intel_historical_gpu_registry.csv"

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} Intel historical GPU registry rows.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
