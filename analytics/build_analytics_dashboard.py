from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "reports" / "analytics_queries.md"
OUTPUT = ROOT / "reports" / "analytics_dashboard.md"


def main():
    source = INPUT.read_text(encoding="utf-8")

    lines = [
        "# AI-RPCT Analytics Dashboard",
        "",
        "## Generated UTC",
        "",
        datetime.now(UTC).isoformat(),
        "",
        "## Analytics Summary",
        "",
        source,
        "",
        "## Governance",
        "",
        "- SQL analytics only",
        "- no ML training",
        "- no accuracy claims",
        "- no paid production promotion",
    ]

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print("Analytics dashboard generated.")
    print(OUTPUT)


if __name__ == "__main__":
    main()
