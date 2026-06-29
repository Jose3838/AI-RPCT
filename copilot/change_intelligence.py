from __future__ import annotations

from copilot.executive_snapshot import get_executive_snapshots


def get_change_intelligence() -> dict:
    snapshots = get_executive_snapshots()

    if "snapshots" not in snapshots:
        return {
            "summary": {
                "status": "change intelligence unavailable",
                "baseline": "no executive snapshots available",
            },
            "metrics": {},
            "changes": [],
            "insights": [],
        }

    rows = snapshots["snapshots"]

    if len(rows) < 2:
        latest = rows[-1]

        return {
            "summary": {
                "status": "change intelligence available",
                "baseline": "single executive snapshot",
            },
            "metrics": {
                "risk_score": int(latest["risk_score"]),
                "risk_severity": latest["risk_severity"],
            },
            "changes": [],
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
        },
        "metrics": {
            "risk_score": current_score,
            "risk_severity": current["risk_severity"],
        },
        "changes": changes,
        "insights": [
            {
                "type": "change",
                "severity": "info",
                "message": (
                    f"Risk score changed by {delta} points "
                    "between the latest two executive snapshots."
                ),
            }
        ],
    }
