import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "historical_entity_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "historical_entity_registry.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "entity_id",
    "entity_type",
    "display_name",
    "canonical_name",
    "vendor",
    "status",
    "source_id",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_entity_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_entity_registry_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_entity_registry_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_required_columns():
    rows = load_rows(CSV_PATH)
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_entity_ids():
    entity_ids = [row["entity_id"] for row in load_rows(CSV_PATH)]
    assert len(entity_ids) == len(set(entity_ids))


def test_entity_types_are_governed():
    allowed = {
        "vendor",
        "architecture",
        "compute_api",
        "product_family",
        "gpu",
        "provider",
        "region",
    }
    for row in load_rows(CSV_PATH):
        assert row["entity_type"] in allowed


def test_entity_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed


def test_entity_source_ids_exist_in_source_registry():
    entity_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in entity_rows:
        assert row["source_id"] in valid_source_ids


def test_core_entities_exist():
    entity_ids = {row["entity_id"] for row in load_rows(CSV_PATH)}
    expected = {
        "vendor_amd",
        "vendor_intel",
        "vendor_nvidia",
        "api_rocm",
        "api_cuda",
        "api_oneapi",
        "gpu_amd_instinct_mi100",
        "gpu_intel_gaudi3",
    }
    assert expected.issubset(entity_ids)
