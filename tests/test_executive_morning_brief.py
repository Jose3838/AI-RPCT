from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "executive_morning_brief.csv"
WAREHOUSE = ROOT / "warehouse" / "decision" / "executive_morning_brief.csv"


def test_executive_morning_brief_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_executive_morning_brief.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Executive morning brief generated." in result.stdout
    assert DATA.exists()
    assert WAREHOUSE.exists()


def test_executive_morning_brief_has_summary():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows
    assert rows[0]["brief_id"] == "brief-001"
    assert rows[0]["summary"]
    assert rows[0]["procurement_recommendation"]
