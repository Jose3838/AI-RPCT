from __future__ import annotations

from copilot.io import load_csv


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_executive_trend() -> dict:
    decision_rows = load_csv("data/decision_history.csv")
    snapshot_rows = load_csv("data/executive_snapshot_registry.csv")
    forecast_rows = load_csv("data/forecast_engine_v1_output.csv")

    confidence_history = []

    for row in decision_rows:
        confidence = _to_float(row.get("confidence"))

        if confidence is None:
            continue

        confidence_history.append(
            {
                "generated_at": (
                    row.get("generated_at")
                    or row.get("timestamp")
                    or row.get("created_at")
                ),
                "confidence": confidence,
            }
        )

    risk_history = []

    for row in snapshot_rows:
        risk_score = _to_float(
            row.get("risk_score")
            or row.get("overall_risk_score")
        )

        if risk_score is None:
            continue

        risk_history.append(
            {
                "generated_at": (
                    row.get("generated_at")
                    or row.get("timestamp")
                    or row.get("created_at")
                ),
                "risk_score": risk_score,
            }
        )

    forecast_watch_count = 0

    for row in forecast_rows:
        if row.get("forecast_class") == "watch":
            forecast_watch_count += 1

    latest_confidence = (
        confidence_history[-1]["confidence"]
        if confidence_history
        else None
    )

    latest_risk_score = (
        risk_history[-1]["risk_score"]
        if risk_history
        else None
    )

    return {
        "summary": {
            "status": "executive trend available",
            "decision_points": len(confidence_history),
            "risk_points": len(risk_history),
            "forecast_watch_count": forecast_watch_count,
            "latest_confidence": latest_confidence,
            "latest_risk_score": latest_risk_score,
        },
        "trends": {
            "confidence_history": confidence_history,
            "risk_history": risk_history,
            "forecast_watch_count": forecast_watch_count,
        },
        "insights": [
            {
                "type": "trend",
                "severity": "info",
                "message": (
                    "Executive trend data is available from decision history, "
                    "executive snapshots, and forecast output."
                ),
            }
        ],
    }
