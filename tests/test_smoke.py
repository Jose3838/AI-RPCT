from datetime import date, datetime
from pathlib import Path

import pytest
import pandas as pd
from fastapi import HTTPException

from main import app
from api.terminal_core import (
    build_dashboard_snapshot,
    build_data_trust_status,
    build_daily_change_brief,
    build_executive_brief,
    build_market_pulse_brief,
    build_market_pulse,
    build_market_pulse_history,
    build_market_signals,
    build_provider_connector_readiness,
    build_provider_connector_upgrade_plan,
    build_provider_risk_radar,
    build_recommendations,
    build_trust_remediation_plan,
    save_market_pulse_snapshot,
    build_terminal_summary,
)
from intelligence.reports.customer_report_pdf_export_v1 import (
    build_customer_report_html,
    build_customer_report_payload,
)
from intelligence.reports.commercial_board_export_v1 import (
    build_commercial_board_html,
    build_commercial_board_payload,
)
from api.access import (
    build_access_status,
    build_plan_limits,
    build_usage_summary,
    enforce_plan_limits,
)
from api.audit_core import build_audit_log, log_audit_event
from api.commercial_core import (
    build_account_health_snapshot,
    build_commercial_snapshot,
    build_revenue_forecast,
    build_sales_pipeline,
)
from api.commercial_core import build_customer_admin_snapshot
from api.onboarding_core import (
    create_customer_api_key,
    reactivate_customer_api_key,
    revoke_customer_api_key,
)
from api.ops_core import build_launch_controls, build_v1_operations_status
from analytics.market_pulse_snapshot import main as save_market_pulse_snapshot_cli
from analytics.morning_brief import build_morning_brief
from analytics.signal_methodology_registry import (
    build_signal_methodology_markdown,
    build_signal_methodology_registry,
)
from analytics.bloomberg_execution_roadmap import (
    build_bloomberg_execution_roadmap,
    build_roadmap_markdown,
    build_roadmap_summary,
)
from analytics.price_dislocation_signal import build_price_dislocation_signal
from analytics.forecast_signal import build_forecast_signal
from analytics.gpu_scarcity_index import build_gpu_scarcity_index
from analytics.provider_reliability_ranking import build_provider_reliability_ranking
from analytics.provider_daily_metrics import build_provider_daily_metrics
from analytics.provider_health import apply_ingestion_status, build_provider_health
from analytics.provider_reliability_gaps import build_provider_reliability_gaps
from analytics.live_provider_ingest import run_live_provider_ingest
from analytics.core_signal_history import (
    append_core_signal_history,
    build_core_signal_history_summary,
)
from analytics.collection_cadence_audit import build_collection_cadence_audit
from analytics.core_history_audit import build_core_history_audit
from analytics.core_provenance_audit import build_core_provenance_audit
from analytics.core_signal_quality import build_core_signal_quality
from analytics.core_intelligence_readiness import (
    build_core_intelligence_readiness,
    readiness_phase,
)
from analytics.paid_beta_gate import build_paid_beta_gate
from analytics.coverage_universe_status import build_coverage_universe_status
from analytics.manual_snapshot_ingest import build_manual_snapshot_ingest
from analytics.manual_snapshot_quality import build_manual_snapshot_quality
from analytics.research_preview_brief import build_research_preview_brief
from analytics.snapshot_collection_plan import build_snapshot_collection_plan
from analytics.provider_preflight import (
    build_provider_preflight,
    is_configured_secret,
    summarize_provider_preflight,
)
from scripts.core_status import build_action_plan, build_core_status
from scripts.founder_daily_close import build_founder_daily_close
from scripts.history_backfill_plan import build_history_backfill_plan
from scripts.manual_snapshot_copy_ready import build_manual_snapshot_copy_ready
from scripts.manual_snapshot_inbox_template import build_manual_snapshot_inbox_template
from scripts.manual_snapshot_template_check import build_manual_snapshot_template_check
from scripts.manual_snapshot_workflow import build_manual_snapshot_workflow
from scripts.provider_env_check import build_provider_env_check
from scripts.provider_recovery_plan import build_provider_recovery_plan
from scripts.scheduler_health import build_scheduler_health
from scripts.secret_hygiene_check import build_secret_hygiene_check
from snapshot_scheduler import run_scheduled_snapshot
from security.limits import build_limit_status
from security.entitlements import has_access
from security.plan_resolver import resolve_plan

def test_core_files_exist():
    assert Path("main.py").exists()
    assert Path("api/routes.py").exists()
    assert Path("run_daily.sh").exists()
    assert Path("scripts/run_core_intelligence.sh").exists()
    assert Path("scripts/core_status.py").exists()
    assert Path("scripts/provider_env_check.py").exists()
    assert Path("scripts/secret_hygiene_check.py").exists()
    assert Path("scripts/history_backfill_plan.py").exists()
    assert Path("scripts/founder_daily_close.py").exists()
    assert Path("scripts/manual_snapshot_inbox_template.py").exists()
    assert Path("scripts/manual_snapshot_template_check.py").exists()
    assert Path("scripts/manual_snapshot_copy_ready.py").exists()
    assert Path("scripts/manual_snapshot_workflow.py").exists()
    assert Path("scripts/install_macos_launch_agent.sh").exists()
    assert Path("scripts/macos_launch_agent_status.sh").exists()
    assert Path("scripts/uninstall_macos_launch_agent.sh").exists()
    assert Path("scripts/scheduler_health.py").exists()
    assert "scripts/core_status.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "scripts/manual_snapshot_copy_ready.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "analytics/collection_cadence_audit.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "analytics/signal_methodology_registry.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "analytics/bloomberg_execution_roadmap.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "analytics/price_dislocation_signal.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "analytics/morning_brief.py" in Path("scripts/run_core_intelligence.sh").read_text()
    assert "scripts/manual_snapshot_copy_ready.py" in Path("run_daily.sh").read_text()
    assert "analytics/collection_cadence_audit.py" in Path("run_daily.sh").read_text()
    assert "analytics/signal_methodology_registry.py" in Path("run_daily.sh").read_text()
    assert "analytics/bloomberg_execution_roadmap.py" in Path("run_daily.sh").read_text()
    assert "analytics/price_dislocation_signal.py" in Path("run_daily.sh").read_text()
    assert "analytics/morning_brief.py" in Path("run_daily.sh").read_text()
    launch_agent_script = Path("scripts/install_macos_launch_agent.sh").read_text()
    assert "com.airpct.daily" in launch_agent_script
    assert "./scripts/run_core_intelligence.sh" in launch_agent_script
    assert "launchd.daily.out.log" in launch_agent_script
    assert "<integer>8</integer>" in launch_agent_script
    assert Path("analytics/market_pulse_snapshot.py").exists()
    assert Path("analytics/morning_brief.py").exists()
    assert Path("analytics/signal_methodology_registry.py").exists()
    assert Path("analytics/bloomberg_execution_roadmap.py").exists()
    assert Path("analytics/price_dislocation_signal.py").exists()
    assert Path("analytics/coverage_universe_status.py").exists()
    assert Path("analytics/manual_snapshot_ingest.py").exists()
    assert Path("analytics/manual_snapshot_quality.py").exists()
    assert Path("analytics/research_preview_brief.py").exists()
    assert Path("analytics/snapshot_collection_plan.py").exists()
    assert Path("analytics/core_signal_history.py").exists()
    assert Path("analytics/collection_cadence_audit.py").exists()
    assert Path("analytics/core_signal_quality.py").exists()
    assert Path("README.md").exists()
    assert Path("data/gpu_universe.csv").exists()
    assert Path("data/provider_universe.csv").exists()
    assert Path("data/region_universe.csv").exists()
    assert Path("data/manual_market_snapshot_inbox.csv").exists()


def test_snapshot_scheduler_contract():
    payload = run_scheduled_snapshot(
        lambda: {"status": "ok", "version": "test"},
        lambda: {"status": "saved", "market_pulse_score": 50},
    )

    assert payload["status"] == "ok"
    assert payload["snapshot_result"]["version"] == "test"
    assert payload["market_pulse_snapshot"]["status"] == "saved"
    assert payload["executed_at"].endswith("+00:00")


