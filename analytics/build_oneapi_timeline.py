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
        "timeline_id": "oneapi_2021_1",
        "software_stack": "oneAPI",
        "vendor": "Intel",
        "version": "2021.1",
        "release_date": "2020-12-08",
        "release_year": "2020",
        "lifecycle_status": "historical",
        "source_id": "intel_newsroom",
        "source_url": "https://www.intel.com/content/www/us/en/newsroom/news/intel-oneapi-toolkits-gold-release.html",
        "notes": "Intel announced gold release of oneAPI toolkits. No compatibility or performance claims stored.",
    },
    {
        "timeline_id": "oneapi_2022_1",
        "software_stack": "oneAPI",
        "vendor": "Intel",
        "version": "2022.1",
        "release_date": "2021-12-22",
        "release_year": "2021",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://www.intel.com/content/www/us/en/developer/articles/release-notes/intel-oneapi-toolkit-release-notes.html",
        "notes": "Intel oneAPI toolkit release notes reference. Date retained as release-note reference.",
    },
    {
        "timeline_id": "oneapi_2023_2",
        "software_stack": "oneAPI",
        "vendor": "Intel",
        "version": "2023.2",
        "release_date": "2023-06-28",
        "release_year": "2023",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://www.intel.com/content/www/us/en/developer/articles/release-notes/intel-oneapi-toolkit-release-notes.html",
        "notes": "Intel oneAPI toolkit release notes reference. No inferred support matrix stored.",
    },
    {
        "timeline_id": "oneapi_2024_2",
        "software_stack": "oneAPI",
        "vendor": "Intel",
        "version": "2024.2",
        "release_date": "2024-06-25",
        "release_year": "2024",
        "lifecycle_status": "historical",
        "source_id": "intel_products",
        "source_url": "https://www.intel.com/content/www/us/en/developer/articles/release-notes/intel-oneapi-toolkit-release-notes.html",
        "notes": "Intel oneAPI toolkit release notes reference.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "oneapi_timeline.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "oneapi"
        / "oneapi_timeline.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} oneAPI timeline records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
