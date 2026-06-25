from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "reports" / "analytics_queries.md"


def test_analytics_queries_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "run_analytics_queries.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert REPORT.exists()
    assert "Analytics report generated." in result.stdout


def test_report_contains_counts():
    text = REPORT.read_text(encoding="utf-8")

    assert "Feature Store" in text
    assert "Providers" in text
    assert "Accelerators" in text