def test_v1_terminal_summary_contract():
    payload = build_terminal_summary()

    assert payload["product"] == "AI-RPCT"
    assert payload["mission"] == "Bloomberg for AI Infrastructure"
    assert "morning_brief" in payload
    assert "terminal" in payload
    assert "risk" in payload
    assert "core_signal_health" in payload
    assert "history_records" in payload["core_signal_health"]
    assert "core_intelligence_readiness" in payload
    assert "core_history_audit" in payload
    assert "collection_cadence" in payload
    assert "core_provenance_audit" in payload
    assert "paid_beta_gate" in payload
    assert "price_dislocation" in payload
    assert "coverage_universe" in payload
    assert "manual_snapshot_quality" in payload
    assert "snapshot_collection_plan" in payload
    assert isinstance(payload["snapshot_collection_plan"], list)
    assert "signal_methodology_registry" in payload
    assert isinstance(payload["signal_methodology_registry"], list)
    assert "bloomberg_execution_roadmap" in payload
    assert "total_steps" in payload["bloomberg_execution_roadmap"]
    assert "manual_snapshot_template_check" in payload
    assert "status" in payload["manual_snapshot_template_check"]
    assert "next_action" in payload["manual_snapshot_template_check"]
    assert "scheduler_health" in payload
    assert "status" in payload["scheduler_health"]
    assert "manual_snapshot_workflow" in payload
    assert "inbox_path" in payload["manual_snapshot_workflow"]
    assert payload["manual_snapshot_workflow"]["fixed_values"]["claim_scope"] == "research_preview"
    assert "provider_recovery_plan" in payload
    assert "paid_beta_gate_status" in payload["core_signal_health"]
    assert "collection_cadence_status" in payload["core_signal_health"]
    assert "provider_reliability" in payload
    assert "quality" in payload


def test_v1_dashboard_snapshot_contract():
    payload = build_dashboard_snapshot()

    assert "market_share" in payload
    assert "provider_health" in payload
    assert "gpu_rankings" in payload
    assert "alerts" in payload
    assert "signals" in payload
    assert "recommendations" in payload
    assert "executive_brief" in payload
    assert payload["recommendations"] == []
    assert "requires Pro access" in payload["executive_brief"]["headline"]


def test_v1_data_trust_status_contract():
    payload = build_data_trust_status()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "data_trust_status"
    assert payload["trust_level"] in {"high", "medium", "low", "critical"}
    assert payload["product_label"] in {
        "decision_support_ready",
        "beta_research_mode",
        "demo_mode",
    }
    assert 0 <= payload["trust_score"] <= 100
    assert isinstance(payload["blockers"], list)
    assert "placeholder_sources" in payload["summary"]


def test_v1_trust_remediation_plan_contract():
    payload = build_trust_remediation_plan()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "trust_remediation_plan"
    assert payload["readiness_path"] in {
        "blocked_by_critical_trust_issues",
        "near_decision_support_ready",
        "maintain_and_validate",
    }
    assert isinstance(payload["actions"], list)
    assert payload["action_count"] == len(payload["actions"])
    assert "current_trust" in payload
    assert "next_action" in payload


def test_v1_provider_connector_readiness_contract():
    payload = build_provider_connector_readiness()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "provider_connector_readiness"
    assert "provider_count" in payload
    assert "readiness_counts" in payload
    assert "provider_recovery_plan" in payload
    assert "missing_credentials" in payload["provider_recovery_plan"]
    assert isinstance(payload["providers"], list)
    if payload["providers"]:
        provider = payload["providers"][0]
        assert "preflight_readiness" in provider
        assert "ingestion_status" in provider
        assert "used_fallback" in provider
        assert "recovery_status" in provider
        assert "verification_command" in provider
    assert isinstance(payload["providers"], list)
    if payload["providers"]:
        provider = payload["providers"][0]
        assert "provider" in provider
        assert "readiness" in provider
        assert "next_action" in provider
        assert "credential_configured" in provider


def test_v1_provider_connector_upgrade_plan_contract():
    payload = build_provider_connector_upgrade_plan()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "provider_connector_upgrade_plan"
    assert payload["rollout_phase"] in {
        "clear_trust_blockers",
        "expand_data_moat",
        "maintain_verified_connectors",
    }
    assert "current_trust" in payload
    assert "next_upgrade" in payload
    assert isinstance(payload["providers"], list)
    if payload["providers"]:
        provider = payload["providers"][0]
        assert "priority_score" in provider
        assert "upgrade_steps" in provider
        assert "buyer_value" in provider


def test_v1_market_pulse_contract():
    payload = build_market_pulse()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "market_pulse"
    assert payload["headline"]
    assert payload["market_pulse_band"] in {"stable", "watch", "elevated", "critical"}
    assert payload["confidence_band"] in {"thin", "low", "medium", "high"}
    assert 0 <= payload["market_pulse_score"] <= 100
    assert 0 <= payload["confidence_score"] <= 100
    assert "terminal_risk_score" in payload["drivers"]
    assert "buyers" in payload["audience_readouts"]
    assert isinstance(payload["next_best_actions"], list)


def test_v1_market_pulse_history_contract(tmp_path, monkeypatch):
    history_file = tmp_path / "market_pulse_history.csv"
    monkeypatch.setattr("api.terminal_core.MARKET_PULSE_HISTORY_FILE", history_file)

    first = build_market_pulse()
    second = build_market_pulse()
    first["market_pulse_score"] = 40
    first["market_pulse_band"] = "watch"
    second["market_pulse_score"] = 55
    second["market_pulse_band"] = "watch"

    save_market_pulse_snapshot(first, history_file)
    save_market_pulse_snapshot(second, history_file)
    payload = build_market_pulse_history()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "market_pulse_history"
    assert payload["record_count"] == 2
    assert payload["trend"]["delta"] == 15
    assert payload["trend"]["direction"] == "up"
    assert len(payload["history"]) == 2


def test_v1_market_pulse_brief_contract():
    payload = build_market_pulse_brief()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "market_pulse_brief"
    assert payload["headline"]
    assert payload["summary"]
    assert "market_pulse" in payload
    assert "history_summary" in payload
    assert isinstance(payload["driver_readout"], list)
    assert "# AI-RPCT Market Pulse Brief" in payload["markdown"]


def test_v1_provider_risk_radar_contract():
    payload = build_provider_risk_radar()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "provider_risk_radar"
    assert "provider_count" in payload
    assert isinstance(payload["providers"], list)
    if payload["providers"]:
        provider = payload["providers"][0]
        assert "provider" in provider
        assert provider["risk_band"] in {"low", "medium", "high"}
        assert 0 <= provider["risk_score"] <= 100
        assert "recommended_action" in provider
        assert "drivers" in provider


def test_v1_daily_change_brief_contract():
    payload = build_daily_change_brief()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "daily_change_brief"
    assert payload["headline"]
    assert payload["summary"]
    assert payload["recommended_decision"]
    assert isinstance(payload["changes"], list)
    assert "market_pulse" in payload
    assert "provider_risk" in payload
    assert "data_trust" in payload
    assert "# AI-RPCT Daily Change Brief" in payload["markdown"]


def test_market_pulse_snapshot_cli_writes_history(tmp_path, monkeypatch):
    history_file = tmp_path / "market_pulse_history.csv"
    monkeypatch.setenv("AIRPCT_MARKET_PULSE_HISTORY_FILE", str(history_file))

    payload = save_market_pulse_snapshot_cli()

    assert payload["status"] == "saved"
    assert payload["file"] == str(history_file)
    assert history_file.exists()
    assert "market_pulse_score" in history_file.read_text()


def test_v1_market_signals_contract():
    payload = build_market_signals()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert isinstance(payload["signals"], list)
    assert payload["signal_count"] == len(payload["signals"])
    signal_types = {signal["type"] for signal in payload["signals"]}
    assert "gpu_scarcity_index" in signal_types
    assert "capacity_shock_forecast" in signal_types
    assert "provider_reliability_gaps" in signal_types


