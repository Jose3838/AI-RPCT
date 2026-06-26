from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_decision_history_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "save_decision_history.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Decision history updated." in result.stdout

    assert (
        ROOT / "data" / "decision_history.csv"
    ).exists()
