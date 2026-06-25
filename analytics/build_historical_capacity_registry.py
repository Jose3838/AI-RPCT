from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "capacity_record_id",
    "relationship_id",
    "observation_date",
    "capacity_status",
    "availability_level",
    "source_id",
]

ROWS = [
    {
        "capacity_record_id": "cap000001",
        "relationship_id": "relprov000004",
        "observation_date": "2024-01-15",
        "capacity_status": "available",
        "availability_level": "high",
        "source_id": "coreweave_docs",
    },
    {
        "capacity_record_id": "cap000002",
        "relationship_id": "relprov000005",
        "observation_date": "2024-02-01",
        "capacity_status": "limited",
        "availability_level": "medium",
        "source_id": "lambda_docs",
    },
    {
        "capacity_record_id": "cap000003",
        "relationship_id": "relprov000001",
        "observation_date": "2024-03-01",
        "capacity_status": "available",
        "availability_level": "high",
        "source_id": "aws_docs",
    },
    {
        "capacity_record_id": "cap000004",
        "relationship_id": "relprov000002",
        "observation_date": "2024-03-15",
        "capacity_status": "available",
        "availability_level": "high",
        "source_id": "azure_docs",
    },
    {
        "capacity_record_id": "cap000005",
        "relationship_id": "relprov000003",
        "observation_date": "2024-04-01",
        "capacity_status": "limited",
        "availability_level": "medium",
        "source_id": "gcp_docs",
    },
]


def write_csv(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():
    data_path = ROOT / "data" / "historical_capacity_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "capacity"
        / "historical_capacity_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} historical capacity records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
