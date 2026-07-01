from __future__ import annotations

from copilot.executive.snapshot import (
    get_executive_snapshots,
)


def _build_alerts(
    current_score: int,
    delta: int | None,
    snapshot_count: int,
) -> list[dict]:
    alerts = []

    if current_score >= 80:
        alerts.append(
            {
                "type": "risk",
                "severity": "critical",
                "message": (
                    f"Executive risk score is elevated at "
                    f"{current_score}/100."
                ),
            }
        )
    elif current_score >= 60:
        alerts.append(
            {
                "type": "risk",
                "severity": "warning",
                "message": (
                    f"Executive risk score requires monitoring at "
                    f"{current_score}/100."
                ),
            }
        )

    if delta is not None and delta > 0:
        alerts.append(
            {
                "type": "trend",
                "severity": "warning",
                "message": (
                    f"Risk score increased by {delta} point(s) "
                    "since the previous executive snapshot."
                ),
            }
        )

    if delta == 0:
        alerts.append(
            {
                "type": "trend",
                "severity": "info",
                "message": (
                    "Risk score is stable compared with the previous "
                    "executive snapshot."
                ),
            }
        )

    if snapshot_count >= 2:
        alerts.append(
            {
                "type": "history",
                "severity": "info",
                "message": (
                    f"Executive change intelligence is based on "
                    f"{snapshot_count} snapshots."
                ),
            }
        )

    return alerts


def get_change_intelligence() -> dict:
    snapshots = get_executive_snapshots()

    if "snapshots" not in snapshots:
        return {
            "summary": {
                "status": "change intelligence unavailable",
                "baseline": "no executive snapshots available",
                "snapshot_count": 0,
            },
            "metrics": {},
            "changes": [],
            "alerts": [],
            "insights": [],
        }

    rows = snapshots["snapshots"]
    snapshot_count = len(rows)

    if snapshot_count < 2:
        latest = rows[-1]
        current_score = int(latest["risk_score"])

        return {
            "summary": {
                "status": "change intelligence available",
                "baseline": "single executive snapshot",
                "snapshot_count": snapshot_count,
            },
            "metrics": {
                "risk_score": current_score,
                "risk_severity": latest["risk_severity"],
            },
            "changes": [],
            "alerts": _build_alerts(
                current_score=current_score,
                delta=None,
                snapshot_count=snapshot_count,
            ),
            "insights": [
                {
                    "type": "change",
                    "severity": "info",
                    "message": (
                        "Only one executive snapshot is available. "
                        "Historical comparison requires at least two snapshots."
                    ),
                }
            ],
        }

    previous = rows[-2]
    current = rows[-1]

    previous_score = int(previous["risk_score"])
    current_score = int(current["risk_score"])
    delta = current_score - previous_score

    changes = [
        {
            "metric": "risk_score",
            "previous": previous_score,
            "current": current_score,
            "delta": delta,
            "severity": "info",
        }
    ]

    if previous["risk_severity"] != current["risk_severity"]:
        changes.append(
            {
                "metric": "risk_severity",
                "previous": previous["risk_severity"],
                "current": current["risk_severity"],
                "severity": "info",
            }
        )

    if previous["recommendation"] != current["recommendation"]:
        changes.append(
            {
                "metric": "recommendation",
                "previous": previous["recommendation"],
                "current": current["recommendation"],
                "severity": "info",
            }
        )

    return {
        "summary": {
            "status": "change intelligence available",
            "baseline": "latest two executive snapshots",
            "snapshot_count": snapshot_count,
        },
        "metrics": {
            "risk_score": current_score,
            "risk_severity": current["risk_severity"],
        },
        "changes": changes,
        "alerts": _build_alerts(
            current_score=current_score,
            delta=delta,
            snapshot_count=snapshot_count,
        ),
        "insights": [
            {
                "type": "change",
                "severity": "info",
                "message": (
                    f"Risk score changed by {delta} points "
                    f"between the latest two of {snapshot_count} "
                    "executive snapshots."
                ),
            }
        ],
    }
