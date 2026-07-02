import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "company_announcement_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "company_announcements" / "company_announcement_registry.csv"

REQUIRED_COLUMNS = {
    "announcement_id",
    "company",
    "announcement_date",
    "announcement_type",
    "title",
    "figure_usd_billion",
    "description",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}

VALID_ANNOUNCEMENT_TYPES = {"capex_guidance", "market_aggregate"}
VALID_SOURCE_CONFIDENCE = {"high", "medium", "low"}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_company_announcement_registry.py")],
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


def test_unique_announcement_ids():
    rows = load_rows(CSV_PATH)
    ids = [row["announcement_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_announcement_types_are_governed():
    for row in load_rows(CSV_PATH):
        assert row["announcement_type"] in VALID_ANNOUNCEMENT_TYPES


def test_source_confidence_is_governed():
    for row in load_rows(CSV_PATH):
        assert row["source_confidence"] in VALID_SOURCE_CONFIDENCE


def test_figures_are_positive_numbers():
    rows = load_rows(CSV_PATH)
    assert len(rows) == 5
    for row in rows:
        assert float(row["figure_usd_billion"]) > 0


def test_combined_aggregate_roughly_matches_individual_figures():
    # Sanity check: the combined 4-company aggregate should be in the
    # right ballpark of the sum of the individual guidance figures
    # (not exact, since individual figures use range midpoints).
    rows = load_rows(CSV_PATH)
    individual_total = sum(
        float(row["figure_usd_billion"])
        for row in rows
        if row["announcement_type"] == "capex_guidance"
    )
    aggregate = next(
        row for row in rows if row["announcement_type"] == "market_aggregate"
    )
    assert abs(individual_total - float(aggregate["figure_usd_billion"])) < 50
