from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

LABELS = Path("data/true_outcome_labels_v1.csv")

OUT = Path("data/outcome_maturity_monitor_v1.csv")
SUMMARY = Path("data/outcome_maturity_summary_v1.csv")
REPORT = Path("reports/outcome_maturity_monitor_v1.md")


def parse_timestamp(value):
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except Exception:
        return None


def main() -> None:
    if not LABELS.exists() or LABELS.stat().st_size <= 1:
        raise SystemExit("true_outcome_labels_v1.csv missing or empty")

    labels = pd.read_csv(LABELS)
    now = datetime.now(UTC)

    rows = []

    for _, row in labels.iterrows():
        target = parse_timestamp(row.get("target_timestamp", ""))
        matured = bool(target and target <= now)

        rows.append({
            "snapshot_id": row.get("snapshot_id"),
            "provider": row.get("provider"),
            "gpu": row.get("gpu"),
            "window_days": row.get("window_days"),
            "target_timestamp": row.get("target_timestamp"),
            "label_status": row.get("label_status"),
            "window_matured": matured,
            "maturity_status": "matured_needs_resolution" if matured else "pending",
        })

    out = pd.DataFrame(rows)

    matured_count = int(out["window_matured"].sum()) if not out.empty else 0
    pending_count = int((~out["window_matured"]).sum()) if not out.empty else 0

    summary = {
        "generated_at": now.isoformat(),
        "total_windows": len(out),
        "matured_windows": matured_count,
        "pending_windows": pending_count,
        "next_action": (
            "Run true outcome resolver for matured windows."
            if matured_count > 0
            else "Continue collecting live data until outcome windows mature."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)
    pd.DataFrame([summary]).to_csv(SUMMARY, index=False)

    REPORT.write_text(
        "\n".join([
            "# Outcome Maturity Monitor v1",
            "",
            f"Total windows: {summary['total_windows']}",
            f"Matured windows: {summary['matured_windows']}",
            f"Pending windows: {summary['pending_windows']}",
            "",
            "## CTO Assessment",
            "",
            "This monitor checks whether forecast outcome windows have reached their target timestamp.",
            "Matured windows are not automatically trainable; they require a resolver to attach observed future market outcomes.",
            "",
            "## Next Action",
            "",
            summary["next_action"],
            "",
        ]),
        encoding="utf-8",
    )

    print("OUTCOME MATURITY MONITOR V1")
    print("===========================")
    print(pd.DataFrame([summary]))


if __name__ == "__main__":
    main()
