import json
from pathlib import Path

import pandas as pd

from scripts.provider_env_check import build_provider_env_check
from scripts.provider_recovery_plan import build_provider_recovery_plan


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
    provenance_audit = read_latest(DATA_DIR / "core_provenance_audit.csv")
    paid_beta_gate = read_latest(DATA_DIR / "paid_beta_gate.csv")
    coverage_universe = read_latest(DATA_DIR / "coverage_universe_status.csv")
    manual_snapshot_quality = read_latest(DATA_DIR / "manual_snapshot_quality.csv")
    snapshot_collection_plan = read_records(DATA_DIR / "snapshot_collection_plan.csv", limit=5)
    gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv", limit=5)
    preflight = read_records(DATA_DIR / "provider_preflight.csv", limit=10)
    env_check = build_provider_env_check()
    recovery_plan = build_provider_recovery_plan()
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
        "provenance_band": provenance_audit.get("provenance_band"),
        "fallback_row_pct": provenance_audit.get("fallback_row_pct"),
        "provenance_blockers": provenance_audit.get("blockers"),
        "paid_beta_gate": {
            "allowed": paid_beta_gate.get("paid_beta_allowed", False),
            "status": paid_beta_gate.get("gate_status", "unknown"),
            "blockers": paid_beta_gate.get("blockers", "unknown"),
            "next_action": paid_beta_gate.get("next_action"),
        },
        "provider_credentials": {
            "configured_count": env_check.get("configured_count"),
            "required_count": env_check.get("required_count"),
            "all_required_configured": env_check.get("all_required_configured"),
        },
        "provider_recovery_plan": {
            "status": recovery_plan.get("status"),
            "configured_count": recovery_plan.get("configured_count"),
            "verified_live_count": recovery_plan.get("verified_live_count"),
            "missing_credentials": recovery_plan.get("missing_credentials", []),
            "next_action": recovery_plan.get("next_action"),
        },
        "coverage_universe": {
            "status": coverage_universe.get("status", "unknown"),
            "gpu_universe_count": coverage_universe.get("gpu_universe_count"),
            "provider_universe_count": coverage_universe.get("provider_universe_count"),
            "region_universe_count": coverage_universe.get("region_universe_count"),
            "manual_snapshot_count": coverage_universe.get("manual_snapshot_count"),
            "valid_manual_snapshot_count": coverage_universe.get("valid_manual_snapshot_count"),
            "history_policy": coverage_universe.get("history_policy"),
            "next_action": coverage_universe.get("next_action"),
        },
        "manual_snapshot_quality": {
            "status": manual_snapshot_quality.get("status", "unknown"),
            "snapshot_count": manual_snapshot_quality.get("snapshot_count"),
            "valid_snapshot_count": manual_snapshot_quality.get("valid_snapshot_count"),
            "invalid_snapshot_count": manual_snapshot_quality.get("invalid_snapshot_count"),
            "blockers": manual_snapshot_quality.get("blockers"),
            "next_action": manual_snapshot_quality.get("next_action"),
        },
        "snapshot_collection_plan": snapshot_collection_plan,
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

    paid_beta_gate = read_latest(DATA_DIR / "paid_beta_gate.csv")
    if paid_beta_gate and str(paid_beta_gate.get("gate_status", "")).lower() != "ready":
        actions.append({
            "priority": "critical",
            "source": "paid_beta_gate",
            "action": paid_beta_gate.get("next_action"),
            "provider": "all",
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
