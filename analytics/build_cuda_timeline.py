from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "timeline_id",
    "software_stack",
    "version",
    "release_date",
    "release_year",
    "source_id",
    "source_url",
    "status",
    "notes",
]

ROWS = [
    {
        "timeline_id": "cuda_090",
        "software_stack": "CUDA",
        "version": "9.0",
        "release_date": "2018-06-21",
        "release_year": "2018",
        "source_id": "cuda_docs",
        "source_url": "https://docs.nvidia.com/cuda/archive/9.0/cuda-toolkit-release-notes/index.html",
        "status": "historical_reference",
        "notes": "Archived CUDA 9.0 release notes reference. Date reflects NVIDIA documentation page date.",
    },
    {
        "timeline_id": "cuda_100",
        "software_stack": "CUDA",
        "version": "10.0",
        "release_date": "2018-10-30",
        "release_year": "2018",
        "source_id": "cuda_docs",
        "source_url": "https://docs.nvidia.com/cuda/archive/10.0/cuda-toolkit-release-notes/index.html",
        "status": "historical_reference",
        "notes": "Archived CUDA 10.0 release notes reference. Date reflects NVIDIA documentation page date.",
    },
    {
        "timeline_id": "cuda_1201",
        "software_stack": "CUDA",
        "version": "12.0 Update 1",
        "release_date": "2023-01-28",
        "release_year": "2023",
        "source_id": "cuda_docs",
        "source_url": "https://docs.nvidia.com/cuda/archive/12.0.1/cuda-toolkit-release-notes/index.html",
        "status": "historical_reference",
        "notes": "CUDA 12.0 Update 1 release notes reference. No driver matrix copied into v1.",
    },
    {
        "timeline_id": "cuda_1230",
        "software_stack": "CUDA",
        "version": "12.3",
        "release_date": "2023-10-10",
        "release_year": "2023",
        "source_id": "cuda_docs",
        "source_url": "https://docs.nvidia.com/cuda/archive/12.3.0/cuda-toolkit-release-notes/contents.html",
        "status": "historical_reference",
        "notes": "CUDA 12.3 release notes contents reference.",
    },
    {
        "timeline_id": "cuda_1301",
        "software_stack": "CUDA",
        "version": "13.0 Update 1",
        "release_date": "2025-09-04",
        "release_year": "2025",
        "source_id": "cuda_docs",
        "source_url": "https://docs.nvidia.com/cuda/archive/13.0.1/cuda-toolkit-release-notes/index.html",
        "status": "historical_reference",
        "notes": "CUDA 13.0 Update 1 release notes reference.",
    },
]

def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)

def main() -> None:
    data_path = ROOT / "data" / "cuda_timeline.csv"
    warehouse_path = ROOT / "warehouse" / "historical" / "cuda" / "cuda_timeline.csv"

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} CUDA timeline records.")
    print(data_path)
    print(warehouse_path)

if __name__ == "__main__":
    main()
