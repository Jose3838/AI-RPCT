import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "unified_accelerator_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "unified_accelerator_registry.csv"
HARDWARE_REGISTRY = ROOT / "data" / "unified_hardware_registry.csv"
ENTITY_REGISTRY = ROOT / "data" / "historical_entity_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "accelerator_id",
    "hardware_id",
    "entity_id",
    "vendor",
    "accelerator_type",
    "product_family",
    "architecture",
    "compute_api",
    "generation",
    "launch_year",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_unified_accelerator_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_unified_accelerator_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_unified_accelerator_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_accelerator_ids():
    accelerator_ids = [row["accelerator_id"] for row in load_rows(CSV_PATH)]
    assert len(accelerator_ids) == len(set(accelerator_ids))


def test_unique_hardware_ids():
    hardware_ids = [row["hardware_id"] for row in load_rows(CSV_PATH)]
    assert len(hardware_ids) == len(set(hardware_ids))


def test_accelerator_types_are_governed():
    allowed = {"GPU", "AI Accelerator"}
    for row in load_rows(CSV_PATH):
        assert row["accelerator_type"] in allowed


def test_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed


def test_hardware_ids_exist():
    accelerator_rows = load_rows(CSV_PATH)
    hardware_rows = load_rows(HARDWARE_REGISTRY)
    valid_hardware_ids = {row["hardware_id"] for row in hardware_rows}

    for row in accelerator_rows:
        assert row["hardware_id"] in valid_hardware_ids


def test_entity_ids_exist():
    accelerator_rows = load_rows(CSV_PATH)
    entity_rows = load_rows(ENTITY_REGISTRY)
    valid_entity_ids = {row["entity_id"] for row in entity_rows}

    for row in accelerator_rows:
        assert row["entity_id"] in valid_entity_ids


def test_source_ids_exist():
    accelerator_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in accelerator_rows:
        assert row["source_id"] in valid_source_ids


def test_core_vendors_exist():
    vendors = {row["vendor"] for row in load_rows(CSV_PATH)}
    expected = {"AMD", "Intel", "NVIDIA"}
    assert expected.issubset(vendors)
