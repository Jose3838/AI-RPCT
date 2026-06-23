import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analytics.research_preview_brief import build_research_preview_brief
from scripts.core_status import build_core_status
from scripts.manual_snapshot_template_check import build_manual_snapshot_template_check


def build_founder_daily_close():
    core = build_core_status()
    preview = build_research_preview_brief()
    cadence = core.get("collection_cadence", {})
    coverage = core.get("coverage_universe", {})
    snapshot_quality = core.get("manual_snapshot_quality", {})
    paid_gate = core.get("paid_beta_gate", {})
    recovery = core.get("provider_recovery_plan", {})
    scheduler = core.get("scheduler_health", {})
    snapshot_plan = core.get("snapshot_collection_plan", [])
    template_check = build_manual_snapshot_template_check()
    action_plan = core.get("action_plan", [])

    tomorrow_focus = preview.get("next_action") or core.get("next_action")
    if template_check.get("status") in {
        "template_needs_sources",
        "template_partially_ready",
        "ready_to_copy",
        "template_missing_or_empty",
    }:
        tomorrow_focus = template_check.get("next_action", tomorrow_focus)
    if (
        preview.get("preview_status") != "snapshot_collection_needed"
        and action_plan
    ):
        tomorrow_focus = action_plan[0].get("action", tomorrow_focus)

    return {
        "product": "AI-RPCT",
        "report_type": "founder_daily_close",
        "status": "saved_for_next_session",
        "readiness_phase": core.get("readiness_phase"),
        "collection_cadence_status": cadence.get("status"),
        "collection_days_collected": cadence.get("days_collected"),
        "collection_current_streak_days": cadence.get("current_streak_days"),
        "collection_missing_day_count": cadence.get("missing_day_count"),
        "research_preview_status": preview.get("preview_status"),
        "paid_beta_gate_status": paid_gate.get("status"),
        "paid_beta_allowed": paid_gate.get("allowed", False),
        "provider_recovery_status": recovery.get("status"),
        "missing_provider_credentials": recovery.get("missing_credentials", []),
        "scheduler_status": scheduler.get("status"),
        "scheduler_last_run_completed": scheduler.get("last_run_completed"),
        "scheduler_next_action": scheduler.get("next_action"),
        "coverage_status": coverage.get("status"),
        "gpu_universe_count": coverage.get("gpu_universe_count"),
        "provider_universe_count": coverage.get("provider_universe_count"),
        "region_universe_count": coverage.get("region_universe_count"),
        "manual_snapshot_quality_status": snapshot_quality.get("status"),
        "valid_manual_snapshot_count": snapshot_quality.get("valid_snapshot_count"),
        "manual_snapshot_template_status": template_check.get("status"),
        "manual_snapshot_template_valid_rows": template_check.get("valid_row_count"),
        "manual_snapshot_template_rejected_rows": template_check.get("rejected_row_count"),
        "snapshot_collection_targets": snapshot_plan[:5],
        "history_policy": coverage.get("history_policy"),
        "tomorrow_focus": tomorrow_focus,
        "top_actions": action_plan[:5],
        "do_not_claim_yet": preview.get("unsafe_claims", []),
    }


def main():
    print(json.dumps(build_founder_daily_close(), indent=2, default=str))


if __name__ == "__main__":
    main()