def test_gpu_scarcity_index_exposes_driver_components():
    gpu = pd.DataFrame([
        {"timestamp": "2026-06-22 09:00:00", "provider": "vast", "gpu": "H100", "price_per_hour": 2.5, "availability": 800},
        {"timestamp": "2026-06-22 09:00:00", "provider": "runpod", "gpu": "A100", "price_per_hour": 1.4, "availability": 1200},
        {"timestamp": "2026-06-21 09:00:00", "provider": "vast", "gpu": "H100", "price_per_hour": 1.0, "availability": 3000},
    ])

    row = build_gpu_scarcity_index(gpu).iloc[0]

    assert 0 <= row["gpu_scarcity_index"] <= 100
    assert row["scarcity_band"] in {"stable", "watch", "elevated", "high"}
    assert row["provider_count"] == 2
    assert "frontier_pressure_score" in row


def test_forecast_signal_exposes_capacity_shock_fields():
    rpct = pd.DataFrame([
        {"score": 30},
        {"score": 35},
        {"score": 40},
        {"score": 80},
    ])
    shortage = pd.DataFrame([{"shortage_probability": 60}])
    scarcity = pd.DataFrame([{"gpu_scarcity_index": 70}])

    row = build_forecast_signal(rpct, shortage, scarcity).iloc[0]

    assert 0 <= row["forecast_score"] <= 100
    assert row["capacity_shock_band"] in {"shock_up", "rising", "stable", "easing", "shock_down"}
    assert row["capacity_shock_delta"] > 0
    assert row["confidence_score"] > 0


def test_provider_reliability_ranking_exposes_score_components():
    health = pd.DataFrame([
        {"provider": "vast", "status": "online", "rows": 100, "freshness_hours": 1, "health_score": 90},
        {"provider": "runpod", "status": "online", "rows": 10, "freshness_hours": 20, "health_score": 45},
    ])
    metrics = pd.DataFrame([
        {"provider": "vast", "availability": 2400, "price_per_hour": 1.2, "date": "2026-06-21"},
        {"provider": "vast", "availability": 2300, "price_per_hour": 1.25, "date": "2026-06-22"},
        {"provider": "runpod", "availability": 500, "price_per_hour": 3.0, "date": "2026-06-22"},
    ])

    ranking = build_provider_reliability_ranking(health, metrics)

    assert ranking.iloc[0]["provider"] == "vast"
    assert "reliability_score" in ranking.columns
    assert "freshness_score" in ranking.columns
    assert ranking.iloc[0]["reliability_band"] in {"strong", "watch", "weak", "critical"}
    assert "history_days" in ranking.columns
    assert "provider_rank_score" in ranking.columns


def test_provider_daily_metrics_normalizes_and_deduplicates():
    rankings = pd.DataFrame([
        {"provider": "vast_real", "price_per_hour": 1.0, "availability": 2500, "score": 70},
        {"provider": "vast", "price_per_hour": 1.2, "availability": 2400, "score": 80},
        {"provider": "runpod_real", "price_per_hour": 2.0, "availability": 1000, "score": 40},
    ])

    daily = build_provider_daily_metrics(rankings, run_date="2026-06-22")

    assert set(daily["provider"]) == {"vast", "runpod"}
    assert len(daily) == 2
    assert daily[daily["provider"] == "vast"].iloc[0]["score"] == 80


def test_provider_health_exposes_freshness_and_errors(tmp_path):
    provider_file = tmp_path / "vast.csv"
    provider_file.write_text(
        "provider,gpu,price_per_hour,availability,timestamp\n"
        "vast_real,H100,2.0,1,2026-06-22 09:00:00\n"
    )

    health = build_provider_health(
        [("vast_real", provider_file), ("runpod", tmp_path / "missing.csv")],
        now=datetime(2026, 6, 22, 10, 0, 0),
    )

    vast = health[health["provider"] == "vast"].iloc[0]
    runpod = health[health["provider"] == "runpod"].iloc[0]

    assert vast["status"] == "online"
    assert vast["freshness_band"] == "fresh"
    assert vast["health_score"] > runpod["health_score"]
    assert runpod["status"] == "offline"


def test_provider_health_applies_ingestion_status(tmp_path):
    health = pd.DataFrame([{
        "provider": "vast",
        "status": "online",
        "rows": 1,
        "freshness_hours": 1,
        "health_score": 90,
    }])
    status_file = tmp_path / "status.csv"
    status_file.write_text(
        "provider,status,fresh_rows,used_fallback,output_file,error\n"
        "vast,fallback,0,True,data/vast_live_report.csv,\n"
    )

    enriched = apply_ingestion_status(health, status_file)

    assert enriched.iloc[0]["ingestion_status"] == "fallback"
    assert bool(enriched.iloc[0]["used_fallback"])


def test_provider_reliability_gaps_prioritize_stale_history():
    ranking = pd.DataFrame([
        {
            "provider": "vast",
            "reliability_score": 45,
            "freshness_score": 20,
            "depth_score": 100,
            "history_days": 3,
            "availability_score": 90,
            "ingestion_status": "fallback",
            "used_fallback": True,
        }
    ])

    gaps = build_provider_reliability_gaps(ranking)

    assert gaps.iloc[0]["priority"] == "high"
    assert "provider_ingestion_using_fallback" in set(gaps["gap"])
    assert "stale_provider_data" in set(gaps["gap"])
    assert "insufficient_reliability_history" in set(gaps["gap"])


def test_live_provider_ingest_writes_fresh_and_status(tmp_path, monkeypatch):
    monkeypatch.setattr("analytics.live_provider_ingest.DATA_DIR", tmp_path)

    class FakeProvider:
        name = "vast_real"

        def fetch(self):
            return [{
                "provider": "vast_real",
                "gpu": "H100",
                "price_per_hour": 2.0,
                "availability": 1,
                "timestamp": "2026-06-22 09:00:00",
            }]

    result = run_live_provider_ingest([FakeProvider()])

    assert result["fresh_providers"] == 1
    assert result["rows"] == 1
    assert (tmp_path / "vast_live_report.csv").exists()
    assert (tmp_path / "live_provider_data.csv").exists()
    assert (tmp_path / "live_provider_ingestion_status.csv").exists()


def test_live_provider_ingest_uses_provider_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr("analytics.live_provider_ingest.DATA_DIR", tmp_path)
    (tmp_path / "runpod_live_report.csv").write_text(
        "provider,gpu,price_per_hour,availability,timestamp\n"
        "runpod,A100,1.0,1,2026-06-21 09:00:00\n"
    )

    class EmptyProvider:
        name = "runpod_real"

        def fetch(self):
            return []

    result = run_live_provider_ingest([EmptyProvider()])

    assert result["fresh_providers"] == 0
    assert result["fallback_providers"] == 1
    assert result["rows"] == 1


def test_core_signal_history_summary_tracks_days(tmp_path):
    history_file = tmp_path / "core_signal_history.csv"

    append_core_signal_history(history_file=history_file, generated_at="2026-06-21T09:00:00+00:00")
    append_core_signal_history(history_file=history_file, generated_at="2026-06-22T09:00:00+00:00")
    summary = build_core_signal_history_summary(history_file)

    assert summary["record_count"] == 2
    assert summary["days_collected"] == 2
    assert summary["coverage_band"] == "thin_history"
    assert "gpu_scarcity_index" in summary["deltas"]


def test_core_history_audit_tracks_progress_and_missing_days(tmp_path):
    history_file = tmp_path / "core_signal_history.csv"
    history_file.write_text(
        "timestamp,date,gpu_scarcity_index\n"
        "2026-06-20T09:00:00+00:00,2026-06-20,30\n"
        "2026-06-22T09:00:00+00:00,2026-06-22,40\n"
    )

    audit = build_core_history_audit(history_file, end_date=date(2026, 6, 22)).iloc[0]

    assert audit["days_collected"] == 2
    assert audit["days_remaining"] == 28
    assert audit["history_band"] == "thin_history"
    assert "2026-06-21" in audit["missing_recent_days"]


