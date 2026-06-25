import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "historical_source_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "metadata" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
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
}


def load_rows():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_source_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_source_registry_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_source_registry_not_empty():
    assert len(load_rows()) > 0


def test_required_columns():
    rows = load_rows()
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())


def test_unique_source_ids():
    source_ids = [row["source_id"] for row in load_rows()]
    assert len(source_ids) == len(set(source_ids))


def test_source_types_are_governed():
    allowed = {"official", "secondary"}
    for row in load_rows():
        assert row["source_type"] in allowed


def test_verification_levels_are_governed():
    allowed = {"high", "medium", "low"}
    for row in load_rows():
        assert row["verification_level"] in allowed


def test_sources_are_active_or_deprecated():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows():
        assert row["status"] in allowed


def test_base_urls_are_https():
    for row in load_rows():
        assert row["base_url"].startswith("https://")


def test_core_sources_exist():
    source_ids = {row["source_id"] for row in load_rows()}
    expected = {
        "amd_ir",
        "amd_products",
        "intel_newsroom",
        "intel_products",
        "nvidia_news",
        "nvidia_products",
        "cuda_docs",
        "rocm_docs",
    }
    assert expected.issubset(source_ids)
