from __future__ import annotations

from pathlib import Path

import pandas as pd

WINDOWS = Path("data/forecast_outcome_windows_v1.csv")
TRACKER = Path("data/forecast_outcome_tracker_v1.csv")

OUT = Path("data/true_outcome_labels_v1.csv")
REPORT = Path("reports/true_outcome_label_builder_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    windows = read_csv(WINDOWS)
    tracker = read_csv(TRACKER)

    rows = []

    if not windows.empty:
        for _, row in windows.iterrows():
            rows.append({
                "snapshot_id": row.get("snapshot_id"),
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "window_days": row.get("window_days"),
                "forecast_signal": row.get("forecast_signal"),
                "target_timestamp": row.get("target_timestamp"),
                "true_outcome_label": "",
                "label_status": "awaiting_future_observation",
                "label_source": "forecast_outcome_window",
                "is_trainable": False,
            })

    if not rows and not tracker.empty:
        for _, row in tracker.iterrows():
            rows.append({
                "snapshot_id": row.get("snapshot_id"),
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "window_days": "",
                "forecast_signal": row.get("forecast_signal"),
                "target_timestamp": "",
                "true_outcome_label": "",
                "label_status": "baseline_only_not_future_label",
                "label_source": "forecast_outcome_tracker",
                "is_trainable": False,
            })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    trainable = int(out["is_trainable"].sum()) if not out.empty else 0

    REPORT.write_text(
        "\n".join([
            "# True Outcome Label Builder v1",
            "",
            f"Rows: {len(out)}",
            f"Trainable labels: {trainable}",
            "",
            "## CTO Assessment",
            "",
            "This module separates true future outcome labels from current-state market regimes.",
            "No ML model should claim real predictive performance until labels become trainable after future windows mature.",
            "",
            "## Rule",
            "",
            "Current market regime is not a true future outcome label.",
            "",
        ]),
        encoding="utf-8",
    )

    print("TRUE OUTCOME LABEL BUILDER V1")
    print("=============================")
    print(f"Rows: {len(out)}")
    print(f"Trainable labels: {trainable}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
