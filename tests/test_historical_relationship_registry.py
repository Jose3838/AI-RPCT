import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "historical_relationship_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "historical_relationship_registry.csv"
ENTITY_REGISTRY = ROOT / "data" / "historical_entity_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "relationship_id",
    "source_entity_id",
    "relationship_type",
    "target_entity_id",
    "source_id",
    "status",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_relationship_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_relationship_registry_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_relationship_registry_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_relationship_ids():
    relationship_ids = [row["relationship_id"] for row in load_rows(CSV_PATH)]
    assert len(relationship_ids) == len(set(relationship_ids))


def test_relationship_types_are_governed():
    allowed = {
        "uses_architecture",
        "uses_compute_api",
        "member_of_family",
        "provided_by",
        "available_in_region",
    }
    for row in load_rows(CSV_PATH):
        assert row["relationship_type"] in allowed


def test_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed


def test_source_entities_exist():
    relationship_rows = load_rows(CSV_PATH)
    entity_rows = load_rows(ENTITY_REGISTRY)
    valid_entity_ids = {row["entity_id"] for row in entity_rows}

    for row in relationship_rows:
        assert row["source_entity_id"] in valid_entity_ids


def test_target_entities_exist():
    relationship_rows = load_rows(CSV_PATH)
    entity_rows = load_rows(ENTITY_REGISTRY)
    valid_entity_ids = {row["entity_id"] for row in entity_rows}

    for row in relationship_rows:
        assert row["target_entity_id"] in valid_entity_ids


def test_source_ids_exist():
    relationship_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in relationship_rows:
        assert row["source_id"] in valid_source_ids
