from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "relationship_id",
    "provider_entity_id",
    "target_entity_id",
    "relationship_type",
    "status",
    "source_id",
]

ROWS = [
    {
        "relationship_id": "relprov000001",
        "provider_entity_id": "provider_aws",
        "target_entity_id": "api_cuda",
        "relationship_type": "supports",
        "status": "active",
        "source_id": "aws_docs",
    },
    {
        "relationship_id": "relprov000002",
        "provider_entity_id": "provider_azure",
        "target_entity_id": "api_cuda",
        "relationship_type": "supports",
        "status": "active",
        "source_id": "azure_docs",
    },
    {
        "relationship_id": "relprov000003",
        "provider_entity_id": "provider_google_cloud",
        "target_entity_id": "api_cuda",
        "relationship_type": "supports",
        "status": "active",
        "source_id": "gcp_docs",
    },
    {
        "relationship_id": "relprov000004",
        "provider_entity_id": "provider_coreweave",
        "target_entity_id": "gpu_nvidia_h100",
        "relationship_type": "offers",
        "status": "active",
        "source_id": "coreweave_docs",
    },
    {
        "relationship_id": "relprov000005",
        "provider_entity_id": "provider_lambda",
        "target_entity_id": "gpu_nvidia_a100",
        "relationship_type": "offers",
        "status": "active",
        "source_id": "lambda_docs",
    },
]

def write_csv(path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():
    data_path = ROOT / "data" / "provider_relationship_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "providers"
        / "provider_relationship_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} provider relationship records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
