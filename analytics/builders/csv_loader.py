from __future__ import annotations

import csv
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    """
    Load a CSV file into a list of dictionaries.
    """
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_by(
    rows: list[dict[str, str]],
    key: str,
) -> dict[str, dict[str, str]]:
    """
    Build an index from one column.
    Example:
        providers = index_by(rows, "provider_id")
        providers["prov000001"]
    """
    return {
        row[key]: row
        for row in rows
    }


def group_by(
    rows: list[dict[str, str]],
    key: str,
) -> dict[str, list[dict[str, str]]]:
    """
    Group rows by one column.
    """
    grouped: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        grouped.setdefault(row[key], []).append(row)

    return grouped


def unique_values(
    rows: list[dict[str, str]],
    key: str,
) -> set[str]:
    """
    Return unique values from one column.
    """
    return {
        row[key]
        for row in rows
    }
