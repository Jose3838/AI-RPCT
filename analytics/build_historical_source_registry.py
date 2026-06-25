from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "source_id",
    "organization",
    "source_name",
    "source_type",
    "base_url",
    "coverage",
    "verification_level",
    "last_verified",
    "status",
    "notes",
]

ROWS = [
    {
        "source_id": "amd_ir",
        "organization": "AMD",
        "source_name": "AMD Investor Relations",
        "source_type": "official",
        "base_url": "https://ir.amd.com",
        "coverage": "AMD official announcements and investor press releases",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Primary source for AMD launch and corporate announcements.",
    },
    {
        "source_id": "amd_products",
        "organization": "AMD",
        "source_name": "AMD Product Pages",
        "source_type": "official",
        "base_url": "https://www.amd.com",
        "coverage": "AMD product specifications and product pages",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Used for product-level references when available.",
    },
    {
        "source_id": "intel_newsroom",
        "organization": "Intel",
        "source_name": "Intel Newsroom",
        "source_type": "official",
        "base_url": "https://newsroom.intel.com",
        "coverage": "Intel official news and launch announcements",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Primary source for Intel public launch announcements.",
    },
    {
        "source_id": "intel_products",
        "organization": "Intel",
        "source_name": "Intel Product Specifications",
        "source_type": "official",
        "base_url": "https://www.intel.com",
        "coverage": "Intel product specification pages",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Used for Intel product SKU details.",
    },
    {
        "source_id": "nvidia_news",
        "organization": "NVIDIA",
        "source_name": "NVIDIA Newsroom",
        "source_type": "official",
        "base_url": "https://nvidianews.nvidia.com",
        "coverage": "NVIDIA official announcements",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Future source for NVIDIA historical expansion.",
    },
    {
        "source_id": "nvidia_products",
        "organization": "NVIDIA",
        "source_name": "NVIDIA Product Pages",
        "source_type": "official",
        "base_url": "https://www.nvidia.com",
        "coverage": "NVIDIA product pages and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Future source for NVIDIA product-level references.",
    },
    {
        "source_id": "cuda_docs",
        "organization": "NVIDIA",
        "source_name": "CUDA Documentation",
        "source_type": "official",
        "base_url": "https://docs.nvidia.com/cuda",
        "coverage": "CUDA documentation and release references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Future source for CUDA timeline registry.",
    },
    {
        "source_id": "rocm_docs",
        "organization": "AMD",
        "source_name": "ROCm Documentation",
        "source_type": "official",
        "base_url": "https://rocm.docs.amd.com",
        "coverage": "ROCm documentation and release references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Future source for ROCm timeline registry.",
    },
    {
        "source_id": "coreweave_docs",
        "organization": "CoreWeave",
        "source_name": "CoreWeave Documentation",
        "source_type": "official",
        "base_url": "https://docs.coreweave.com",
        "coverage": "CoreWeave documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official CoreWeave documentation.",
    },
    {
        "source_id": "lambda_docs",
        "organization": "Lambda",
        "source_name": "Lambda Documentation",
        "source_type": "official",
        "base_url": "https://docs.lambda.ai",
        "coverage": "Lambda documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official Lambda documentation.",
    },
    {
        "source_id": "crusoe_docs",
        "organization": "Crusoe",
        "source_name": "Crusoe Documentation",
        "source_type": "official",
        "base_url": "https://docs.crusoe.ai",
        "coverage": "Crusoe documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official Crusoe documentation.",
    },
    {
        "source_id": "nebius_docs",
        "organization": "Nebius",
        "source_name": "Nebius Documentation",
        "source_type": "official",
        "base_url": "https://docs.nebius.com",
        "coverage": "Nebius documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official Nebius documentation.",
    },
    {
        "source_id": "runpod_docs",
        "organization": "RunPod",
        "source_name": "RunPod Documentation",
        "source_type": "official",
        "base_url": "https://docs.runpod.io",
        "coverage": "RunPod documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official RunPod documentation.",
    },
    {
        "source_id": "vast_docs",
        "organization": "Vast.ai",
        "source_name": "Vast.ai Documentation",
        "source_type": "official",
        "base_url": "https://docs.vast.ai",
        "coverage": "Vast.ai documentation and platform references",
        "verification_level": "high",
        "last_verified": "2026-06-25",
        "status": "active",
        "notes": "Official Vast.ai documentation.",
    },
    

]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "historical_source_registry.csv"
    warehouse_path = ROOT / "warehouse" / "historical" / "metadata" / "historical_source_registry.csv"

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} historical source registry rows.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
