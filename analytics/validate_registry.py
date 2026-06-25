from __future__ import annotations

from pathlib import Path
from typing import Iterable

from historical_data_quality import (
    load_csv,
    validate_allowed_values,
    validate_https,
    validate_no_duplicate_rows,
    validate_not_empty,
    validate_required_columns,
    validate_unique,
)


def validate_registry(
    csv_path: Path,
    required_columns: Iterable[str],
    unique_columns: Iterable[str] | None = None,
    allowed_values: dict[str, Iterable[str]] | None = None,
    https_columns: Iterable[str] | None = None,
) -> None:
    rows = load_csv(csv_path)

    validate_not_empty(rows)
    validate_required_columns(rows, required_columns)
    validate_no_duplicate_rows(rows)

    for column in unique_columns or []:
        validate_unique(rows, column)

    for column, values in (allowed_values or {}).items():
        validate_allowed_values(rows, column, values)

    for column in https_columns or []:
        validate_https(rows, column)


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    validate_registry(
        csv_path=root / "data" / "historical_source_registry.csv",
        required_columns={
            "source_id",
            "organization",
            "source_name",
            "source_type",
            "base_url",
            "coverage",
            "verification_level",
            "last_verified",
            "status",
            "notes",
        },
        unique_columns={"source_id"},
        allowed_values={
            "source_type": {"official", "secondary"},
            "verification_level": {"high", "medium", "low"},
            "status": {"active", "deprecated", "pending_review"},
        },
        https_columns={"base_url"},
    )

    validate_registry(
        csv_path=root / "data" / "historical_entity_registry.csv",
        required_columns={
            "entity_id",
            "entity_type",
            "display_name",
            "canonical_name",
            "vendor",
            "status",
            "source_id",
            "notes",
        },
        unique_columns={"entity_id"},
        allowed_values={
            "entity_type": {
                "vendor",
                "architecture",
                "compute_api",
                "product_family",
                "gpu",
                "provider",
                "region",
            },
            "status": {"active", "deprecated", "pending_review"},
        },
    )

    print("Historical registry validation passed.")


if __name__ == "__main__":
    main()
