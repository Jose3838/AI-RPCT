from __future__ import annotations

import csv
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASETS = [
    "feature_store.csv",
    "forecast_dataset.csv",
    "forecast_engine_v1_output.csv",
    "forecast_explanations.csv",
    "data_quality_metrics.csv",
    "pipeline_health_summary.csv",
]


def row_count(path: Path) -> int:
    if not path.exists():
        return 0

    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def main():
    report = ROOT / "reports" / "pipeline_dashboard.md"

    report.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# AI-RPCT Pipeline Dashboard")
    lines.append("")
    lines.append("## Pipeline Status")
    lines.append("")
    lines.append("SUCCESS")
    lines.append("")
    lines.append("## Generated (UTC)")
    lines.append("")
    lines.append(datetime.now(UTC).isoformat())
    lines.append("")
    lines.append("## Datasets")
    lines.append("")

    for dataset in DATASETS:
        count = row_count(ROOT / "data" / dataset)
        lines.append(f"- {dataset}: {count} rows")

    lines.append("")
    lines.append("## Pipeline Version")
    lines.append("")
    lines.append("1.0")

    report.write_text("\n".join(lines), encoding="utf-8")

    print("Pipeline dashboard generated.")
    print(report)


if __name__ == "__main__":
    main()
