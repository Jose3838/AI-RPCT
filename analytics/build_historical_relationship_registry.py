from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "relationship_id",
    "source_entity_id",
    "relationship_type",
    "target_entity_id",
    "source_id",
    "status",
    "notes",
]

ROWS = [
    {
        "relationship_id": "rel000001",
        "source_entity_id": "gpu_amd_instinct_mi100",
        "relationship_type": "uses_architecture",
        "target_entity_id": "arch_cdna",
        "source_id": "amd_products",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000002",
        "source_entity_id": "gpu_amd_instinct_mi100",
        "relationship_type": "uses_compute_api",
        "target_entity_id": "api_rocm",
        "source_id": "rocm_docs",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000003",
        "source_entity_id": "gpu_amd_instinct_mi300x",
        "relationship_type": "uses_architecture",
        "target_entity_id": "arch_cdna3",
        "source_id": "amd_products",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000004",
        "source_entity_id": "gpu_amd_instinct_mi300x",
        "relationship_type": "uses_compute_api",
        "target_entity_id": "api_rocm",
        "source_id": "rocm_docs",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000005",
        "source_entity_id": "gpu_intel_max_1100",
        "relationship_type": "uses_architecture",
        "target_entity_id": "arch_ponte_vecchio",
        "source_id": "intel_products",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000006",
        "source_entity_id": "gpu_intel_max_1100",
        "relationship_type": "uses_compute_api",
        "target_entity_id": "api_oneapi",
        "source_id": "intel_products",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000007",
        "source_entity_id": "gpu_intel_gaudi2",
        "relationship_type": "uses_compute_api",
        "target_entity_id": "api_synapseai",
        "source_id": "intel_newsroom",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000008",
        "source_entity_id": "gpu_intel_gaudi3",
        "relationship_type": "uses_compute_api",
        "target_entity_id": "api_synapseai",
        "source_id": "intel_newsroom",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000009",
        "source_entity_id": "gpu_amd_instinct_mi100",
        "relationship_type": "member_of_family",
        "target_entity_id": "family_amd_instinct",
        "source_id": "amd_products",
        "status": "active",
        "notes": "",
    },
    {
        "relationship_id": "rel000010",
        "source_entity_id": "gpu_intel_max_1100",
        "relationship_type": "member_of_family",
        "target_entity_id": "family_intel_data_center_gpu_max",
        "source_id": "intel_products",
        "status": "active",
        "notes": "",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main():
    data_path = ROOT / "data" / "historical_relationship_registry.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "metadata"
        / "historical_relationship_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} relationships.")


if __name__ == "__main__":
    main()
