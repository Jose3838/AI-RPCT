from __future__ import annotations


def build_strategic_signals(
    risk: dict,
    forecast: dict,
    analytics: dict,
    executive_health: dict,
) -> list[dict]:
    signals = []

    risk_score = risk.get("summary", {}).get("risk_score", 0)
    forecast_watch_count = forecast.get("summary", {}).get("watch_count", 0)
    stability_score = analytics.get("decision_stability_score")
    health_score = executive_health.get("score", 0)

    if health_score >= 90:
        signals.append(
            {
                "type": "platform",
                "severity": "positive",
                "label": "Stable Platform",
                "message": (
                    "Executive health is strong and platform status is stable."
                ),
            }
        )

    if risk_score >= 80:
        signals.append(
            {
                "type": "risk",
                "severity": "info",
                "label": "Risk Under Control",
                "message": f"Executive risk score is currently {risk_score}/100.",
            }
        )

    if forecast_watch_count > 0:
        signals.append(
            {
                "type": "forecast",
                "severity": "warning",
                "label": "Capacity Watch",
                "message": (
                    f"{forecast_watch_count} forecast signal(s) require "
                    "capacity monitoring."
                ),
            }
        )

    if stability_score == 1:
        signals.append(
            {
                "type": "decision",
                "severity": "positive",
                "label": "Decision Stability",
                "message": (
                    "Executive recommendations are stable across history."
                ),
            }
        )

    if not signals:
        signals.append(
            {
                "type": "platform",
                "severity": "info",
                "label": "No Strategic Signals",
                "message": "No elevated strategic signals detected.",
            }
        )

    return signals


def build_changes(changes: dict) -> dict:
    return {
        "summary": changes.get("summary", {}),
        "metrics": changes.get("metrics", {}),
        "changes": changes.get("changes", []),
        "insights": changes.get("insights", []),
    }


def build_trend(trend: dict) -> dict:
    return {
        "summary": trend.get("summary", {}),
        "trends": trend.get("trends", {}),
        "insights": trend.get("insights", []),
    }


def build_snapshot_summary(snapshot_summary: dict) -> dict:
    return {
        "latest_snapshot": snapshot_summary.get("latest_snapshot"),
        "snapshot_count": snapshot_summary.get("snapshot_count", 0),
    }
