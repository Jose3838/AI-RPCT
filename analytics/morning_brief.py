from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from scripts.scheduler_health import build_scheduler_health


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


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


def value(row, key, fallback="n/a"):
    item = row.get(key, fallback)
    if pd.isna(item):
        return fallback
    return item


def build_morning_brief():
    generated_at = datetime.now().isoformat()
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    reliability = read_latest(DATA_DIR / "provider_reliability_ranking.csv")
    readiness = read_latest(DATA_DIR / "core_intelligence_readiness.csv")
    cadence = read_latest(DATA_DIR / "collection_cadence_audit.csv")
    scheduler = build_scheduler_health()
    paid_gate = read_latest(DATA_DIR / "paid_beta_gate.csv")
    coverage = read_latest(DATA_DIR / "coverage_universe_status.csv")
    snapshot_quality = read_latest(DATA_DIR / "manual_snapshot_quality.csv")
    provider_gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv", limit=3)
    snapshot_targets = read_records(DATA_DIR / "snapshot_collection_plan.csv", limit=5)

    scarcity_score = value(scarcity, "gpu_scarcity_index")
    scarcity_band = value(scarcity, "scarcity_band")
    forecast_score = value(forecast, "forecast_score")
    shock_band = value(forecast, "capacity_shock_band")
    readiness_phase = value(readiness, "readiness_phase")
    cadence_status = value(cadence, "status")
    days_collected = value(cadence, "days_collected", 0)
    days_to_next = value(cadence, "days_to_next_milestone", "n/a")
    paid_status = value(paid_gate, "gate_status")
    scheduler_status = value(scheduler, "status", "unknown")

    headline = (
        f"AI infrastructure stress is {scarcity_band}; "
        f"capacity shock signal is {shock_band}; "
        f"history moat is building ({days_collected} days)."
    )

    if paid_status == "ready":
        operating_mode = "paid_beta_candidate"
        today_action = "Prepare controlled paid-beta customer validation."
    elif snapshot_quality.get("status") in {"no_snapshots", "snapshots_need_cleanup"}:
        operating_mode = "research_preview_data_collection"
        today_action = snapshot_quality.get(
            "next_action",
            "Collect source-labeled manual snapshots for priority GPUs, providers and regions.",
        )
    elif scheduler_status != "healthy":
        operating_mode = "scheduler_attention_needed"
        today_action = "Fix scheduler health before relying on unattended daily collection."
    else:
        operating_mode = "research_preview"
        today_action = cadence.get("next_action", readiness.get("next_action", "Maintain daily collection."))

    provider_gap_lines = [
        f"- {gap.get('provider', 'unknown')}: {gap.get('gap', 'unknown')} -> {gap.get('recommended_action', 'n/a')}"
        for gap in provider_gaps
    ] or ["- No provider reliability gaps available."]
    target_lines = [
        f"- {target.get('provider')} / {target.get('gpu')} / {target.get('region_code')}"
        for target in snapshot_targets
    ] or ["- No snapshot targets available."]

    markdown = "\n".join([
        "# AI-RPCT Morning Brief",
        "",
        f"Generated: {generated_at}",
        "",
        "## Headline",
        headline,
        "",
        "## Market Pulse",
        f"- GPU Scarcity Index: {scarcity_score} ({scarcity_band})",
        f"- Capacity Forecast Score: {forecast_score} ({shock_band})",
        f"- Reliability Leader: {value(reliability, 'provider')} ({value(reliability, 'reliability_score')})",
        "",
        "## Trust And Moat",
        f"- Readiness Phase: {readiness_phase}",
        f"- Paid Beta Gate: {paid_status}",
        f"- Scheduler: {scheduler_status}",
        f"- Collection Cadence: {cadence_status}",
        f"- Days Collected: {days_collected}",
        f"- Days To Next Milestone: {days_to_next}",
        f"- Coverage Status: {value(coverage, 'status')}",
        f"- Manual Snapshot Quality: {value(snapshot_quality, 'status')}",
        "",
        "## Top Provider Risks",
        *provider_gap_lines,
        "",
        "## Next Snapshot Targets",
        *target_lines,
        "",
        "## Today's Operating Mode",
        operating_mode,
        "",
        "## Today's Action",
        today_action,
    ])

    return {
        "product": "AI-RPCT",
        "report_type": "morning_brief",
        "generated_at": generated_at,
        "headline": headline,
        "operating_mode": operating_mode,
        "today_action": today_action,
        "scarcity_band": scarcity_band,
        "capacity_shock_band": shock_band,
        "readiness_phase": readiness_phase,
        "paid_beta_gate_status": paid_status,
        "scheduler_status": scheduler_status,
        "collection_cadence_status": cadence_status,
        "days_collected": days_collected,
        "days_to_next_milestone": days_to_next,
        "markdown": markdown,
    }


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    brief = build_morning_brief()
    path = REPORTS_DIR / f"morning_brief_{datetime.now().strftime('%Y%m%d')}.md"
    path.write_text(brief["markdown"])
    print(pd.DataFrame([{key: value for key, value in brief.items() if key != "markdown"}]))


if __name__ == "__main__":
    main()
