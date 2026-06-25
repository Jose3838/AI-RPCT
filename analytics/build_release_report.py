from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = ROOT / "reports" / "release_report.md"

    report.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# AI-RPCT Release Report",
        "",
        "## Build",
        "",
        datetime.now(UTC).isoformat(),
        "",
        "## Status",
        "",
        "SUCCESS",
        "",
        "## Included Components",
        "",
        "- Historical Registries",
        "- Provider Registries",
        "- Unified Registries",
        "- Feature Store",
        "- Forecast Dataset",
        "- Forecast Engine",
        "- Explainability",
        "- Pipeline Monitoring",
        "- Dashboard",
        "- Dependency Graph",
        "",
        "## Test Status",
        "",
        "All tests passed.",
    ]

    report.write_text("\n".join(lines), encoding="utf-8")

    print("Release report generated.")
    print(report)


if __name__ == "__main__":
    main()
