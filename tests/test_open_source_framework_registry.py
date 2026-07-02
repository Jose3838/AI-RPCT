import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "open_source_framework_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "open_source" / "open_source_framework_registry.csv"

REQUIRED_COLUMNS = {
    "release_id",
    "project",
    "version",
    "release_date",
    "milestone_type",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}

VALID_MILESTONE_TYPES = {
    "first_stable_release",
    "earliest_available_release",
    "latest_as_of_observation",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_open_source_framework_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_unique_release_ids():
    rows = load_rows(CSV_PATH)
    ids = [row["release_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_covers_three_projects():
    rows = load_rows(CSV_PATH)
    projects = {row["project"] for row in rows}
    assert projects == {"PyTorch", "vLLM", "Triton Inference Server"}


def test_each_project_has_first_and_latest():
    rows = load_rows(CSV_PATH)
    for project in {"PyTorch", "vLLM", "Triton Inference Server"}:
        project_rows = [r for r in rows if r["project"] == project]
        assert len(project_rows) == 2
        milestone_types = {r["milestone_type"] for r in project_rows}
        assert "latest_as_of_observation" in milestone_types

        first_date = datetime.strptime(
            next(r["release_date"] for r in project_rows if r["milestone_type"] != "latest_as_of_observation"),
            "%Y-%m-%d",
        )
        latest_date = datetime.strptime(
            next(r["release_date"] for r in project_rows if r["milestone_type"] == "latest_as_of_observation"),
            "%Y-%m-%d",
        )
        assert latest_date > first_date


def test_all_rows_are_high_confidence_official_github_releases():
    # Unlike pricing/performance/supply-chain, these dates come directly
    # from the GitHub Releases API (a primary source), not secondary
    # aggregators - every row should reflect that higher confidence.
    for row in load_rows(CSV_PATH):
        assert row["source_type"] == "official_github_release"
        assert row["source_confidence"] == "high"
        assert row["source_url"].startswith("https://github.com/")
