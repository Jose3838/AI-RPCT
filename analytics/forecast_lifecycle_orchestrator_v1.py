from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("data/forecast_lifecycle_orchestrator_v1.csv")
REPORT = Path("reports/forecast_lifecycle_orchestrator_v1.md")

STEPS = [
    "analytics/forecast_snapshot_store_v1.py",
    "analytics/forecast_outcome_tracker_v1.py",
    "analytics/forecast_outcome_windows_v1.py",
    "analytics/true_outcome_label_builder_v1.py",
    "analytics/outcome_maturity_monitor_v1.py",
    "analytics/true_outcome_resolver_v1.py",
    "analytics/training_dataset_builder_v3.py",
]


def run_step(script: str) -> dict:
    started_at = datetime.now(UTC).isoformat()

    if not Path(script).exists():
        return {
            "script": script,
            "status": "missing",
            "started_at": started_at,
            "finished_at": datetime.now(UTC).isoformat(),
            "returncode": "",
            "error": "script_not_found",
        }

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
    )

    return {
        "script": script,
        "status": "ok" if result.returncode == 0 else "failed",
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "returncode": result.returncode,
        "error": result.stderr.strip(),
    }


def main() -> None:
    rows = [run_step(step) for step in STEPS]

    df = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    failed = int((df["status"] == "failed").sum())
    missing = int((df["status"] == "missing").sum())
    ok = int((df["status"] == "ok").sum())

    REPORT.write_text(
        "\n".join([
            "# Forecast Lifecycle Orchestrator v1",
            "",
            f"OK steps: {ok}",
            f"Failed steps: {failed}",
            f"Missing steps: {missing}",
            "",
            "## Lifecycle",
            "",
            "Forecast snapshot → outcome tracking → outcome windows → true labels → maturity monitor → resolver → training dataset v3.",
            "",
            "## CTO Assessment",
            "",
            "This orchestrator closes the continuous-learning forecast lifecycle.",
            "It should be called from daily collection after forecasts and market-regime outputs are refreshed.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST LIFECYCLE ORCHESTRATOR V1")
    print("==================================")
    print(df)


if __name__ == "__main__":
    main()
