import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "unified_hardware_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "unified_hardware_registry.csv"
ENTITY_REGISTRY = ROOT / "data" / "historical_entity_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "hardware_id",
    "entity_id",
    "vendor",
    "product_family",
    "architecture",
    "compute_api",
    "launch_year",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_unified_hardware_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_unified_hardware_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_unified_hardware_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_hardware_ids():
    hardware_ids = [row["hardware_id"] for row in load_rows(CSV_PATH)]
    assert len(hardware_ids) == len(set(hardware_ids))


def test_unique_entity_ids():
    entity_ids = [row["entity_id"] for row in load_rows(CSV_PATH)]
    assert len(entity_ids) == len(set(entity_ids))


def test_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed


def test_entity_ids_exist():
    hardware_rows = load_rows(CSV_PATH)
    entity_rows = load_rows(ENTITY_REGISTRY)
    valid_entity_ids = {row["entity_id"] for row in entity_rows}

    for row in hardware_rows:
        assert row["entity_id"] in valid_entity_ids


def test_source_ids_exist():
    hardware_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in hardware_rows:
        assert row["source_id"] in valid_source_ids


def test_core_hardware_records_exist():
    hardware_ids = {row["hardware_id"] for row in load_rows(CSV_PATH)}
    expected = {"hw000001", "hw000002", "hw000003", "hw000004", "hw000005"}
    assert expected.issubset(hardware_ids)
