from __future__ import annotations

from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

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


def main():
    data_path = ROOT / "data" / "historical_capacity_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "capacity"
        / "historical_capacity_registry.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=ROWS,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(ROWS),
        label="historical capacity records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
