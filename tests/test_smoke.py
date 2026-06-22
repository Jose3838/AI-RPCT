from datetime import datetime
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
from analytics.forecast_signal import build_forecast_signal
from analytics.gpu_scarcity_index import build_gpu_scarcity_index
from analytics.provider_reliability_ranking import build_provider_reliability_ranking
from analytics.provider_daily_metrics import build_provider_daily_metrics
from analytics.provider_health import build_provider_health
from analytics.provider_reliability_gaps import build_provider_reliability_gaps
from analytics.core_signal_history import (
    append_core_signal_history,
    build_core_signal_history_summary,
)
from analytics.core_signal_quality import build_core_signal_quality
from snapshot_scheduler import run_scheduled_snapshot
from security.limits import build_limit_status
from security.entitlements import has_access
from security.plan_resolver import resolve_plan

def test_core_files_exist():
    assert Path("main.py").exists()
    assert Path("api/routes.py").exists()
    assert Path("run_daily.sh").exists()
    assert Path("scripts/run_core_intelligence.sh").exists()
    assert Path("analytics/market_pulse_snapshot.py").exists()
    assert Path("analytics/core_signal_history.py").exists()
    assert Path("analytics/core_signal_quality.py").exists()
    assert Path("README.md").exists()


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
    assert "terminal" in payload
    assert "risk" in payload
    assert "core_signal_health" in payload
    assert "history_records" in payload["core_signal_health"]
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


def test_provider_reliability_gaps_prioritize_stale_history():
    ranking = pd.DataFrame([
        {
            "provider": "vast",
            "reliability_score": 45,
            "freshness_score": 20,
            "depth_score": 100,
            "history_days": 3,
            "availability_score": 90,
        }
    ])

    gaps = build_provider_reliability_gaps(ranking)

    assert gaps.iloc[0]["priority"] == "high"
    assert "stale_provider_data" in set(gaps["gap"])
    assert "insufficient_reliability_history" in set(gaps["gap"])


def test_core_signal_history_summary_tracks_days(tmp_path):
    history_file = tmp_path / "core_signal_history.csv"

    append_core_signal_history(history_file=history_file, generated_at="2026-06-21T09:00:00+00:00")
    append_core_signal_history(history_file=history_file, generated_at="2026-06-22T09:00:00+00:00")
    summary = build_core_signal_history_summary(history_file)

    assert summary["record_count"] == 2
    assert summary["days_collected"] == 2
    assert summary["coverage_band"] == "thin_history"
    assert "gpu_scarcity_index" in summary["deltas"]


def test_core_signal_quality_contract():
    quality = build_core_signal_quality().iloc[0]

    assert 0 <= quality["core_signal_quality_score"] <= 100
    assert quality["quality_band"] in {"strong", "usable", "needs_work", "weak"}
    assert "paid_beta_signal_ready" in quality
    assert "blockers" in quality


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
    assert "capacity_forecast_score" in payload["core_metrics"]
    assert "Core Signal Quality" in payload["markdown"]


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
    assert isinstance(payload["files"], list)


def test_v1_launch_controls_contract():
    payload = build_launch_controls()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert payload["report_type"] == "launch_controls"
    assert "billing_ready" in payload["controls"]
    assert "terms_ready" in payload["controls"]
    assert "paid_customers_allowed" in payload["controls"]


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
    records = [
        {"timestamp": "2026-06-22 09:00:00", "api_key": "demo-free-key", "endpoint": "/v1/signals"}
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