def test_core_provenance_audit_detects_fallback_rows(tmp_path):
    history_file = tmp_path / "core_signal_history.csv"
    history_file.write_text(
        "timestamp,date,provider_fallback_count,paid_reliability_claims_allowed,history_claim_scope\n"
        "2026-06-22T09:00:00+00:00,2026-06-22,2,False,research_only\n"
    )

    audit = build_core_provenance_audit(history_file).iloc[0]

    assert audit["provenance_band"] == "fallback_contaminated"
    assert audit["fallback_rows"] == 1
    assert not bool(audit["paid_claims_allowed"])


def test_core_signal_quality_contract():
    quality = build_core_signal_quality().iloc[0]

    assert 0 <= quality["core_signal_quality_score"] <= 100
    assert quality["quality_band"] in {"strong", "usable", "needs_work", "weak"}
    assert "paid_beta_signal_ready" in quality
    assert "provider_gap_score" in quality
    assert "high_provider_gap_count" in quality
    assert "history_progress_pct" in quality
    assert "history_days_remaining" in quality
    assert "provenance_score" in quality
    assert "provenance_band" in quality
    assert "blockers" in quality


def test_core_intelligence_readiness_phase_priority():
    assert readiness_phase(
        {"paid_beta_signal_ready": False, "core_signal_quality_score": 50},
        {"restore_live_provider_ingestion"},
    ) == "blocked_by_live_data"
    assert readiness_phase(
        {"paid_beta_signal_ready": False, "core_signal_quality_score": 50},
        {"collect_30_days_of_core_signal_history"},
    ) == "building_history"
    assert readiness_phase(
        {"paid_beta_signal_ready": True, "core_signal_quality_score": 90},
        set(),
    ) == "paid_beta_ready"


def test_core_intelligence_readiness_contract():
    readiness = build_core_intelligence_readiness().iloc[0]

    assert readiness["readiness_phase"] in {
        "paid_beta_ready",
        "blocked_by_live_data",
        "building_history",
        "usable_beta_signal",
        "research_mode",
    }
    assert "next_action" in readiness
    assert "blockers" in readiness
    assert "provider_preflight_blocked_count" in readiness


def test_core_status_contract():
    status = build_core_status()

    assert status["product"] == "AI-RPCT"
    assert "readiness_phase" in status
    assert "provider_credentials" in status
    assert "configured_count" in status["provider_credentials"]
    assert "provider_recovery_plan" in status
    assert "coverage_universe" in status
    assert "manual_snapshot_quality" in status
    assert "snapshot_collection_plan" in status
    assert "next_action" in status
    assert "action_plan" in status
    assert isinstance(status["action_plan"], list)
    assert isinstance(status["top_provider_gaps"], list)


def test_core_status_action_plan_prioritizes_preflight():
    actions = build_action_plan(
        {"blockers": "collect_30_days_of_core_signal_history"},
        [{"provider": "vast", "priority": "high", "gap": "stale_provider_data", "recommended_action": "Refresh Vast."}],
        [{"provider": "vast", "readiness": "blocked", "next_action": "Configure VAST_API_KEY."}],
    )

    assert actions[0]["priority"] == "critical"
    assert actions[0]["source"] == "provider_preflight"


def test_history_backfill_plan_contract():
    plan = build_history_backfill_plan()

    assert plan["product"] == "AI-RPCT"
    assert plan["policy"] == "do_not_fake_history"
    assert "recommended_action" in plan
    assert isinstance(plan["missing_recent_days"], list)


def test_coverage_universe_status_contract():
    status = build_coverage_universe_status().iloc[0]

    assert status["gpu_universe_count"] >= 20
    assert status["provider_universe_count"] >= 15
    assert status["region_universe_count"] >= 8
    assert status["claim_scope"] == "research_preview"
    assert status["history_policy"] == "do_not_backfill_without_sources"
    assert "valid_manual_snapshot_count" in status
    assert "next_action" in status


def test_manual_snapshot_quality_empty_template_contract():
    quality = build_manual_snapshot_quality().iloc[0]

    assert quality["status"] in {"no_snapshots", "snapshots_valid_for_research_preview", "snapshots_need_cleanup"}
    assert quality["claim_scope"] == "research_preview"
    assert quality["history_policy"] == "do_not_backfill_without_sources"
    assert "next_action" in quality


def test_manual_snapshot_workflow_contract():
    workflow = build_manual_snapshot_workflow()

    assert workflow["product"] == "AI-RPCT"
    assert workflow["report_type"] == "manual_snapshot_workflow"
    assert workflow["fixed_values"]["source_type"] == "manual_public_snapshot"
    assert workflow["fixed_values"]["claim_scope"] == "research_preview"
    assert "snapshot_date" in workflow["required_columns"]
    assert workflow["example_row"]["source_type"] == "manual_public_snapshot"
    assert workflow["example_row"]["claim_scope"] == "research_preview"
    assert workflow["priority_collection"]["gpus"]
    assert workflow["priority_collection"]["providers"]
    assert workflow["priority_collection"]["regions"]
    assert workflow["next_snapshot_targets"]
    assert workflow["next_snapshot_targets"][0]["claim_scope"] == "research_preview"


def test_snapshot_collection_plan_contract():
    plan = build_snapshot_collection_plan()

    assert not plan.empty
    assert {"provider", "gpu", "region_code", "priority_score"}.issubset(plan.columns)
    assert plan.iloc[0]["source_type"] == "manual_public_snapshot"
    assert plan.iloc[0]["claim_scope"] == "research_preview"


def test_manual_snapshot_inbox_template_contract():
    template = build_manual_snapshot_inbox_template(limit=3)

    assert len(template) == 3
    assert template.iloc[0]["source_type"] == "manual_public_snapshot"
    assert template.iloc[0]["claim_scope"] == "research_preview"
    assert "source_url" in template.columns
    assert "Fill price" in template.iloc[0]["notes"]


