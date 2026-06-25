import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "provider_relationship_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "providers" / "provider_relationship_registry.csv"

SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"
ENTITY_REGISTRY = ROOT / "data" / "historical_entity_registry.csv"
PROVIDER_ENTITY_REGISTRY = ROOT / "data" / "provider_entity_registry.csv"


REQUIRED_COLUMNS = {
    "relationship_id",
    "provider_entity_id",
    "target_entity_id",
    "relationship_type",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "analytics" / "build_provider_relationship_registry.py"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_relationship_ids():
    ids = [r["relationship_id"] for r in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_provider_entity_ids_exist():
    valid = {
        r["entity_id"]
        for r in load_rows(PROVIDER_ENTITY_REGISTRY)
    }

    for row in load_rows(CSV_PATH):
        assert row["provider_entity_id"] in valid


def test_target_entity_ids_exist():
    valid = {
        r["entity_id"]
        for r in load_rows(ENTITY_REGISTRY)
    }

    for row in load_rows(CSV_PATH):
        assert row["target_entity_id"] in valid


def test_source_ids_exist():
    valid = {
        r["source_id"]
        for r in load_rows(SOURCE_REGISTRY)
    }

    for row in load_rows(CSV_PATH):
        assert row["source_id"] in valid


def test_relationship_types():
    allowed = {
        "supports",
        "offers",
    }

    for row in load_rows(CSV_PATH):
        assert row["relationship_type"] in allowed


def test_status():
    allowed = {
        "active",
        "deprecated",
        "pending_review",
    }

    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed
