from __future__ import annotations

from pathlib import Path
from datetime import UTC, datetime

import pandas as pd

LABELS = Path("data/true_outcome_labels_v1.csv")

OUT = Path("data/outcome_maturity_monitor_v1.csv")
REPORT = Path("reports/outcome_maturity_monitor_v1.md")


def main() -> None:
    if not LABELS.exists():
        raise SystemExit("true_outcome_labels_v1.csv missing")

    df = pd.read_csv(LABELS)

    now = datetime.now(UTC)

    matured = 0
    pending = 0
    missing_timestamp = 0

    rows = []

    for _, row in df.iterrows():

        ts = str(row.get("target_timestamp", "")).strip()

        matured_now = False

        if ts:
            try:
                target = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                matured_now = target <= now
            except Exception:
                matured_now = False
        else:
            missing_timestamp += 1

        if matured_now:
            matured += 1
        else:
            pending += 1

        rows.append(
            {
                "snapshot_id": row.get("snapshot_id"),
                "provider": row.get("provider"),
                "gpu": row.get("gpu"),
                "label_status": row.get("label_status"),
                "target_timestamp": ts,
                "window_matured": matured_now,
            }
        )

    out = pd.DataFrame(rows)

    summary = pd.DataFrame(
        [
            {
                "generated_at": now.isoformat(),
                "rows": len(out),
                "matured_windows": matured,
                "pending_windows": pending,
                "missing_target_timestamp": missing_timestamp,
            }
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)
    summary.to_csv(
        "data/outcome_maturity_summary_v1.csv",
        index=False,
    )

    REPORT.write_text(
        "\n".join(
            [
                "# Outcome Maturity Monitor v1",
                "",
                f"Rows: {len(out)}",
                f"Matured windows: {matured}",
                f"Pending windows: {pending}",
                "",
                "## CTO Assessment",
                "",
                "This monitor determines when future labels become eligible for ML training.",
                "Training Dataset v3 should only become READY after mature outcome windows exist.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("OUTCOME MATURITY MONITOR V1")
    print("===========================")
    print(summary)


if __name__ == "__main__":
    main()
