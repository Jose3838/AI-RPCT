from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class HistoricalRegistryMetadata:
    dataset_id: str
    dataset_name: str
    schema_version: str
    owner: str
    first_release: str
    latest_update: str
    row_count: int
    verification_status: str
    source_type: str
    governance_status: str


VALID_VERIFICATION_STATUS = {"verified", "partial", "pending"}
VALID_GOVERNANCE_STATUS = {"compliant", "needs_review", "blocked"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_required_columns(rows: list[dict[str, str]], required_columns: Iterable[str]) -> None:
    if not rows:
        raise ValueError("Registry is empty.")

    missing = set(required_columns) - set(rows[0].keys())
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def validate_unique_column(rows: list[dict[str, str]], column: str) -> None:
    values = [row[column] for row in rows]
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ValueError(f"Duplicate values in {column}: {duplicates}")


def validate_no_duplicate_rows(rows: list[dict[str, str]]) -> None:
    fingerprints = [tuple(sorted(row.items())) for row in rows]
    if len(fingerprints) != len(set(fingerprints)):
        raise ValueError("Duplicate rows found.")


def build_metadata(
    dataset_id: str,
    dataset_name: str,
    schema_version: str,
    row_count: int,
    verification_status: str,
    source_type: str,
    governance_status: str = "compliant",
    owner: str = "AI-RPCT",
    first_release: str | None = None,
    latest_update: str | None = None,
) -> HistoricalRegistryMetadata:
    if verification_status not in VALID_VERIFICATION_STATUS:
        raise ValueError(f"Invalid verification_status: {verification_status}")

    if governance_status not in VALID_GOVERNANCE_STATUS:
        raise ValueError(f"Invalid governance_status: {governance_status}")

    today = date.today().isoformat()

    return HistoricalRegistryMetadata(
        dataset_id=dataset_id,
        dataset_name=dataset_name,
        schema_version=schema_version,
        owner=owner,
        first_release=first_release or today,
        latest_update=latest_update or today,
        row_count=row_count,
        verification_status=verification_status,
        source_type=source_type,
        governance_status=governance_status,
    )


def append_metadata_catalog(path: Path, metadata: HistoricalRegistryMetadata) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(metadata.__dataclass_fields__.keys())
    existing: list[dict[str, str]] = []

    if path.exists():
        existing = read_csv(path)

    existing = [row for row in existing if row["dataset_id"] != metadata.dataset_id]
    existing.append({field: str(getattr(metadata, field)) for field in fieldnames})
    existing.sort(key=lambda row: row["dataset_id"])

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
