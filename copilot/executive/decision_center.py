from __future__ import annotations

from datetime import datetime, timezone

from copilot.change_intelligence import get_change_intelligence
from copilot.executive.intelligence import (
    get_executive_intelligence,
)
from copilot.executive.recommendation import (
    get_executive_recommendation,
)
from copilot.executive.snapshot import (
    get_executive_snapshots,
)
from copilot.forecast_intelligence import get_forecast_intelligence
from copilot.risk_intelligence import get_risk_intelligence
from copilot.schemas import ExecutiveSummary
from copilot.status import get_status


def _calculate_executive_health(
    risk_score: int,
    forecast_watch_count: int,
    platform_status: str,
) -> int:
    score = 100

    if risk_score < 80:
        score -= 15

    if risk_score < 60:
        score -= 15

    if forecast_watch_count > 0:
        score -= 10

    if platform_status.lower() != "healthy":
        score -= 10

    return max(0, score)


def _executive_action(
    risk_score: int,
    forecast_watch_count: int,
    priority: str,
) -> str:
    if risk_score < 60:
        return "Escalate risk review and prepare executive mitigation plan."

    if forecast_watch_count > 0:
        return "Review forecast watch signals and validate capacity readiness."

    if priority.lower() == "high":
        return "Prioritize current recommendation and monitor execution."

    return "Continue monitoring current executive intelligence signals."


def get_executive_decision_center() -> dict:
    risk = get_risk_intelligence()
    recommendation = get_executive_recommendation()
    changes = get_change_intelligence()
    snapshots = get_executive_snapshots()
    executive = get_executive_intelligence()
    forecast = get_forecast_intelligence()
    status = get_status()

    risk_score = risk["summary"]["risk_score"]
    risk_severity = risk["summary"]["risk_severity"]
    priority = recommendation["summary"]["priority"]
    forecast_watch_count = forecast["summary"].get("watch_count", 0)
    platform_status = status.get("platform_status", "unknown")

    executive_health_score = _calculate_executive_health(
        risk_score=risk_score,
        forecast_watch_count=forecast_watch_count,
        platform_status=platform_status,
    )

    executive_action = _executive_action(
        risk_score=risk_score,
        forecast_watch_count=forecast_watch_count,
        priority=priority,
    )

    summary: ExecutiveSummary = {
        "status": "executive decision center available",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_risk_score": risk_score,
        "overall_risk_severity": risk_severity,
        "overall_recommendation": (
            recommendation["recommendation"]["action"]
        ),
    }

    return {
        "summary": summary,
        "metadata": {
            "version": "2.0",
            "module": "executive",
            "generated_by": "AI-RPCT Copilot",
        },
        "priority": priority,
        "executive_health": {
            "score": executive_health_score,
            "action": executive_action,
            "platform_status": platform_status,
            "forecast_watch_count": forecast_watch_count,
            "risk_score": risk_score,
            "risk_severity": risk_severity,
        },
        "kpis": {
            "snapshot_count": (
                snapshots["summary"]["snapshot_count"]
                if "summary" in snapshots
                else 0
            ),
            "change_events": len(changes["changes"]),
            "risk_score": risk_score,
            "priority": priority,
            "forecast_watch_count": forecast_watch_count,
            "executive_health_score": executive_health_score,
        },
        "risk": risk,
        "forecast": forecast,
        "status": status,
        "recommendation": recommendation,
        "changes": changes,
        "snapshots": snapshots,
        "executive_intelligence": executive,
    }
