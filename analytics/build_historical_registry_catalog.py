from __future__ import annotations

from pathlib import Path

from historical_registry_framework import append_metadata_catalog, build_metadata, read_csv

ROOT = Path(__file__).resolve().parents[1]

CATALOG = ROOT / "warehouse" / "historical" / "metadata" / "historical_registry_catalog.csv"

REGISTRIES = [
    {
        "path": ROOT / "data" / "amd_historical_gpu_registry.csv",
        "dataset_id": "amd_historical_gpu_registry",
        "dataset_name": "AMD Historical GPU Registry",
        "schema_version": "1",
        "verification_status": "partial",
        "source_type": "official_mixed",
    },
    {
        "path": ROOT / "data" / "intel_historical_gpu_registry.csv",
        "dataset_id": "intel_historical_gpu_registry",
        "dataset_name": "Intel Historical GPU Registry",
        "schema_version": "1",
        "verification_status": "partial",
        "source_type": "official_mixed",
    },
]


def main() -> None:
    registered = 0

    for registry in REGISTRIES:
        rows = read_csv(registry["path"])

        metadata = build_metadata(
            dataset_id=registry["dataset_id"],
            dataset_name=registry["dataset_name"],
            schema_version=registry["schema_version"],
            row_count=len(rows),
            verification_status=registry["verification_status"],
            source_type=registry["source_type"],
            governance_status="compliant",
        )

        append_metadata_catalog(CATALOG, metadata)
        registered += 1

    print(f"Wrote registry catalog: {CATALOG}")
    print(f"Registered datasets: {registered}")


if __name__ == "__main__":
    main()
