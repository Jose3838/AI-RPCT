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

ROWS = [
    {
        "pricing_record_id": "price000001",
        "relationship_id": "rel000011",
        "observation_date": "2014-11-01",
        "price_amount": "5000",
        "currency": "USD",
        "unit": "per_gpu",
        "price_type": "launch_price_estimate",
        "verification_status": "partial",
        "source_id": "market_reporting_estimate",
        "notes": (
            "Tesla K80 launch-era price commonly cited around this figure "
            "in public reporting at the time. No single official NVIDIA "
            "list price document found; treat as a rough anchor point, "
            "not a confirmed price."
        ),
    },
    {
        "pricing_record_id": "price000002",
        "relationship_id": "rel000012",
        "observation_date": "2017-12-01",
        "price_amount": "8999",
        "currency": "USD",
        "unit": "per_gpu",
        "price_type": "launch_price_estimate",
        "verification_status": "partial",
        "source_id": "market_reporting_estimate",
        "notes": (
            "Tesla V100 (PCIe) list price as commonly quoted by resellers "
            "around its 2017/2018 launch window. SXM2 variants were "
            "reported higher. No single official NVIDIA source found; "
            "treat as an estimate."
        ),
    },
    {
        "pricing_record_id": "price000003",
        "relationship_id": "rel000013",
        "observation_date": "2020-05-01",
        "price_amount": "11000",
        "currency": "USD",
        "unit": "per_gpu",
        "price_type": "launch_price_estimate",
        "verification_status": "partial",
        "source_id": "market_reporting_estimate",
        "notes": (
            "A100 (40GB, PCIe) launch-era price; public reporting commonly "
            "cited a range of roughly $10,000-$12,500, this uses the "
            "approximate midpoint. 80GB variant and SXM form factors were "
            "priced higher. Not an official NVIDIA list price."
        ),
    },
    {
        "pricing_record_id": "price000004",
        "relationship_id": "rel000014",
        "observation_date": "2023-03-01",
        "price_amount": "30000",
        "currency": "USD",
        "unit": "per_gpu",
        "price_type": "launch_price_estimate",
        "verification_status": "partial",
        "source_id": "market_reporting_estimate",
        "notes": (
            "H100 has no public NVIDIA list price (sold via OEM/system "
            "integrator deals); analyst and press estimates commonly cited "
            "a range of roughly $25,000-$40,000 depending on configuration "
            "and channel. This uses the low end of that range as a "
            "conservative anchor, not a confirmed price."
        ),
    },
]


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
