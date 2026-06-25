from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pandas as pd

TRACKER = Path("data/forecast_outcome_tracker_v1.csv")
OUT = Path("data/forecast_outcome_windows_v1.csv")
REPORT = Path("reports/forecast_outcome_windows_v1.md")

WINDOW_DAYS = [7, 14, 30]


def main() -> None:
    if not TRACKER.exists() or TRACKER.stat().st_size <= 1:
        raise SystemExit("forecast_outcome_tracker_v1.csv missing or empty")

    tracker = pd.read_csv(TRACKER)
    tracker["snapshot_timestamp"] = pd.to_datetime(tracker["snapshot_timestamp"], errors="coerce")

    rows = []

    for _, row in tracker.iterrows():
        base_ts = row["snapshot_timestamp"]

        if pd.isna(base_ts):
            continue

        for days in WINDOW_DAYS:
            rows.append({
                "snapshot_id": row.get("snapshot_id"),
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "forecast_signal": row.get("forecast_signal"),
                "confidence": row.get("confidence"),
                "baseline_market_regime": row.get("current_market_regime"),
                "window_days": days,
                "target_timestamp": (base_ts + timedelta(days=days)).isoformat(),
                "outcome_status": "awaiting_target_window",
            })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Forecast Outcome Windows v1",
            "",
            f"Outcome windows created: {len(out)}",
            "",
            "## Windows",
            "",
            "- 7 days",
            "- 14 days",
            "- 30 days",
            "",
            "## CTO Assessment",
            "",
            "This module creates future validation windows for every forecast snapshot.",
            "It turns forecast tracking into a measurable future-outcome process.",
            "",
            "## Next Step",
            "",
            "When target windows mature, compare forecast signals with observed market regimes.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST OUTCOME WINDOWS V1")
    print("===========================")
    print(f"Rows: {len(out)}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
