from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from scripts.scheduler_health import build_scheduler_health


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
SUMMARY_FILE = DATA_DIR / "morning_brief_summary.csv"


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
    price_dislocation = read_latest(DATA_DIR / "price_dislocation_signal.csv")
    stress = read_latest(DATA_DIR / "ai_infrastructure_stress_index.csv")
    reliability = read_latest(DATA_DIR / "provider_reliability_ranking.csv")
    readiness = read_latest(DATA_DIR / "core_intelligence_readiness.csv")
    cadence = read_latest(DATA_DIR / "collection_cadence_audit.csv")
    scheduler = build_scheduler_health()
    paid_gate = read_latest(DATA_DIR / "paid_beta_gate.csv")
    coverage = read_latest(DATA_DIR / "coverage_universe_status.csv")
    snapshot_quality = read_latest(DATA_DIR / "manual_snapshot_quality.csv")
    source_coverage = read_latest(DATA_DIR / "source_url_coverage_metrics.csv")
    source_backed_scarcity = read_latest(DATA_DIR / "source_backed_scarcity.csv")
    signal_performance = read_latest(DATA_DIR / "signal_performance_score.csv")
    alerts = read_records(DATA_DIR / "core_intelligence_alerts.csv", limit=5)
    claim_gates = read_records(DATA_DIR / "claim_gate_matrix.csv", limit=10)
    region_heatmap = read_records(DATA_DIR / "region_scarcity_heatmap.csv", limit=10)
    forecast_accuracy = read_latest(DATA_DIR / "forecast_accuracy.csv")
    forecast_validation = read_latest(DATA_DIR / "forecast_validation_history.csv")
    methodology = read_records(DATA_DIR / "signal_methodology_registry.csv", limit=10)
    roadmap = read_records(DATA_DIR / "bloomberg_execution_roadmap.csv", limit=50)
    provider_gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv", limit=3)
    snapshot_targets = read_records(DATA_DIR / "snapshot_collection_plan.csv", limit=5)

    scarcity_score = value(scarcity, "gpu_scarcity_index")
    scarcity_band = value(scarcity, "scarcity_band")
    forecast_score = value(forecast, "forecast_score")
    shock_band = value(forecast, "capacity_shock_band")
    dislocation_score = value(price_dislocation, "price_dislocation_score")
    dislocation_band = value(price_dislocation, "dislocation_band")
    stress_score = value(stress, "ai_infrastructure_stress_index")
    stress_band_value = value(stress, "stress_band")
    readiness_phase = value(readiness, "readiness_phase")
    cadence_status = value(cadence, "status")
    days_collected = value(cadence, "days_collected", 0)
    days_to_next = value(cadence, "days_to_next_milestone", "n/a")
    paid_status = value(paid_gate, "gate_status")
    scheduler_status = value(scheduler, "status", "unknown")
    methodology_count = len(methodology)
    roadmap_done = len([row for row in roadmap if row.get("status") == "done"])
    roadmap_total = len(roadmap)
    allowed_claims = len([row for row in claim_gates if row.get("allowed") is True or str(row.get("allowed")).lower() == "true"])
    action_confidence_score = 80
    action_confidence_reason = "Daily scheduler is healthy and trust gates identify source-labeled snapshots as the active blocker."

    headline = (
        f"AI infrastructure stress is {scarcity_band}; "
        f"capacity shock signal is {shock_band}; "
        f"history moat is building ({days_collected} days)."
    )

    if paid_status == "ready":
        operating_mode = "paid_beta_candidate"
        today_action = "Prepare controlled paid-beta customer validation."
        action_confidence_score = 70
        action_confidence_reason = "Paid gate is ready; customer validation is the next commercial risk reducer."
    elif snapshot_quality.get("status") in {"no_snapshots", "snapshots_need_cleanup"}:
        operating_mode = "research_preview_data_collection"
        today_action = snapshot_quality.get(
            "next_action",
            "Collect source-labeled manual snapshots for priority GPUs, providers and regions.",
        )
    elif scheduler_status != "healthy":
        operating_mode = "scheduler_attention_needed"
        today_action = "Fix scheduler health before relying on unattended daily collection."
        action_confidence_score = 95
        action_confidence_reason = "Scheduler health directly controls whether the data moat grows daily."
    else:
        operating_mode = "research_preview"
        today_action = cadence.get("next_action", readiness.get("next_action", "Maintain daily collection."))
        action_confidence_score = 65
        action_confidence_reason = "Daily collection remains useful, but current blocker priority is less specific."

    provider_gap_lines = [
        f"- {gap.get('provider', 'unknown')}: {gap.get('gap', 'unknown')} -> {gap.get('recommended_action', 'n/a')}"
        for gap in provider_gaps
    ] or ["- No provider reliability gaps available."]
    alert_lines = [
        f"- {alert.get('severity', 'unknown')}: {alert.get('title', 'unknown')} -> {alert.get('recommended_action', 'n/a')}"
        for alert in alerts
    ] or ["- No core intelligence alerts available."]
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
        f"- AI Infrastructure Stress Index: {stress_score} ({stress_band_value})",
        f"- GPU Scarcity Index: {scarcity_score} ({scarcity_band})",
        f"- Capacity Forecast Score: {forecast_score} ({shock_band})",
        f"- Price Dislocation Score: {dislocation_score} ({dislocation_band})",
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
        f"- Source URL Coverage: {value(source_coverage, 'source_url_coverage_pct', 0)}%",
        f"- Source-Backed Scarcity: {value(source_backed_scarcity, 'status')}",
        f"- Forecast Accuracy: {value(forecast_accuracy, 'directional_accuracy_pct', 0)}%",
        f"- Forecast Validation: {value(forecast_validation, 'validation_band')}",
        f"- Signal Performance: {value(signal_performance, 'signal_performance_score', 0)} ({value(signal_performance, 'performance_band')})",
        f"- Allowed Claim Gates: {allowed_claims}/{len(claim_gates)}",
        f"- Region Heatmap Rows: {len(region_heatmap)}",
        f"- Documented Core Methodologies: {methodology_count}",
        f"- Bloomberg Roadmap: {roadmap_done}/{roadmap_total} steps done",
        "",
        "## Top Provider Risks",
        *provider_gap_lines,
        "",
        "## Core Alerts",
        *alert_lines,
        "",
        "## Next Snapshot Targets",
        *target_lines,
        "",
        "## Today's Operating Mode",
        operating_mode,
        "",
        "## Today's Action",
        today_action,
        "",
        "## Action Confidence",
        f"{action_confidence_score}/100 - {action_confidence_reason}",
    ])

    return {
        "product": "AI-RPCT",
        "report_type": "morning_brief",
        "generated_at": generated_at,
        "headline": headline,
        "operating_mode": operating_mode,
        "today_action": today_action,
        "action_confidence_score": action_confidence_score,
        "action_confidence_reason": action_confidence_reason,
        "scarcity_band": scarcity_band,
        "capacity_shock_band": shock_band,
        "price_dislocation_score": dislocation_score,
        "price_dislocation_band": dislocation_band,
        "ai_infrastructure_stress_index": stress_score,
        "stress_band": stress_band_value,
        "source_url_coverage_pct": value(source_coverage, "source_url_coverage_pct", 0),
        "source_backed_scarcity_status": value(source_backed_scarcity, "status"),
        "core_alert_count": len(alerts),
        "forecast_directional_accuracy_pct": value(forecast_accuracy, "directional_accuracy_pct", 0),
        "forecast_validation_band": value(forecast_validation, "validation_band"),
        "signal_performance_score": value(signal_performance, "signal_performance_score", 0),
        "signal_performance_band": value(signal_performance, "performance_band"),
        "allowed_claim_gate_count": allowed_claims,
        "claim_gate_count": len(claim_gates),
        "region_heatmap_count": len(region_heatmap),
        "readiness_phase": readiness_phase,
        "paid_beta_gate_status": paid_status,
        "scheduler_status": scheduler_status,
        "collection_cadence_status": cadence_status,
        "days_collected": days_collected,
        "days_to_next_milestone": days_to_next,
        "documented_methodology_count": methodology_count,
        "bloomberg_roadmap_done_steps": roadmap_done,
        "bloomberg_roadmap_total_steps": roadmap_total,
        "markdown": markdown,
    }


def main():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    brief = build_morning_brief()
    path = REPORTS_DIR / f"morning_brief_{datetime.now().strftime('%Y%m%d')}.md"
    path.write_text(brief["markdown"])
    summary = pd.DataFrame([{key: value for key, value in brief.items() if key != "markdown"}])
    summary.to_csv(SUMMARY_FILE, index=False)
    print(summary)


if __name__ == "__main__":
    main()
