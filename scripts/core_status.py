import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_records(path, limit=5):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).head(limit).to_dict(orient="records")


def build_core_status():
    readiness = read_latest(DATA_DIR / "core_intelligence_readiness.csv")
    quality = read_latest(DATA_DIR / "core_signal_quality.csv")
    pulse = read_latest(DATA_DIR / "market_pulse_history.csv")
    history_audit = read_latest(DATA_DIR / "core_history_audit.csv")
    gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv", limit=5)
    preflight = read_records(DATA_DIR / "provider_preflight.csv", limit=10)
    action_plan = build_action_plan(readiness, gaps, preflight)

    return {
        "product": "AI-RPCT",
        "readiness_phase": readiness.get("readiness_phase", "unknown"),
        "core_signal_quality_score": readiness.get("core_signal_quality_score", quality.get("core_signal_quality_score")),
        "quality_band": readiness.get("quality_band", quality.get("quality_band", "unknown")),
        "market_pulse_score": readiness.get("market_pulse_score", pulse.get("market_pulse_score")),
        "history_progress_pct": history_audit.get("progress_pct"),
        "history_days_remaining": history_audit.get("days_remaining"),
        "history_band": history_audit.get("history_band"),
        "paid_beta_signal_ready": readiness.get("paid_beta_signal_ready", False),
        "blockers": readiness.get("blockers", quality.get("blockers", "unknown")),
        "next_action": readiness.get("next_action", "Run ./scripts/run_core_intelligence.sh"),
        "action_plan": action_plan,
        "top_provider_gaps": gaps,
    }


def build_action_plan(readiness, gaps, preflight):
    actions = []
    for row in preflight:
        if row.get("readiness") == "blocked":
            actions.append({
                "priority": "critical",
                "source": "provider_preflight",
                "action": row.get("next_action"),
                "provider": row.get("provider"),
            })

    for gap in gaps:
        if gap.get("priority") in {"high", "critical"}:
            actions.append({
                "priority": gap.get("priority"),
                "source": "provider_reliability_gap",
                "action": gap.get("recommended_action"),
                "provider": gap.get("provider"),
                "gap": gap.get("gap"),
            })

    blockers = str(readiness.get("blockers", ""))
    if "collect_30_days_of_core_signal_history" in blockers:
        actions.append({
            "priority": "high",
            "source": "core_signal_history",
            "action": "Run the core intelligence pipeline daily until 30 clean history days are collected.",
            "provider": "all",
        })

    if not actions:
        actions.append({
            "priority": "low",
            "source": "core_status",
            "action": "Maintain daily monitoring.",
            "provider": "all",
        })

    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    actions = sorted(actions, key=lambda item: priority_order.get(item.get("priority"), 9))

    deduped = []
    seen = set()
    for action in actions:
        key = (action.get("provider"), action.get("action"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(action)
    return deduped[:5]


def main():
    print(json.dumps(build_core_status(), indent=2, default=str))


if __name__ == "__main__":
    main()
