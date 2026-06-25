from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "reports" / "analytics_dashboard.md"


def test_analytics_dashboard_builder_runs():
    subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "run_analytics_queries.py")],
        cwd=ROOT,
        check=True,
    )

    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_analytics_dashboard.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert REPORT.exists()
    assert "Analytics dashboard generated." in result.stdout


def test_dashboard_contains_governance():
    text = REPORT.read_text(encoding="utf-8")

    assert "# AI-RPCT Analytics Dashboard" in text
    assert "## Governance" in text
    assert "no ML training" in text
