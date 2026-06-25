import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "data_quality_metrics.csv"


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_data_quality_metrics.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_dataset_exists():
    assert CSV_PATH.exists()


def test_not_empty():
    assert len(load_rows(CSV_PATH)) > 0


def test_row_counts_positive():
    for row in load_rows(CSV_PATH):
        assert int(row["row_count"]) >= 0


def test_column_counts_positive():
    for row in load_rows(CSV_PATH):
        assert int(row["column_count"]) > 0
