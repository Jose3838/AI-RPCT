import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "provider_entity_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "providers" / "provider_entity_registry.csv"
PROVIDER_REGISTRY = ROOT / "data" / "cloud_provider_registry_v2.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "entity_id",
    "provider_id",
    "provider_name",
    "provider_category",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_provider_entity_registry.py")],
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


def test_unique_entity_ids():
    ids = [row["entity_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_unique_provider_ids():
    ids = [row["provider_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_provider_ids_exist():
    entity_rows = load_rows(CSV_PATH)
    provider_rows = load_rows(PROVIDER_REGISTRY)
    valid_provider_ids = {row["provider_id"] for row in provider_rows}

    for row in entity_rows:
        assert row["provider_id"] in valid_provider_ids


def test_source_ids_exist():
    entity_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in entity_rows:
        assert row["source_id"] in valid_source_ids


def test_provider_categories_are_governed():
    allowed = {"Hyperscaler", "GPU Cloud", "GPU Marketplace"}
    for row in load_rows(CSV_PATH):
        assert row["provider_category"] in allowed


def test_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed
