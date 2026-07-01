from __future__ import annotations

from collections import Counter

from copilot.io import load_csv


def get_forecast_intelligence() -> dict:
    rows = load_csv("data/forecast_engine_v1_output.csv")

    if not rows:
        return {
            "status": "no forecast intelligence available"
        }

    forecast_classes = Counter()
    rule_based_signals = Counter()
    governance_statuses = Counter()
    confidence_levels = Counter()
    provider_ids = set()
    entity_ids = set()

    for row in rows:
        forecast_class = row.get("forecast_class")
        rule_based_signal = row.get("rule_based_signal")
        governance_status = row.get("governance_status")
        confidence_level = row.get("confidence_level")
        provider_id = row.get("provider_id")
        entity_id = row.get("entity_id")

        if forecast_class:
            forecast_classes[forecast_class] += 1

        if rule_based_signal:
            rule_based_signals[rule_based_signal] += 1

        if governance_status:
            governance_statuses[governance_status] += 1

        if confidence_level:
            confidence_levels[confidence_level] += 1

        if provider_id:
            provider_ids.add(provider_id)

        if entity_id:
            entity_ids.add(entity_id)

    watch_count = forecast_classes.get("watch", 0)
    monitor_count = forecast_classes.get("monitor_only", 0)

    latest = rows[-1]

    insight = (
        f"Forecast intelligence is available across {len(rows)} records, "
        f"covering {len(provider_ids)} providers and {len(entity_ids)} entities."
    )

    if watch_count:
        insight += (
            f" {watch_count} forecast record(s) require watch-level attention."
        )

    return {
        "summary": {
            "status": "forecast intelligence available",
            "forecast_count": len(rows),
            "provider_count": len(provider_ids),
            "entity_count": len(entity_ids),
            "watch_count": watch_count,
            "monitor_count": monitor_count,
            "latest_forecast_class": latest.get("forecast_class"),
            "latest_signal": latest.get("rule_based_signal"),
        },
        "metrics": {
            "forecast_classes": dict(forecast_classes),
            "rule_based_signals": dict(rule_based_signals),
            "governance_statuses": dict(governance_statuses),
            "confidence_levels": dict(confidence_levels),
        },
        "trends": {
            "forecast_classes": dict(forecast_classes),
            "rule_based_signals": dict(rule_based_signals),
        },
        "insights": [
            {
                "type": "forecast",
                "severity": "info",
                "message": insight,
            }
        ],
    }
