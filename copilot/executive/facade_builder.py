from __future__ import annotations


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
