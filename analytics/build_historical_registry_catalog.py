from __future__ import annotations

from pathlib import Path

from historical_registry_framework import append_metadata_catalog, build_metadata, read_csv

ROOT = Path(__file__).resolve().parents[1]

AMD_REGISTRY = ROOT / "data" / "amd_historical_gpu_registry.csv"
CATALOG = ROOT / "warehouse" / "historical" / "metadata" / "historical_registry_catalog.csv"


def main() -> None:
    amd_rows = read_csv(AMD_REGISTRY)

    amd_metadata = build_metadata(
        dataset_id="amd_historical_gpu_registry",
        dataset_name="AMD Historical GPU Registry",
        schema_version="1",
        row_count=len(amd_rows),
        verification_status="partial",
        source_type="official_mixed",
        governance_status="compliant",
    )

    append_metadata_catalog(CATALOG, amd_metadata)

    print(f"Wrote registry catalog: {CATALOG}")
    print(f"Registered datasets: 1")


if __name__ == "__main__":
    main()
