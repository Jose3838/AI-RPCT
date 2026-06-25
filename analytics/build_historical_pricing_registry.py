from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "pricing_record_id",
    "relationship_id",
    "observation_date",
    "price_amount",
    "currency",
    "unit",
    "price_type",
    "verification_status",
    "source_id",
    "notes",
]

ROWS = []


def write_csv(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():
    data_path = ROOT / "data" / "historical_pricing_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "pricing"
        / "historical_pricing_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} historical pricing records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