def test_manual_snapshot_template_check_rejects_unfilled_template(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    build_manual_snapshot_inbox_template(tmp_path, limit=1).to_csv(
        tmp_path / "manual_market_snapshot_inbox_template.csv",
        index=False,
    )

    check = build_manual_snapshot_template_check(tmp_path)

    assert check["status"] == "template_needs_sources"
    assert check["valid_row_count"] == 0
    assert check["rejected_row_count"] == 1


def test_manual_snapshot_template_check_accepts_completed_template(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame([{
        "snapshot_date": "2026-06-23",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "us-east",
        "price_per_hour": 1.5,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "https://example.com/h100",
        "source_type": "manual_public_snapshot",
        "claim_scope": "research_preview",
        "notes": "test",
    }]).to_csv(tmp_path / "manual_market_snapshot_inbox_template.csv", index=False)

    check = build_manual_snapshot_template_check(tmp_path)

    assert check["status"] == "ready_to_copy"
    assert check["valid_row_count"] == 1
    assert check["rejected_row_count"] == 0


def test_manual_snapshot_copy_ready_copies_only_valid_template_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame(columns=[
        "snapshot_date",
        "provider",
        "gpu",
        "region_code",
        "price_per_hour",
        "availability",
        "delivery_time_days",
        "source_url",
        "source_type",
        "claim_scope",
        "notes",
    ]).to_csv(tmp_path / "manual_market_snapshot_inbox.csv", index=False)
    pd.DataFrame([
        {
            "snapshot_date": "2026-06-23",
            "provider": "vast",
            "gpu": "H100",
            "region_code": "us-east",
            "price_per_hour": 1.5,
            "availability": 10,
            "delivery_time_days": 0,
            "source_url": "https://example.com/h100",
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "notes": "valid",
        },
        {
            "snapshot_date": "2026-06-23",
            "provider": "vast",
            "gpu": "H100",
            "region_code": "unknown",
            "price_per_hour": "",
            "availability": 10,
            "delivery_time_days": 0,
            "source_url": "",
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "notes": "invalid",
        },
    ]).to_csv(tmp_path / "manual_market_snapshot_inbox_template.csv", index=False)

    result = build_manual_snapshot_copy_ready(tmp_path)
    inbox = pd.read_csv(tmp_path / "manual_market_snapshot_inbox.csv")
    rejections = pd.read_csv(tmp_path / "manual_market_snapshot_template_rejections.csv")

    assert result["status"] == "partially_copied"
    assert result["copied_count"] == 1
    assert result["rejected_template_row_count"] == 1
    assert len(inbox) == 1
    assert len(rejections) == 1


def test_manual_snapshot_copy_ready_deduplicates_existing_inbox_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    row = {
        "snapshot_date": "2026-06-23",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "us-east",
        "price_per_hour": 1.5,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "https://example.com/h100",
        "source_type": "manual_public_snapshot",
        "claim_scope": "research_preview",
        "notes": "valid",
    }
    pd.DataFrame([row]).to_csv(tmp_path / "manual_market_snapshot_inbox.csv", index=False)
    pd.DataFrame([row]).to_csv(tmp_path / "manual_market_snapshot_inbox_template.csv", index=False)

    result = build_manual_snapshot_copy_ready(tmp_path)
    inbox = pd.read_csv(tmp_path / "manual_market_snapshot_inbox.csv")

    assert result["status"] == "no_new_rows"
    assert result["copied_count"] == 0
    assert result["duplicate_count"] == 1
    assert len(inbox) == 1


def test_manual_snapshot_quality_rejects_untrusted_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame([{
        "snapshot_date": "2099-01-01",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "us-east",
        "price_per_hour": 1.5,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "not-a-url",
        "source_type": "manual",
        "claim_scope": "paid_claim",
        "notes": "",
    }]).to_csv(tmp_path / "manual_market_snapshots.csv", index=False)

    quality = build_manual_snapshot_quality(tmp_path).iloc[0]

    assert quality["status"] == "snapshots_need_cleanup"
    assert quality["valid_snapshot_count"] == 0
    assert "source_url_not_http" in quality["blockers"]
    assert "claim_scope_must_be_research_preview" in quality["blockers"]


def test_manual_snapshot_quality_accepts_source_labeled_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame([{
        "snapshot_date": "2026-06-23",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "us-east",
        "price_per_hour": 1.5,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "https://example.com/h100",
        "source_type": "manual_public_snapshot",
        "claim_scope": "research_preview",
        "notes": "",
    }]).to_csv(tmp_path / "manual_market_snapshots.csv", index=False)

    quality = build_manual_snapshot_quality(tmp_path).iloc[0]

    assert quality["status"] == "snapshots_valid_for_research_preview"
    assert quality["valid_snapshot_count"] == 1
    assert quality["blockers"] == "none"


def test_manual_snapshot_ingest_imports_valid_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame(columns=[
        "snapshot_date",
        "provider",
        "gpu",
        "region_code",
        "price_per_hour",
        "availability",
        "delivery_time_days",
        "source_url",
        "source_type",
        "claim_scope",
        "notes",
    ]).to_csv(tmp_path / "manual_market_snapshots.csv", index=False)
    pd.DataFrame([{
        "snapshot_date": "2026-06-23",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "us-east",
        "price_per_hour": 1.5,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "https://example.com/h100",
        "source_type": "manual_public_snapshot",
        "claim_scope": "research_preview",
        "notes": "test",
    }]).to_csv(tmp_path / "manual_market_snapshot_inbox.csv", index=False)

    result = build_manual_snapshot_ingest(tmp_path)
    master = pd.read_csv(tmp_path / "manual_market_snapshots.csv")

    assert result["status"] == "imported"
    assert result["imported_count"] == 1
    assert result["rejected_count"] == 0
    assert len(master) == 1


def test_manual_snapshot_ingest_rejects_invalid_rows(tmp_path):
    pd.DataFrame([{"gpu": "H100"}]).to_csv(tmp_path / "gpu_universe.csv", index=False)
    pd.DataFrame([{"provider": "vast"}]).to_csv(tmp_path / "provider_universe.csv", index=False)
    pd.DataFrame([{"region_code": "us-east"}]).to_csv(tmp_path / "region_universe.csv", index=False)
    pd.DataFrame(columns=[
        "snapshot_date",
        "provider",
        "gpu",
        "region_code",
        "price_per_hour",
        "availability",
        "delivery_time_days",
        "source_url",
        "source_type",
        "claim_scope",
        "notes",
    ]).to_csv(tmp_path / "manual_market_snapshots.csv", index=False)
    pd.DataFrame([{
        "snapshot_date": "2026-06-23",
        "provider": "vast",
        "gpu": "H100",
        "region_code": "unknown-region",
        "price_per_hour": -1,
        "availability": 10,
        "delivery_time_days": 0,
        "source_url": "not-a-url",
        "source_type": "manual",
        "claim_scope": "research_preview",
        "notes": "test",
    }]).to_csv(tmp_path / "manual_market_snapshot_inbox.csv", index=False)

    result = build_manual_snapshot_ingest(tmp_path)
    master = pd.read_csv(tmp_path / "manual_market_snapshots.csv")
    rejected = pd.read_csv(tmp_path / "manual_market_snapshot_rejections.csv")

    assert result["status"] == "nothing_imported"
    assert result["imported_count"] == 0
    assert result["rejected_count"] == 1
    assert len(master) == 0
    assert "unknown_region" in rejected.iloc[0]["rejection_reason"]


def test_research_preview_brief_contract():
    brief = build_research_preview_brief()

    assert brief["product"] == "AI-RPCT"
    assert brief["report_type"] == "research_preview_brief"
    assert brief["preview_status"] in {
        "research_preview",
        "snapshot_collection_needed",
        "paid_beta_ready",
    }
    assert "safe_claims" in brief
    assert "unsafe_claims" in brief
    assert "No 6-12 month history claim without sourced historical records." in brief["unsafe_claims"]
    assert "Research Preview Brief" in brief["markdown"]
    assert "Claims Not Yet Safe" in brief["markdown"]


def test_morning_brief_contract():
    brief = build_morning_brief()

    assert brief["product"] == "AI-RPCT"
    assert brief["report_type"] == "morning_brief"
    assert "headline" in brief
    assert "operating_mode" in brief
    assert "today_action" in brief
    assert "documented_methodology_count" in brief
    assert "bloomberg_roadmap_total_steps" in brief
    assert "AI-RPCT Morning Brief" in brief["markdown"]
    assert "Today's Action" in brief["markdown"]


def test_signal_methodology_registry_contract():
    registry = build_signal_methodology_registry()
    markdown = build_signal_methodology_markdown(registry)

    assert len(registry) >= 3
    assert set(registry["signal_id"]) >= {
        "gpu_scarcity_index",
        "capacity_shock_forecast",
        "provider_reliability_score",
        "price_dislocation_signal",
    }
    assert "formula_summary" in registry.columns
    assert "paid_safe_requirement" in registry.columns
    assert "AI-RPCT Signal Methodology Registry" in markdown


def test_bloomberg_execution_roadmap_contract():
    roadmap = build_bloomberg_execution_roadmap()
    summary = build_roadmap_summary(roadmap)
    markdown = build_roadmap_markdown(roadmap)

    assert len(roadmap) == 50
    assert summary["total_steps"] == 50
    assert summary["done_steps"] > 0
    assert roadmap[roadmap["step"] == 24].iloc[0]["status"] == "done"
    assert set(roadmap["category"]) == {
        "data_moat",
        "trust",
        "core_intelligence",
        "terminal_product",
        "commercial",
    }
    assert "AI-RPCT Bloomberg Execution Roadmap" in markdown


def test_price_dislocation_signal_detects_wide_spread():
    gpu_data = pd.DataFrame([
        {"timestamp": "2026-06-23 08:00:00", "provider": "cheap_cloud", "gpu": "H100", "price_per_hour": 2.0, "availability": 5},
        {"timestamp": "2026-06-23 08:00:00", "provider": "premium_cloud", "gpu": "H100", "price_per_hour": 6.0, "availability": 5},
        {"timestamp": "2026-06-23 08:00:00", "provider": "mid_cloud", "gpu": "H100", "price_per_hour": 4.0, "availability": 5},
    ])

    signal = build_price_dislocation_signal(gpu_data).iloc[0]

    assert signal["status"] == "price_dislocation_signal_ready"
    assert signal["price_dislocation_score"] == 100
    assert signal["dislocation_band"] == "extreme"
    assert signal["top_gpu"] == "H100"


def test_morning_brief_cli_writes_summary():
    from analytics import morning_brief

    morning_brief.main()

    summary = pd.read_csv("data/morning_brief_summary.csv").iloc[-1].to_dict()
    assert summary["report_type"] == "morning_brief"
    assert "headline" in summary
    assert "today_action" in summary


def test_founder_daily_close_contract():
    close = build_founder_daily_close()

    assert close["product"] == "AI-RPCT"
    assert close["report_type"] == "founder_daily_close"
    assert close["status"] == "saved_for_next_session"
    assert "morning_headline" in close
    assert "morning_operating_mode" in close
    assert "morning_today_action" in close
    assert "collection_cadence_status" in close
    assert "collection_days_collected" in close
    assert "tomorrow_focus" in close
    assert "top_actions" in close
    assert isinstance(close["top_actions"], list)
    assert "manual_snapshot_template_status" in close
    assert "snapshot_collection_targets" in close
    assert isinstance(close["snapshot_collection_targets"], list)
    assert "scheduler_status" in close
    assert "scheduler_next_action" in close
    assert "do_not_claim_yet" in close


def test_scheduler_health_contract():
    health = build_scheduler_health()

    assert health["product"] == "AI-RPCT"
    assert health["report_type"] == "scheduler_health"
    assert "status" in health
    assert "plist_installed" in health
    assert "last_run_completed" in health
    assert "next_action" in health


def test_collection_cadence_audit_detects_missing_days(tmp_path):
    pd.DataFrame([
        {"date": "2026-06-20"},
        {"date": "2026-06-22"},
        {"date": "2026-06-23"},
    ]).to_csv(tmp_path / "core_signal_history.csv", index=False)

    audit = build_collection_cadence_audit(tmp_path, today=date(2026, 6, 23)).iloc[0]

    assert audit["status"] == "history_has_gaps"
    assert audit["days_collected"] == 3
    assert audit["current_streak_days"] == 2
    assert audit["missing_day_count"] == 1
    assert audit["missing_dates"] == "2026-06-21"


def test_provider_preflight_blocks_missing_keys_and_fallback():
    preflight = build_provider_preflight(
        env={},
        ingestion_rows=[
            {"provider": "vast", "status": "fallback", "used_fallback": True},
            {"provider": "runpod", "status": "empty", "used_fallback": False},
        ],
    )
    summary = summarize_provider_preflight(preflight)

    assert set(preflight["readiness"]) == {"blocked"}
    assert summary["paid_reliability_claims_allowed"] is False
    assert summary["blocked_count"] == 2
    assert "missing_api_key" in preflight.iloc[0]["blockers"]


def test_provider_secret_validation_rejects_placeholders():
    assert not is_configured_secret("")
    assert not is_configured_secret("DEIN_KEY_HIER")
    assert not is_configured_secret("placeholder")
    assert is_configured_secret("realistic_test_key_123")


def test_provider_preflight_allows_fresh_configured():
    preflight = build_provider_preflight(
        env={"VAST_API_KEY": "realistic_vast_test_key", "RUNPOD_API_KEY": "realistic_runpod_test_key"},
        ingestion_rows=[
            {"provider": "vast", "status": "fresh", "used_fallback": False},
            {"provider": "runpod", "status": "fresh", "used_fallback": False},
        ],
    )
    summary = summarize_provider_preflight(preflight)

    assert set(preflight["readiness"]) == {"ready"}
    assert summary["paid_reliability_claims_allowed"] is True
    assert summary["ready_count"] == 2


def test_provider_env_check_contract():
    payload = build_provider_env_check({
        "VAST_API_KEY": "realistic_test_key_123",
        "RUNPOD_API_KEY": "",
    })

    assert payload["product"] == "AI-RPCT"
    assert payload["configured_count"] == 1
    assert not payload["all_required_configured"]
    assert "providers" in payload
    assert "realistic_test_key_123" not in str(payload)


def test_provider_recovery_plan_blocks_missing_credentials(tmp_path):
    pd.DataFrame([{
        "provider": "vast",
        "readiness": "blocked",
        "ingestion_status": "fallback",
        "used_fallback": True,
        "next_action": "Configure VAST_API_KEY in the runtime environment.",
    }, {
        "provider": "runpod",
        "readiness": "blocked",
        "ingestion_status": "fallback",
        "used_fallback": True,
        "next_action": "Configure RUNPOD_API_KEY in the runtime environment.",
    }]).to_csv(tmp_path / "provider_preflight.csv", index=False)
    pd.DataFrame([{
        "provider": "vast",
        "status": "fallback",
        "used_fallback": True,
    }]).to_csv(tmp_path / "live_provider_ingestion_status.csv", index=False)

    payload = build_provider_recovery_plan(
        env={"VAST_API_KEY": "", "RUNPOD_API_KEY": "real_runpod_secret_123"},
        data_dir=tmp_path,
    )

    assert payload["product"] == "AI-RPCT"
    assert payload["report_type"] == "provider_recovery_plan"
    assert payload["status"] == "blocked_by_missing_credentials"
    assert payload["missing_credentials"] == ["VAST_API_KEY"]
    assert payload["configured_count"] == 1
    assert "real_runpod_secret_123" not in str(payload)


def test_provider_recovery_plan_allows_clean_history_collection(tmp_path):
    pd.DataFrame([{
        "provider": "vast",
        "readiness": "ready",
        "ingestion_status": "fresh",
        "used_fallback": False,
    }, {
        "provider": "runpod",
        "readiness": "ready",
        "ingestion_status": "fresh",
        "used_fallback": False,
    }]).to_csv(tmp_path / "provider_preflight.csv", index=False)
    pd.DataFrame([{
        "provider": "vast",
        "status": "fresh",
        "used_fallback": False,
    }, {
        "provider": "runpod",
        "status": "fresh",
        "used_fallback": False,
    }]).to_csv(tmp_path / "live_provider_ingestion_status.csv", index=False)

    payload = build_provider_recovery_plan(
        env={
            "VAST_API_KEY": "realistic_vast_secret_123",
            "RUNPOD_API_KEY": "realistic_runpod_secret_123",
        },
        data_dir=tmp_path,
    )

    assert payload["status"] == "ready_for_clean_history_collection"
    assert payload["verified_live_count"] == 2
    assert payload["missing_credentials"] == []


def test_secret_hygiene_check_contract():
    payload = build_secret_hygiene_check()

    assert payload["product"] == "AI-RPCT"
    assert payload["env_ignored"]
    assert not payload["env_example_has_secret_values"]
    assert payload["status"] == "ok"


def test_v1_recommendations_contract():
    payload = build_recommendations()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert isinstance(payload["recommendations"], list)
    assert payload["recommendation_count"] == len(payload["recommendations"])


def test_v1_executive_brief_contract():
    payload = build_executive_brief()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "executive_brief"
    assert payload["headline"]
    assert payload["summary"]
    assert "markdown" in payload
    assert "signal_readiness" in payload
    assert "core_intelligence_readiness" in payload
    assert "paid_beta_gate" in payload
    assert "capacity_forecast_score" in payload["core_metrics"]
    assert "core_readiness_phase" in payload["core_metrics"]
    assert "history_progress_pct" in payload["core_metrics"]
    assert "provenance_band" in payload["core_metrics"]
    assert "paid_beta_gate_status" in payload["core_metrics"]
    assert "Core Signal Quality" in payload["markdown"]
    assert "History Progress" in payload["markdown"]
    assert "Provenance" in payload["markdown"]
    assert "Paid Beta Gate" in payload["markdown"]
    assert "Provider Reliability" in payload["markdown"]


def test_customer_report_export_contract():
    payload = build_customer_report_payload("Test Customer")
    html = build_customer_report_html("Test Customer")

    assert payload["product"] == "AI-RPCT"
    assert payload["report_type"] == "customer_report_pdf_ready"
    assert payload["customer_name"] == "Test Customer"
    assert "markdown" in payload
    assert "<html" in html
    assert "Test Customer" in html


def test_v1_plan_access_contract():
    assert resolve_plan("demo-free-key") == "free"
    assert resolve_plan("demo-pro-key") == "pro"
    assert resolve_plan("demo-enterprise-key") == "enterprise"

    assert has_access("free", "/v1/access-status")
    assert has_access("free", "/v1/plan-limits")
    assert has_access("free", "/v1/data-trust-status")
    assert has_access("free", "/v1/trust-remediation-plan")
    assert has_access("free", "/v1/provider-connector-readiness")
    assert has_access("free", "/v1/provider-connector-upgrade-plan")
    assert has_access("free", "/v1/market-pulse")
    assert not has_access("free", "/v1/market-pulse-history")
    assert has_access("pro", "/v1/market-pulse-history")
    assert has_access("pro", "/v1/market-pulse/snapshot")
    assert not has_access("free", "/v1/market-pulse-brief")
    assert has_access("pro", "/v1/market-pulse-brief")
    assert has_access("pro", "/v1/market-pulse-brief/save")
    assert not has_access("free", "/v1/provider-risk-radar")
    assert has_access("pro", "/v1/provider-risk-radar")
    assert not has_access("free", "/v1/daily-change-brief")
    assert has_access("pro", "/v1/daily-change-brief")
    assert not has_access("free", "/v1/usage-summary")
    assert has_access("pro", "/v1/usage-summary")
    assert not has_access("pro", "/v1/commercial-snapshot")
    assert has_access("enterprise", "/v1/commercial-snapshot")
    assert not has_access("pro", "/v1/sales-pipeline")
    assert has_access("enterprise", "/v1/sales-pipeline")
    assert not has_access("pro", "/v1/customer-admin")
    assert has_access("enterprise", "/v1/customer-admin")
    assert not has_access("pro", "/v1/account-health")
    assert has_access("enterprise", "/v1/account-health")
    assert not has_access("pro", "/v1/revenue-forecast")
    assert has_access("enterprise", "/v1/revenue-forecast")
    assert not has_access("pro", "/v1/commercial-board-report")
    assert has_access("enterprise", "/v1/commercial-board-report")
    assert has_access("enterprise", "/v1/commercial-board-report/html")
    assert not has_access("pro", "/v1/audit-log")
    assert has_access("enterprise", "/v1/audit-log")
    assert not has_access("pro", "/v1/operations-status")
    assert has_access("enterprise", "/v1/operations-status")
    assert not has_access("pro", "/v1/launch-controls")
    assert has_access("enterprise", "/v1/launch-controls")
    assert not has_access("pro", "/v1/customers")
    assert has_access("enterprise", "/v1/customers")
    assert not has_access("pro", "/v1/customers/revoke")
    assert has_access("enterprise", "/v1/customers/revoke")
    assert not has_access("pro", "/v1/customers/reactivate")
    assert has_access("enterprise", "/v1/customers/reactivate")
    assert has_access("free", "/v1/signals")
    assert not has_access("free", "/v1/recommendations")
    assert has_access("pro", "/v1/recommendations")
    assert not has_access("pro", "/v1/customer-report")
    assert has_access("enterprise", "/v1/customer-report")


def test_v1_access_status_contract():
    payload = build_access_status("demo-pro-key")

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["authenticated"]
    assert payload["plan"] == "pro"
    assert "/v1/recommendations" in payload["allowed_endpoints"]
    assert "/v1/customer-report" not in payload["allowed_endpoints"]
    assert "usage" in payload
    assert payload["limits"]["plan"] == "pro"
    assert "daily_remaining" in payload["limits"]


def test_v1_usage_summary_contract():
    payload = build_usage_summary("demo-enterprise-key")

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["plan"] == "enterprise"
    assert "total_calls" in payload
    assert isinstance(payload["by_endpoint"], list)
    assert isinstance(payload["recent"], list)
    assert payload["limits"]["plan"] == "enterprise"


def test_v1_plan_limits_contract():
    payload = build_plan_limits()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["plans"]["free"]["requests_per_day"] == 50
    assert payload["plans"]["pro"]["requests_per_day"] == 10000
    assert payload["plans"]["enterprise"]["requests_per_month"] == 10000000


def test_v1_commercial_snapshot_contract():
    payload = build_commercial_snapshot()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "commercial_snapshot"
    assert payload["summary"]["active_accounts"] >= 3
    assert payload["summary"]["mrr_usd"] >= 2799
    assert payload["summary"]["annual_run_rate_usd"] == payload["summary"]["mrr_usd"] * 12
    assert isinstance(payload["accounts"], list)
    assert payload["accounts"][0]["usage"]["total_calls"] >= 0
    assert "upgrade_signal" in payload["accounts"][0]


def test_v1_sales_pipeline_contract():
    payload = build_sales_pipeline()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "sales_pipeline"
    assert "opportunity_count" in payload["summary"]
    assert "estimated_mrr_lift_usd" in payload["summary"]
    assert isinstance(payload["opportunities"], list)


def test_v1_customer_admin_snapshot_contract():
    payload = build_customer_admin_snapshot()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "customer_admin_snapshot"
    assert payload["summary"]["total_accounts"] >= 3
    assert "active" in payload["summary"]["status_counts"]
    assert isinstance(payload["accounts"], list)
    assert "api_key" in payload["accounts"][0]


def test_v1_account_health_contract():
    payload = build_account_health_snapshot()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "account_health"
    assert payload["summary"]["account_count"] >= 3
    assert isinstance(payload["accounts"], list)
    assert "health_score" in payload["accounts"][0]
    assert "health" in payload["accounts"][0]


def test_v1_revenue_forecast_contract():
    payload = build_revenue_forecast()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "revenue_forecast"
    assert payload["summary"]["current_mrr_usd"] >= 0
    assert payload["summary"]["expected_arr_usd"] == payload["summary"]["expected_mrr_usd"] * 12
    assert "pipeline" in payload["drivers"]
    assert "health" in payload["drivers"]


def test_commercial_board_export_contract():
    payload = build_commercial_board_payload()
    html = build_commercial_board_html()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "commercial_board_export"
    assert "commercial" in payload
    assert "forecast" in payload
    assert "markdown" in payload
    assert "<html" in html
    assert "Commercial Board Report" in html


def test_v1_operations_status_contract():
    payload = build_v1_operations_status()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "operations_status"
    assert payload["status"] in {"ready", "beta_watch"}
    assert isinstance(payload["blocking_issues"], list)
    assert "readiness" in payload
    assert "launch_controls" in payload["readiness"]
    assert "paid_beta_gate" in payload["readiness"]
    assert "effective_controls" in payload
    assert isinstance(payload["files"], list)


def test_v1_launch_controls_contract():
    payload = build_launch_controls()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "launch_controls"
    assert "billing_ready" in payload["controls"]
    assert "terms_ready" in payload["controls"]
    assert "paid_customers_allowed" in payload["controls"]
    assert "paid_beta_gate" in payload
    assert "effective_controls" in payload


def test_paid_beta_gate_blocks_research_grade_core(tmp_path):
    pd.DataFrame([{
        "readiness_phase": "blocked_by_live_data",
        "core_signal_quality_score": 53.3,
        "paid_beta_signal_ready": False,
        "provider_preflight_blocked_count": 2,
    }]).to_csv(tmp_path / "core_intelligence_readiness.csv", index=False)
    pd.DataFrame([{
        "core_signal_quality_score": 53.3,
    }]).to_csv(tmp_path / "core_signal_quality.csv", index=False)
    pd.DataFrame([{
        "progress_pct": 3.33,
        "days_remaining": 29,
        "paid_beta_history_ready": False,
    }]).to_csv(tmp_path / "core_history_audit.csv", index=False)
    pd.DataFrame([{
        "provenance_band": "fallback_contaminated",
        "paid_claims_allowed": False,
    }]).to_csv(tmp_path / "core_provenance_audit.csv", index=False)
    pd.DataFrame([{
        "blocked_count": 2,
        "paid_reliability_claims_allowed": False,
        "next_action": "Configure VAST_API_KEY in the runtime environment.",
    }]).to_csv(tmp_path / "provider_preflight_summary.csv", index=False)
    pd.DataFrame([
        {"control": "billing_ready", "status": "false", "detail": ""},
        {"control": "terms_ready", "status": "false", "detail": ""},
        {"control": "paid_customers_allowed", "status": "false", "detail": ""},
    ]).to_csv(tmp_path / "launch_controls.csv", index=False)

    gate = build_paid_beta_gate(tmp_path).iloc[0].to_dict()

    assert bool(gate["paid_beta_allowed"]) is False
    assert gate["gate_status"] == "blocked"
    assert "provider_preflight_blocked" in gate["blockers"]
    assert gate["next_action"] == "Configure VAST_API_KEY in the runtime environment."


def test_paid_beta_gate_allows_clean_paid_beta(tmp_path):
    pd.DataFrame([{
        "readiness_phase": "paid_beta_ready",
        "core_signal_quality_score": 88,
        "paid_beta_signal_ready": True,
        "provider_preflight_blocked_count": 0,
    }]).to_csv(tmp_path / "core_intelligence_readiness.csv", index=False)
    pd.DataFrame([{
        "core_signal_quality_score": 88,
    }]).to_csv(tmp_path / "core_signal_quality.csv", index=False)
    pd.DataFrame([{
        "progress_pct": 100,
        "days_remaining": 0,
        "paid_beta_history_ready": True,
    }]).to_csv(tmp_path / "core_history_audit.csv", index=False)
    pd.DataFrame([{
        "provenance_band": "paid_claim_safe",
        "paid_claims_allowed": True,
    }]).to_csv(tmp_path / "core_provenance_audit.csv", index=False)
    pd.DataFrame([{
        "blocked_count": 0,
        "paid_reliability_claims_allowed": True,
        "next_action": "Start controlled paid beta with one customer.",
    }]).to_csv(tmp_path / "provider_preflight_summary.csv", index=False)
    pd.DataFrame([
        {"control": "billing_ready", "status": "true", "detail": ""},
        {"control": "terms_ready", "status": "true", "detail": ""},
        {"control": "paid_customers_allowed", "status": "true", "detail": ""},
    ]).to_csv(tmp_path / "launch_controls.csv", index=False)

    gate = build_paid_beta_gate(tmp_path).iloc[0].to_dict()

    assert bool(gate["paid_beta_allowed"]) is True
    assert gate["gate_status"] == "ready"
    assert gate["blockers"] == "none"


def test_v1_audit_log_contract(tmp_path, monkeypatch):
    audit_file = tmp_path / "audit_log.csv"
    monkeypatch.setattr("api.audit_core.AUDIT_FILE", audit_file)

    log_audit_event(
        "demo-enterprise-key",
        "customer_created",
        "airpct_test",
        "acct_test",
    )
    payload = build_audit_log()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "audit_log"
    assert payload["summary"]["events"] == 1
    assert payload["summary"]["action_counts"]["customer_created"] == 1
    assert payload["events"][0]["target_api_key"] == "airpct_test"


def test_v1_customer_onboarding_contract(tmp_path, monkeypatch):
    registry = tmp_path / "api_key_registry.csv"
    accounts = tmp_path / "customer_accounts.csv"
    registry.write_text("key,plan,status\n")
    accounts.write_text("account_id,customer_name,api_key,plan,status\n")

    monkeypatch.setattr("api.onboarding_core.API_KEY_REGISTRY_FILE", registry)
    monkeypatch.setattr("api.onboarding_core.CUSTOMER_ACCOUNTS_FILE", accounts)

    payload = create_customer_api_key("Acme Test", "pro")

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["status"] == "created"
    assert payload["account"]["customer_name"] == "Acme Test"
    assert payload["account"]["plan"] == "pro"
    assert payload["api_key"].startswith("airpct_")
    assert "Acme Test" in accounts.read_text()
    assert payload["api_key"] in registry.read_text()


def test_v1_customer_lifecycle_contract(tmp_path, monkeypatch):
    registry = tmp_path / "api_key_registry.csv"
    accounts = tmp_path / "customer_accounts.csv"
    registry.write_text("key,plan,status\nairpct_test,pro,active\n")
    accounts.write_text(
        "account_id,customer_name,api_key,plan,status\n"
        "acct_test,Test Buyer,airpct_test,pro,active\n"
    )

    monkeypatch.setattr("api.onboarding_core.API_KEY_REGISTRY_FILE", registry)
    monkeypatch.setattr("api.onboarding_core.CUSTOMER_ACCOUNTS_FILE", accounts)

    revoked = revoke_customer_api_key("airpct_test")

    assert revoked["status"] == "updated"
    assert revoked["key_status"] == "revoked"
    assert "airpct_test,pro,revoked" in registry.read_text()
    assert "acct_test,Test Buyer,airpct_test,pro,revoked" in accounts.read_text()

    reactivated = reactivate_customer_api_key("airpct_test")

    assert reactivated["key_status"] == "active"
    assert "airpct_test,pro,active" in registry.read_text()
    assert "acct_test,Test Buyer,airpct_test,pro,active" in accounts.read_text()


def test_v1_limit_status_contract():
    now = datetime(2026, 6, 22, 12, 0, 0)
    records = [
        {"timestamp": "2026-06-22 09:00:00", "api_key": "demo-free-key", "endpoint": "/v1/signals"},
        {"timestamp": "2026-06-01 09:00:00", "api_key": "demo-free-key", "endpoint": "/v1/signals"},
        {"timestamp": "2026-05-31 09:00:00", "api_key": "demo-free-key", "endpoint": "/v1/signals"},
    ]

    status = build_limit_status("free", records, now)

    assert not status["limited"]
    assert status["daily_calls"] == 1
    assert status["monthly_calls"] == 2
    assert status["daily_remaining"] == 49


def test_v1_enforce_plan_limits_blocks_exhausted_plan(monkeypatch):
    today = date.today().isoformat()
    records = [
        {"timestamp": f"{today} 09:00:00", "api_key": "demo-free-key", "endpoint": "/v1/signals"}
        for _ in range(50)
    ]

    monkeypatch.setattr("api.access.read_usage_records", lambda: records)

    with pytest.raises(HTTPException) as exc:
        enforce_plan_limits("free", "demo-free-key")

    assert exc.value.status_code == 429
    assert exc.value.detail["reason"] == "daily_limit_exceeded"


def test_main_app_exposes_v1_core_routes():
    paths = {getattr(route, "path", "") for route in app.routes}

    assert "/v1/terminal-summary" in paths
    assert "/v1/dashboard-snapshot" in paths
    assert "/v1/data-trust-status" in paths
    assert "/v1/trust-remediation-plan" in paths
    assert "/v1/provider-connector-readiness" in paths
    assert "/v1/provider-connector-upgrade-plan" in paths
    assert "/v1/market-pulse" in paths
    assert "/v1/market-pulse-history" in paths
    assert "/v1/market-pulse/snapshot" in paths
    assert "/v1/market-pulse-brief" in paths
    assert "/v1/market-pulse-brief/save" in paths
    assert "/v1/provider-risk-radar" in paths
    assert "/v1/daily-change-brief" in paths
    assert "/v1/api-catalog" in paths
    assert "/v1/access-status" in paths
    assert "/v1/plan-limits" in paths
    assert "/v1/usage-summary" in paths
    assert "/v1/commercial-snapshot" in paths
    assert "/v1/sales-pipeline" in paths
    assert "/v1/customer-admin" in paths
    assert "/v1/account-health" in paths
    assert "/v1/revenue-forecast" in paths
    assert "/v1/commercial-board-report" in paths
    assert "/v1/commercial-board-report/html" in paths
    assert "/v1/commercial-board-report/save" in paths
    assert "/v1/audit-log" in paths
    assert "/v1/operations-status" in paths
    assert "/v1/launch-controls" in paths
    assert "/v1/customers" in paths
    assert "/v1/customers/revoke" in paths
    assert "/v1/customers/reactivate" in paths
    assert "/v1/reports/latest" in paths
    assert "/v1/signals" in paths
    assert "/v1/recommendations" in paths
    assert "/v1/executive-brief" in paths
    assert "/v1/customer-report" in paths
    assert "/v1/customer-report/html" in paths
    assert "/v1/customer-report/save" in paths
