from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "entity_id",
    "provider_id",
    "provider_name",
    "provider_category",
    "status",
    "source_id",
]

ROWS = [
    {
        "entity_id": "provider_aws",
        "provider_id": "prov000001",
        "provider_name": "Amazon Web Services",
        "provider_category": "Hyperscaler",
        "status": "active",
        "source_id": "aws_docs",
    },
    {
        "entity_id": "provider_azure",
        "provider_id": "prov000002",
        "provider_name": "Microsoft Azure",
        "provider_category": "Hyperscaler",
        "status": "active",
        "source_id": "azure_docs",
    },
    {
        "entity_id": "provider_google_cloud",
        "provider_id": "prov000003",
        "provider_name": "Google Cloud",
        "provider_category": "Hyperscaler",
        "status": "active",
        "source_id": "gcp_docs",
    },
    {
        "entity_id": "provider_coreweave",
        "provider_id": "prov000004",
        "provider_name": "CoreWeave",
        "provider_category": "GPU Cloud",
        "status": "active",
        "source_id": "coreweave_docs",
    },
    {
        "entity_id": "provider_lambda",
        "provider_id": "prov000005",
        "provider_name": "Lambda",
        "provider_category": "GPU Cloud",
        "status": "active",
        "source_id": "lambda_docs",
    },
    {
        "entity_id": "provider_crusoe",
        "provider_id": "prov000006",
        "provider_name": "Crusoe",
        "provider_category": "GPU Cloud",
        "status": "active",
        "source_id": "crusoe_docs",
    },
    {
        "entity_id": "provider_nebius",
        "provider_id": "prov000007",
        "provider_name": "Nebius",
        "provider_category": "GPU Cloud",
        "status": "active",
        "source_id": "nebius_docs",
    },
    {
        "entity_id": "provider_runpod",
        "provider_id": "prov000008",
        "provider_name": "RunPod",
        "provider_category": "GPU Cloud",
        "status": "active",
        "source_id": "runpod_docs",
    },
    {
        "entity_id": "provider_vast",
        "provider_id": "prov000009",
        "provider_name": "Vast.ai",
        "provider_category": "GPU Marketplace",
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
    data_path = ROOT / "data" / "provider_entity_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "providers"
        / "provider_entity_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} provider entity records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
