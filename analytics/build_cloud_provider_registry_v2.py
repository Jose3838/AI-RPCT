from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "provider_id",
    "provider_name",
    "provider_category",
    "headquarters_country",
    "status",
    "source_id",
]

ROWS = [
    {
        "provider_id": "prov000001",
        "provider_name": "Amazon Web Services",
        "provider_category": "Hyperscaler",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "aws_docs",
    },
    {
        "provider_id": "prov000002",
        "provider_name": "Microsoft Azure",
        "provider_category": "Hyperscaler",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "azure_docs",
    },
    {
        "provider_id": "prov000003",
        "provider_name": "Google Cloud",
        "provider_category": "Hyperscaler",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "gcp_docs",
    },
    {
        "provider_id": "prov000004",
        "provider_name": "CoreWeave",
        "provider_category": "GPU Cloud",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "coreweave_docs",
    },
    {
        "provider_id": "prov000005",
        "provider_name": "Lambda",
        "provider_category": "GPU Cloud",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "lambda_docs",
    },
    {
        "provider_id": "prov000006",
        "provider_name": "Crusoe",
        "provider_category": "GPU Cloud",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "crusoe_docs",
    },
    {
        "provider_id": "prov000007",
        "provider_name": "Nebius",
        "provider_category": "GPU Cloud",
        "headquarters_country": "Netherlands",
        "status": "active",
        "source_id": "nebius_docs",
    },
    {
        "provider_id": "prov000008",
        "provider_name": "RunPod",
        "provider_category": "GPU Cloud",
        "headquarters_country": "",
        "status": "active",
        "source_id": "runpod_docs",
    },
    {
        "provider_id": "prov000009",
        "provider_name": "Vast.ai",
        "provider_category": "GPU Marketplace",
        "headquarters_country": "USA",
        "status": "active",
        "source_id": "vast_docs",
    },
]

def write_csv(path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():
    data_path = ROOT / "data" / "cloud_provider_registry_v2.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "providers"
        / "cloud_provider_registry_v2.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} cloud provider records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
