from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "timeline_id",
    "software_stack",
    "vendor",
    "version",
    "release_date",
    "release_year",
    "lifecycle_status",
    "source_id",
    "source_url",
    "notes",
]

ROWS = [
    {
        "timeline_id": "rocm_050",
        "software_stack": "ROCm",
        "vendor": "AMD",
        "version": "5.0",
        "release_date": "2022-02-15",
        "release_year": "2022",
        "lifecycle_status": "historical",
        "source_id": "rocm_docs",
        "source_url": "https://rocm.docs.amd.com",
        "notes": "Official ROCm documentation reference.",
    },
    {
        "timeline_id": "rocm_060",
        "software_stack": "ROCm",
        "vendor": "AMD",
        "version": "6.0",
        "release_date": "2023-12-06",
        "release_year": "2023",
        "lifecycle_status": "historical",
        "source_id": "rocm_docs",
        "source_url": "https://rocm.docs.amd.com",
        "notes": "Official ROCm documentation reference.",
    },
    {
        "timeline_id": "rocm_061",
        "software_stack": "ROCm",
        "vendor": "AMD",
        "version": "6.1",
        "release_date": "2024-03-20",
        "release_year": "2024",
        "lifecycle_status": "historical",
        "source_id": "rocm_docs",
        "source_url": "https://rocm.docs.amd.com",
        "notes": "Official ROCm documentation reference.",
    },
    {
        "timeline_id": "rocm_070",
        "software_stack": "ROCm",
        "vendor": "AMD",
        "version": "7.0",
        "release_date": "2025-06-17",
        "release_year": "2025",
        "lifecycle_status": "current",
        "source_id": "rocm_docs",
        "source_url": "https://rocm.docs.amd.com",
        "notes": "Official ROCm documentation reference.",
    },
]

def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "rocm_timeline.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "rocm"
        / "rocm_timeline.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} ROCm timeline records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
