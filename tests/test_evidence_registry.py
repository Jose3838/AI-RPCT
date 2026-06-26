from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "evidence_registry.csv"


def test_evidence_registry_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_evidence_registry.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "evidence records" in result.stdout
    assert DATA.exists()


def test_evidence_registry_contains_records():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) >= 2
    assert rows[0]["decision_id"] == "decision-001"
