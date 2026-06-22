from datetime import datetime
from pathlib import Path

import pytest
from fastapi import HTTPException

from main import app
from api.terminal_core import (
    build_dashboard_snapshot,
    build_executive_brief,
    build_market_signals,
    build_recommendations,
    build_terminal_summary,
)
from intelligence.reports.customer_report_pdf_export_v1 import (
    build_customer_report_html,
    build_customer_report_payload,
)
from api.access import (
    build_access_status,
    build_plan_limits,
    build_usage_summary,
    enforce_plan_limits,
)
from api.commercial_core import build_commercial_snapshot, build_sales_pipeline
from security.limits import build_limit_status
from security.entitlements import has_access
from security.plan_resolver import resolve_plan

def test_core_files_exist():
    assert Path("main.py").exists()
    assert Path("api/routes.py").exists()
    assert Path("run_daily.sh").exists()
    assert Path("README.md").exists()


def test_v1_terminal_summary_contract():
    payload = build_terminal_summary()

    assert payload["product"] == "AI-RPCT"
    assert payload["mission"] == "Bloomberg for AI Infrastructure"
    assert "terminal" in payload
    assert "risk" in payload
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


def test_v1_market_signals_contract():
    payload = build_market_signals()

    assert payload["product"] == "AI-RPCT"
    assert payload["version"] == "v1"
    assert isinstance(payload["signals"], list)
    assert payload["signal_count"] == len(payload["signals"])


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
    assert not has_access("free", "/v1/usage-summary")
    assert has_access("pro", "/v1/usage-summary")
    assert not has_access("pro", "/v1/commercial-snapshot")
    assert has_access("enterprise", "/v1/commercial-snapshot")
    assert not has_access("pro", "/v1/sales-pipeline")
    assert has_access("enterprise", "/v1/sales-pipeline")
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
    assert "/v1/api-catalog" in paths
    assert "/v1/access-status" in paths
    assert "/v1/plan-limits" in paths
    assert "/v1/usage-summary" in paths
    assert "/v1/commercial-snapshot" in paths
    assert "/v1/sales-pipeline" in paths
    assert "/v1/reports/latest" in paths
    assert "/v1/signals" in paths
    assert "/v1/recommendations" in paths
    assert "/v1/executive-brief" in paths
    assert "/v1/customer-report" in paths
    assert "/v1/customer-report/html" in paths
    assert "/v1/customer-report/save" in paths
