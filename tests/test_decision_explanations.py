from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "decision_explanations.csv"


def test_decision_explanations_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_decision_explanations.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Decision explanations generated." in result.stdout
    assert DATA.exists()


def test_decision_explanations_contains_reasons():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows
    assert rows[0]["reason_1"]
    assert rows[0]["reason_2"]
