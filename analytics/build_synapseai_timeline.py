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
        "timeline_id": "synapseai_100",
        "software_stack": "SynapseAI",
        "vendor": "Intel",
        "version": "1.10",
        "release_date": "2022-09-27",
        "release_year": "2022",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://docs.habana.ai",
        "notes": "Official SynapseAI documentation reference.",
    },
    {
        "timeline_id": "synapseai_110",
        "software_stack": "SynapseAI",
        "vendor": "Intel",
        "version": "1.11",
        "release_date": "2023-03-30",
        "release_year": "2023",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://docs.habana.ai",
        "notes": "Official SynapseAI documentation reference.",
    },
    {
        "timeline_id": "synapseai_115",
        "software_stack": "SynapseAI",
        "vendor": "Intel",
        "version": "1.15",
        "release_date": "2024-04-02",
        "release_year": "2024",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://docs.habana.ai",
        "notes": "Official SynapseAI documentation reference.",
    },
    {
        "timeline_id": "synapseai_120",
        "software_stack": "SynapseAI",
        "vendor": "Intel",
        "version": "1.20",
        "release_date": "2025-03-18",
        "release_year": "2025",
        "lifecycle_status": "current",
        "source_id": "intel_products",
        "source_url": "https://docs.habana.ai",
        "notes": "Official SynapseAI documentation reference.",
    },
]


def write_csv(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():

    data_path = ROOT / "data" / "synapseai_timeline.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "synapseai"
        / "synapseai_timeline.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} SynapseAI timeline records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
