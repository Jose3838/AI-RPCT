from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


class DataQualityError(Exception):
    """Raised when a historical data quality rule fails."""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_not_empty(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise DataQualityError("Dataset is empty.")


def validate_required_columns(
    rows: list[dict[str, str]],
    required_columns: Iterable[str],
) -> None:
    validate_not_empty(rows)
    missing = set(required_columns) - set(rows[0].keys())

    if missing:
        raise DataQualityError(f"Missing required columns: {sorted(missing)}")


def validate_unique(rows: list[dict[str, str]], column: str) -> None:
    validate_not_empty(rows)

    values = [row[column] for row in rows]
    duplicates = sorted({value for value in values if values.count(value) > 1})

    if duplicates:
        raise DataQualityError(f"Duplicate values in '{column}': {duplicates}")


def validate_allowed_values(
    rows: list[dict[str, str]],
    column: str,
    allowed_values: Iterable[str],
) -> None:
    validate_not_empty(rows)

    allowed = set(allowed_values)
    invalid = sorted({row[column] for row in rows if row[column] not in allowed})

    if invalid:
        raise DataQualityError(f"Invalid values in '{column}': {invalid}")


def validate_https(rows: list[dict[str, str]], column: str) -> None:
    validate_not_empty(rows)

    invalid = [
        row[column]
        for row in rows
        if row.get(column, "") and not row[column].startswith("https://")
    ]

    if invalid:
        raise DataQualityError(f"Invalid https values in '{column}': {invalid}")


def validate_no_duplicate_rows(rows: list[dict[str, str]]) -> None:
    validate_not_empty(rows)

    fingerprints = [tuple(sorted(row.items())) for row in rows]

    if len(fingerprints) != len(set(fingerprints)):
        raise DataQualityError("Duplicate rows found.")


def validate_references_exist(
    rows: list[dict[str, str]],
    column: str,
    valid_values: Iterable[str],
) -> None:
    validate_not_empty(rows)

    valid = set(valid_values)
    invalid = sorted({row[column] for row in rows if row[column] not in valid})

    if invalid:
        raise DataQualityError(f"Invalid references in '{column}': {invalid}")
