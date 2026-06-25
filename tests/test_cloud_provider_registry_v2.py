import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "cloud_provider_registry_v2.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "providers" / "cloud_provider_registry_v2.csv"
SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REQUIRED_COLUMNS = {
    "provider_id",
    "provider_name",
    "provider_category",
    "headquarters_country",
    "status",
    "source_id",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_cloud_provider_registry_v2.py")],
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


def test_unique_provider_ids():
    ids = [row["provider_id"] for row in load_rows(CSV_PATH)]
    assert len(ids) == len(set(ids))


def test_provider_categories_are_governed():
    allowed = {"Hyperscaler", "GPU Cloud", "GPU Marketplace"}
    for row in load_rows(CSV_PATH):
        assert row["provider_category"] in allowed


def test_status_is_governed():
    allowed = {"active", "deprecated", "pending_review"}
    for row in load_rows(CSV_PATH):
        assert row["status"] in allowed


def test_source_ids_exist():
    provider_rows = load_rows(CSV_PATH)
    source_rows = load_rows(SOURCE_REGISTRY)
    valid_source_ids = {row["source_id"] for row in source_rows}

    for row in provider_rows:
        assert row["source_id"] in valid_source_ids


def test_core_providers_exist():
    providers = {row["provider_name"] for row in load_rows(CSV_PATH)}
    expected = {
        "Amazon Web Services",
        "Microsoft Azure",
        "Google Cloud",
        "CoreWeave",
        "Lambda",
        "Crusoe",
        "Nebius",
        "RunPod",
        "Vast.ai",
    }
    assert expected.issubset(providers)
