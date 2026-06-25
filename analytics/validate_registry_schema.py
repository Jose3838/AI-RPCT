from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASETS = {
    "historical_capacity_registry": ROOT / "data" / "historical_capacity_registry.csv",
    "provider_relationship_registry": ROOT / "data" / "provider_relationship_registry.csv",
    "historical_source_registry": ROOT / "data" / "historical_source_registry.csv",
}

SCHEMAS = [
    ROOT / "schemas" / "historical_capacity_registry.schema.json",
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_fieldnames(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or [])


def validate_schema(schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    dataset_id = schema["dataset_id"]

    csv_path = DATASETS[dataset_id]
    rows = load_csv(csv_path)
    fieldnames = load_fieldnames(csv_path)

    missing = set(schema["required_columns"]) - set(fieldnames)
    if missing:
        raise ValueError(f"{dataset_id}: missing columns {sorted(missing)}")

    for column in schema.get("unique_columns", []):
        values = [row[column] for row in rows]
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            raise ValueError(f"{dataset_id}: duplicate values in {column}: {duplicates}")

    for column, allowed_values in schema.get("allowed_values", {}).items():
        allowed = set(allowed_values)
        invalid = sorted({row[column] for row in rows if row[column] not in allowed})
        if invalid:
            raise ValueError(f"{dataset_id}: invalid values in {column}: {invalid}")

    for column, reference in schema.get("reference_columns", {}).items():
        ref_dataset_id, ref_column = reference.split(".")
        ref_rows = load_csv(DATASETS[ref_dataset_id])
        valid_refs = {row[ref_column] for row in ref_rows}
        invalid_refs = sorted({row[column] for row in rows if row[column] not in valid_refs})
        if invalid_refs:
            raise ValueError(f"{dataset_id}: invalid references in {column}: {invalid_refs}")


def main() -> None:
    for schema_path in SCHEMAS:
        validate_schema(schema_path)

    print(f"Validated {len(SCHEMAS)} registry schema(s).")


if __name__ == "__main__":
    main()
