from pathlib import Path
import subprocess
import sys

from decision.engine import build_recommendation

ROOT = Path(__file__).resolve().parents[1]


def test_decision_engine_builds_recommendation():
    decision = build_recommendation()

    assert decision.decision_id == "decision-001"
    assert decision.topic == "AI Infrastructure"
    assert decision.recommendation
    assert 0 <= decision.confidence <= 1
    assert decision.rationale
    assert "evidence" in decision.rationale.lower()


def test_decision_summary_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_decision_summary.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Decision summary generated." in result.stdout
    assert (ROOT / "data" / "decision_summary.csv").exists()
    assert (ROOT / "warehouse" / "decision" / "decision_summary.csv").exists()
