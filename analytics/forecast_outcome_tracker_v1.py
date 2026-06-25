from __future__ import annotations

from pathlib import Path

import pandas as pd

SNAPSHOT_INDEX = Path("data/forecast_snapshot_index.csv")
REGIME_PATH = Path("data/market_regime_v1.csv")
OUT = Path("data/forecast_outcome_tracker_v1.csv")
REPORT = Path("reports/forecast_outcome_tracker_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    index = read_csv(SNAPSHOT_INDEX)
    regimes = read_csv(REGIME_PATH)

    rows = []

    for _, snapshot in index.iterrows():
        snapshot_file = Path(snapshot["output_file"])
        forecasts = read_csv(snapshot_file)

        if forecasts.empty:
            continue

        merged = forecasts.merge(
            regimes[["provider", "gpu", "market_regime"]],
            on=["provider", "gpu"],
            how="left",
        )

        for _, row in merged.iterrows():
            rows.append({
                "snapshot_id": snapshot["snapshot_id"],
                "snapshot_timestamp": snapshot["snapshot_timestamp"],
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "forecast_signal": row.get("forecast_signal"),
                "confidence": row.get("confidence"),
                "current_market_regime": row.get("market_regime"),
                "tracking_status": "baseline_created",
            })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Forecast Outcome Tracker v1",
            "",
            f"Tracked rows: {len(out)}",
            "",
            "## CTO Assessment",
            "",
            "This tracker connects forecast snapshots with observed market regimes.",
            "It creates the baseline required for future true-outcome validation.",
            "",
            "## Next Step",
            "",
            "Add age windows: 7d, 14d, 30d outcome comparison.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST OUTCOME TRACKER V1")
    print("===========================")
    print(f"Tracked rows: {len(out)}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
