from fastapi import APIRouter, Header
import pandas as pd
from pathlib import Path

router = APIRouter()

def read_csv(path):
    if not Path(path).exists():
        return []
    return pd.read_csv(path).to_dict(orient="records")

@router.get("/rankings")
def rankings():
    return read_csv("data/provider_rankings.csv")

@router.get("/forecast")
def forecast():
    return read_csv("data/forecast_signal.csv")

@router.get("/rpct")
def rpct():
    return read_csv("data/rpct_scores.csv")

@router.get("/shortage")
def shortage():
    return read_csv("data/shortage_probability.csv")

@router.get("/investor")
def investor():
    import pandas as pd

    return pd.read_csv(
        "data/investor_metrics.csv"
    ).to_dict(orient="records")

@router.get("/db/rpct")
def db_rpct():
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/airpct.db")
    df = pd.read_sql_query("SELECT * FROM rpct_scores", conn)
    conn.close()

    return df.tail(20).to_dict(orient="records")


@router.get("/db/providers")
def db_providers():
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/airpct.db")
    df = pd.read_sql_query("SELECT * FROM provider_rankings", conn)
    conn.close()

    return df.to_dict(orient="records")


@router.get("/db/forecasts")
def db_forecasts():
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/airpct.db")
    df = pd.read_sql_query("SELECT * FROM forecasts", conn)
    conn.close()

    return df.to_dict(orient="records")

@router.get("/investor-dashboard")
def investor_dashboard():
    import pandas as pd
    from pathlib import Path

    path = Path("data/investor_dashboard.csv")
    if not path.exists():
        return {"error": "investor dashboard data not found"}

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/investor-dashboard")
def investor_dashboard():
    import pandas as pd
    from pathlib import Path

    path = Path("data/investor_dashboard.csv")
    if not path.exists():
        return {"error": "investor dashboard data not found"}

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/marketshare")
def marketshare():
    import pandas as pd

    return pd.read_csv(
        "data/provider_marketshare.csv"
    ).to_dict(orient="records")


@router.get("/concentration")
def concentration():
    import pandas as pd

    return pd.read_csv(
        "data/provider_concentration.csv"
    ).to_dict(orient="records")

@router.get("/alerts")
def alerts():
    import pandas as pd

    return pd.read_csv(
        "data/alerts.csv"
    ).to_dict(orient="records")

@router.get("/data-quality")
def data_quality():
    import pandas as pd
    return pd.read_csv("data/data_quality.csv").to_dict(orient="records")

@router.get("/usage")
def usage():
    import pandas as pd
    return pd.read_csv("data/usage_metrics.csv").to_dict(orient="records")

@router.get("/admin-summary")
def admin_summary():
    import pandas as pd
    return pd.read_csv("data/admin_summary.csv").to_dict(orient="records")

@router.get("/usage")
def usage():
    import pandas as pd
    return pd.read_csv("data/usage_metrics.csv").to_dict(orient="records")

@router.get("/pricing")
def pricing():
    import pandas as pd
    return pd.read_csv("data/pricing_tiers.csv").to_dict(orient="records")

@router.get("/customer-value")
def customer_value():
    import pandas as pd
    return pd.read_csv("data/customer_value.csv").to_dict(orient="records")

@router.get("/kpis")
def kpis():
    import pandas as pd
    return pd.read_csv(
        "data/kpi_dashboard.csv"
    ).to_dict(orient="records")

@router.get("/metrics")
def metrics():
    import pandas as pd

    return {
        "providers": len(
            pd.read_csv(
                "data/provider_rankings.csv"
            )
        ),
        "alerts": len(
            pd.read_csv(
                "data/alerts.csv"
            )
        ),
        "quality": float(
            pd.read_csv(
                "data/data_quality.csv"
            )["data_quality_score"].iloc[0]
        )
    }

@router.get("/system-status")
def system_status():
    return {
        "status": "online",
        "version": "17.4"
    }

@router.get("/providers-active")
def providers_active():
    from integrations.provider_registry import active_providers

    return {
        "providers": active_providers()
    }

@router.get("/executive-status")
def executive_status():
    return {
        "platform": "AI-RPCT",
        "stage": "beta",
        "version": "21.4"
    }

@router.get("/provider-errors")
def provider_errors():
    import pandas as pd
    from pathlib import Path

    path = Path("data/provider_errors.csv")
    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/provider-credentials")
def provider_credentials():
    import pandas as pd
    from pathlib import Path

    path = Path("data/provider_credentials.csv")
    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/provider-readiness")
def provider_readiness():
    import pandas as pd
    from pathlib import Path

    path = Path("data/provider_readiness.csv")
    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/logs")
def logs():
    from pathlib import Path

    path = Path("data/system.log")
    if not path.exists():
        return []

    return path.read_text().splitlines()[-50:]

@router.get("/health")
def health():
    return {
        "status": "ok"
    }

@router.get("/data-sources")
def data_sources():
    import pandas as pd
    return pd.read_csv("data/data_source_status.csv").to_dict(orient="records")

@router.get("/ai-index")
def ai_index():
    import pandas as pd

    return pd.read_csv(
        "data/ai_infrastructure_index.csv"
    ).to_dict(orient="records")

@router.get("/gpu-scarcity")
def gpu_scarcity():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_scarcity_index.csv"
    ).to_dict(orient="records")

@router.get("/provider-dominance")
def provider_dominance():
    import pandas as pd

    return pd.read_csv(
        "data/provider_dominance_index.csv"
    ).to_dict(orient="records")

@router.get("/cron-health")
def cron_health():
    import pandas as pd
    return pd.read_csv("data/cron_health.csv").to_dict(orient="records")

@router.get("/data-moat")
def data_moat():
    import pandas as pd
    return pd.read_csv("data/data_moat_score.csv").to_dict(orient="records")

@router.get("/daily-intelligence")
def daily_intelligence():
    from pathlib import Path

    reports = sorted(Path("reports").glob("daily_intelligence_summary_*.txt"))

    if not reports:
        return {"error": "no daily intelligence summary found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/provider-intelligence-readiness")
def provider_intelligence_readiness():
    import pandas as pd
    return pd.read_csv("data/provider_intelligence_readiness.csv").to_dict(orient="records")

@router.get("/raw-provider-archives")
def raw_provider_archives():
    from pathlib import Path

    folder = Path("warehouse/raw_providers")
    if not folder.exists():
        return []

    return [p.name for p in sorted(folder.glob("*.csv"))]

@router.get("/data-freshness")
def data_freshness():
    import pandas as pd
    return pd.read_csv("data/data_freshness.csv").to_dict(orient="records")

@router.get("/real-provider-todo")
def real_provider_todo():
    import pandas as pd
    return pd.read_csv("data/real_provider_todo.csv").to_dict(orient="records")

@router.get("/provider-live-readiness")
def provider_live_readiness():
    import pandas as pd

    return pd.read_csv(
        "data/provider_live_readiness.csv"
    ).to_dict(orient="records")

@router.get("/vast-live-report")
def vast_live_report():
    import pandas as pd
    from pathlib import Path

    path = Path("data/vast_live_report.csv")
    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/live-provider-status")
def live_provider_status():
    import pandas as pd
    return pd.read_csv("data/live_provider_status.csv").to_dict(orient="records")

@router.get("/provider-data-mode")
def provider_data_mode():
    import pandas as pd
    return pd.read_csv("data/provider_data_mode.csv").to_dict(orient="records")

@router.get("/public-beta-status")
def public_beta_status():
    import pandas as pd
    return pd.read_csv("data/public_beta_status.csv").to_dict(orient="records")

@router.get("/commercial-readiness")
def commercial_readiness():
    import pandas as pd
    return pd.read_csv("data/commercial_readiness.csv").to_dict(orient="records")

@router.get("/trust-status")
def trust_status():
    import pandas as pd
    return pd.read_csv("data/trust_status.csv").to_dict(orient="records")

@router.get("/launch-readiness")
def launch_readiness():
    import pandas as pd
    return pd.read_csv("data/launch_readiness.csv").to_dict(orient="records")

@router.get("/ai-index-history")
def ai_index_history():
    import pandas as pd
    return pd.read_csv(
        "data/ai_infrastructure_index_history.csv"
    ).to_dict(orient="records")

@router.get("/provider-history")
def provider_history():
    import pandas as pd
    return pd.read_csv(
        "data/provider_daily_metrics.csv"
    ).to_dict(orient="records")

@router.get("/index-history")
def index_history():
    import pandas as pd
    return pd.read_csv(
        "data/index_history.csv"
    ).to_dict(orient="records")

@router.get("/terminal")
def terminal():
    import pandas as pd

    result = {}

    try:
        result["ai_index"] = pd.read_csv(
            "data/ai_infrastructure_index.csv"
        ).iloc[-1].to_dict()
    except:
        pass

    try:
        result["gpu_scarcity"] = pd.read_csv(
            "data/gpu_scarcity_index.csv"
        ).iloc[-1].to_dict()
    except:
        pass

    try:
        result["data_moat"] = pd.read_csv(
            "data/data_moat_score.csv"
        ).iloc[-1].to_dict()
    except:
        pass

    try:
        result["provider_mode"] = pd.read_csv(
            "data/provider_data_mode.csv"
        ).iloc[-1].to_dict()
    except:
        pass

    return result

@router.get("/gpu-price-index")
def gpu_price_index():
    import pandas as pd

    return pd.read_csv(
        "data/live_gpu_price_index.csv"
    ).to_dict(orient="records")

@router.get("/gpu-price-history")
def gpu_price_history():
    import pandas as pd
    return pd.read_csv("data/live_gpu_price_history.csv").to_dict(orient="records")

@router.get("/live-offer-summary")
def live_offer_summary():
    import pandas as pd
    return pd.read_csv("data/live_offer_summary.csv").to_dict(orient="records")

@router.get("/gpu-rankings")
def gpu_rankings():
    import pandas as pd

    return {
        "most_expensive": pd.read_csv(
            "data/live_gpu_most_expensive.csv"
        ).to_dict(orient="records"),
        "cheapest": pd.read_csv(
            "data/live_gpu_cheapest.csv"
        ).to_dict(orient="records"),
        "most_available": pd.read_csv(
            "data/live_gpu_most_available.csv"
        ).to_dict(orient="records")
    }

@router.get("/gpu-market-brief")
def gpu_market_brief():
    import pandas as pd
    return pd.read_csv(
        "data/gpu_market_brief.csv"
    ).to_dict(orient="records")

@router.get("/gpu-market-movers")
def gpu_market_movers():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_market_movers.csv"
    ).to_dict(orient="records")

@router.get("/live-gpu-alerts")
def live_gpu_alerts():
    import pandas as pd
    return pd.read_csv("data/live_gpu_alerts.csv").to_dict(orient="records")

@router.get("/weekly-infrastructure-report")
def weekly_infrastructure_report():
    from pathlib import Path

    reports = sorted(Path("reports").glob("weekly_infrastructure_report_*.txt"))

    if not reports:
        return {"error": "no weekly infrastructure report found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/runpod-live-report")
def runpod_live_report():
    import pandas as pd
    from pathlib import Path

    path = Path("data/runpod_live_report.csv")
    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/provider-comparison")
def provider_comparison():
    import pandas as pd

    return pd.read_csv(
        "data/provider_comparison.csv"
    ).to_dict(orient="records")

@router.get("/provider-health")
def provider_health():
    import pandas as pd

    return pd.read_csv(
        "data/provider_health.csv"
    ).to_dict(orient="records")

@router.get("/provider-reliability")
def provider_reliability():
    import pandas as pd

    return pd.read_csv(
        "data/provider_reliability_ranking.csv"
    ).to_dict(orient="records")

@router.get("/gpu-price-trend")
def gpu_price_trend():
    import pandas as pd

    return pd.read_csv(
        "data/gpu_price_trend_signal.csv"
    ).to_dict(orient="records")

@router.get("/terminal-summary")
def terminal_summary():
    import pandas as pd

    return pd.read_csv(
        "data/terminal_summary.csv"
    ).to_dict(orient="records")

@router.get("/public-status")
def public_status():
    return {
        "product": "AI-RPCT",
        "stage": "public_beta",
        "deployment": "railway",
        "live_provider_feeds": 2,
        "primary_data_sources": [
            "Vast.ai",
            "RunPod"
        ],
        "status": "online"
    }

@router.get("/terminal-kpis")
def terminal_kpis():
    import pandas as pd

    summary = pd.read_csv("data/terminal_summary.csv").iloc[-1].to_dict()
    provider_health = pd.read_csv("data/provider_health.csv")
    live_offers = pd.read_csv("data/live_provider_data.csv")
    runpod = pd.read_csv("data/runpod_live_report.csv")

    return {
        "ai_infrastructure_index": summary.get("ai_infrastructure_index"),
        "gpu_price_index": summary.get("gpu_price_index"),
        "gpu_price_trend": summary.get("gpu_price_trend"),
        "live_providers": len(provider_health[provider_health["status"] == "online"]),
        "vast_offers": len(live_offers),
        "runpod_gpu_types": len(runpod),
        "top_provider": summary.get("top_provider")
    }

@router.get("/api-inventory")
def api_inventory():
    import pandas as pd
    return pd.read_csv("data/api_inventory_runtime.csv").to_dict(orient="records")

@router.get("/market-data-moat")
def market_data_moat():
    import pandas as pd
    return pd.read_csv("data/market_data_moat_status.csv").to_dict(orient="records")

@router.get("/executive-snapshot")
def executive_snapshot():
    import pandas as pd

    return {
        "terminal_summary": pd.read_csv("data/terminal_summary.csv").iloc[-1].to_dict(),
        "provider_reliability": pd.read_csv("data/provider_reliability_ranking.csv").to_dict(orient="records"),
        "gpu_market_brief": pd.read_csv("data/gpu_market_brief.csv").iloc[-1].to_dict(),
        "market_data_moat": pd.read_csv("data/market_data_moat_status.csv").iloc[-1].to_dict()
    }

@router.get("/gpu-watchlist")
def gpu_watchlist():
    import pandas as pd
    return pd.read_csv("data/gpu_watchlist_intelligence.csv").to_dict(orient="records")

@router.get("/frontier-gpu-index")
def frontier_gpu_index():
    import pandas as pd
    return pd.read_csv("data/frontier_gpu_index.csv").to_dict(orient="records")

@router.get("/intelligence-signal")
def intelligence_signal():
    import pandas as pd
    return pd.read_csv("data/intelligence_signal_score.csv").to_dict(orient="records")

@router.get("/daily-terminal-brief")
def daily_terminal_brief():
    from pathlib import Path

    reports = sorted(Path("reports").glob("daily_terminal_brief_*.txt"))

    if not reports:
        return {"error": "no daily terminal brief found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/gpu-category-index")
def gpu_category_index():
    import pandas as pd
    return pd.read_csv("data/gpu_category_index.csv").to_dict(orient="records")

@router.get("/provider-coverage")
def provider_coverage():
    import pandas as pd
    return pd.read_csv("data/provider_coverage_score.csv").to_dict(orient="records")

@router.get("/scarcity-watchlist")
def scarcity_watchlist():
    import pandas as pd
    return pd.read_csv("data/scarcity_watchlist.csv").to_dict(orient="records")

@router.get("/terminal-risk")
def terminal_risk():
    import pandas as pd
    return pd.read_csv("data/terminal_risk_score.csv").to_dict(orient="records")

@router.get("/executive-ai-memo")
def executive_ai_memo():
    from pathlib import Path

    reports = sorted(Path("reports").glob("executive_ai_infrastructure_memo_*.txt"))

    if not reports:
        return {"error": "no executive memo found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/live-data-quality")
def live_data_quality():
    import pandas as pd
    return pd.read_csv("data/live_data_quality_score.csv").to_dict(orient="records")

@router.get("/live-provider-market-share")
def live_provider_market_share():
    import pandas as pd
    from pathlib import Path

    path = Path("data/live_provider_market_share.csv")

    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.get("/terminal-trend-history")
def terminal_trend_history():
    import pandas as pd
    return pd.read_csv("data/terminal_trend_history.csv").to_dict(orient="records")

@router.get("/live-provider-market-share-history")
def live_provider_market_share_history():
    import pandas as pd
    return pd.read_csv("data/live_provider_market_share_history.csv").to_dict(orient="records")

@router.get("/market-intelligence-snapshot")
def market_intelligence_snapshot():
    from pathlib import Path

    reports = sorted(Path("reports").glob("market_intelligence_snapshot_*.txt"))

    if not reports:
        return {"error": "no market intelligence snapshot found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/gpu-price-volatility")
def gpu_price_volatility():
    import pandas as pd
    return pd.read_csv("data/gpu_price_volatility.csv").to_dict(orient="records")

@router.get("/live-provider-dominance")
def live_provider_dominance():
    import pandas as pd
    return pd.read_csv("data/live_provider_dominance.csv").to_dict(orient="records")

@router.get("/ai-infrastructure-pulse")
def ai_infrastructure_pulse():
    import pandas as pd
    return pd.read_csv("data/ai_infrastructure_pulse.csv").to_dict(orient="records")

@router.get("/investor-snapshot")
def investor_snapshot():
    from pathlib import Path

    reports = sorted(Path("reports").glob("investor_snapshot_*.txt"))

    if not reports:
        return {"error": "no investor snapshot found"}

    latest = reports[-1]

    return {
        "file": latest.name,
        "content": latest.read_text()
    }

@router.get("/customer-value-score")
def customer_value_score():
    import pandas as pd
    return pd.read_csv("data/customer_value_score.csv").to_dict(orient="records")

@router.get("/founder-summary")
def founder_summary():
    import pandas as pd
    return pd.read_csv("data/founder_dashboard_summary.csv").to_dict(orient="records")

@router.get("/sales-readiness")
def sales_readiness():
    import pandas as pd
    return pd.read_csv("data/sales_readiness.csv").to_dict(orient="records")

@router.get("/history-summary")
def history_summary():
    import pandas as pd
    return pd.read_csv("data/history_summary.csv").to_dict(orient="records")

@router.get("/feedback-summary")
def feedback_summary():
    import pandas as pd
    return pd.read_csv("data/feedback_summary.csv").to_dict(orient="records")

@router.get("/public-usage-snapshot")
def public_usage_snapshot():
    import pandas as pd
    return pd.read_csv("data/public_usage_snapshot.csv").to_dict(orient="records")

@router.get("/customer-pipeline-summary")
def customer_pipeline_summary():
    import pandas as pd
    return pd.read_csv("data/customer_pipeline_summary.csv").to_dict(orient="records")

@router.get("/product-readiness")
def product_readiness():
    import pandas as pd
    return pd.read_csv("data/product_readiness_score.csv").to_dict(orient="records")

@router.get("/founder-operating-dashboard")
def founder_operating_dashboard():
    import pandas as pd
    return pd.read_csv("data/founder_operating_dashboard.csv").to_dict(orient="records")

@router.get("/dashboard-version")
def dashboard_version():
    return {
        "dashboard": "v2",
        "charts": True,
        "market_share": True,
        "price_history": True
    }

@router.get("/dashboard-health")
def dashboard_health():
    import pandas as pd
    return pd.read_csv("data/dashboard_health.csv").to_dict(orient="records")

@router.get("/dashboard-snapshot")
def dashboard_snapshot():
    import pandas as pd

    return {
        "terminal": pd.read_csv("data/terminal_summary.csv").iloc[-1].to_dict(),
        "risk": pd.read_csv("data/terminal_risk_score.csv").iloc[-1].to_dict(),
        "quality": pd.read_csv("data/live_data_quality_score.csv").iloc[-1].to_dict(),
        "market_share": pd.read_csv("data/live_provider_market_share.csv").to_dict(orient="records"),
        "gpu_rankings": pd.read_csv("data/live_gpu_most_expensive.csv").head(10).to_dict(orient="records"),
        "provider_health": pd.read_csv("data/provider_health.csv").to_dict(orient="records")
    }

@router.get("/api-catalog")
def api_catalog():
    import pandas as pd
    return pd.read_csv("data/api_catalog.csv").to_dict(orient="records")

@router.get("/public-roadmap")
def public_roadmap():
    from pathlib import Path
    return {
        "content": Path("docs/PUBLIC_ROADMAP.md").read_text()
    }

@router.get("/api-product-status")
def api_product_status():
    import pandas as pd
    return pd.read_csv("data/api_product_status.csv").to_dict(orient="records")

@router.get("/usage-plans")
def usage_plans():
    import pandas as pd
    return pd.read_csv("data/usage_plan_matrix.csv").to_dict(orient="records")

@router.get("/value-proposition")
def value_proposition():
    from pathlib import Path
    return {
        "content": Path("docs/VALUE_PROPOSITION.md").read_text()
    }

@router.get("/product-terminal-readiness")
def product_terminal_readiness():
    import pandas as pd
    return pd.read_csv("data/product_terminal_readiness.csv").to_dict(orient="records")

@router.get("/plan-access-matrix")
def plan_access_matrix():
    import pandas as pd
    return pd.read_csv("data/plan_access_matrix.csv").to_dict(orient="records")

@router.get("/entitlement-check")
def entitlement_check(endpoint: str, x_api_key: str = Header(default=None)):
    from security.plan_resolver import resolve_plan
    from security.entitlements import has_access

    plan = resolve_plan(x_api_key)

    return {
        "endpoint": endpoint,
        "plan": plan,
        "allowed": has_access(plan, endpoint)
    }

@router.get("/monetization-readiness")
def monetization_readiness():
    import pandas as pd
    return pd.read_csv("data/monetization_readiness.csv").to_dict(orient="records")

@router.get("/provider-health-history")
def provider_health_history(days: int = 30):
    import pandas as pd
    from pathlib import Path
    from datetime import datetime, timedelta, timezone

    path = Path("data/provider_health_history.csv")
    if not path.exists():
        return []

    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        return df.to_dict(orient="records")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df[df["timestamp"] >= cutoff]

    return df.to_dict(orient="records")


@router.get("/provider-market-share-history")
def provider_market_share_history(days: int = 30):
    import pandas as pd
    from pathlib import Path
    from datetime import datetime, timedelta, timezone

    path = Path("data/provider_market_share_history.csv")
    if not path.exists():
        return []

    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        return df.to_dict(orient="records")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df[df["timestamp"] >= cutoff]

    return df.to_dict(orient="records")


@router.get("/history-moat-status")
def history_moat_status():
    import pandas as pd
    from pathlib import Path

    files = {
        "gpu_price_history": Path("data/gpu_price_history.csv"),
        "provider_health_history": Path("data/provider_health_history.csv"),
        "provider_market_share_history": Path("data/provider_market_share_history.csv"),
    }

    result = {}
    for name, path in files.items():
        if path.exists():
            df = pd.read_csv(path)
            result[name] = {
                "exists": True,
                "rows": len(df),
                "columns": list(df.columns)
            }
        else:
            result[name] = {
                "exists": False,
                "rows": 0,
                "columns": []
            }

    return {
        "product": "AI-RPCT",
        "data_moat": "historical_snapshots",
        "status": "active",
        "files": result
    }

@router.get("/history-health")
def history_health():
    import pandas as pd
    from pathlib import Path

    files = [
        "data/gpu_price_history.csv",
        "data/provider_health_history.csv",
        "data/provider_market_share_history.csv"
    ]

    result = {}

    for file in files:
        p = Path(file)

        if p.exists():
            result[p.name] = len(pd.read_csv(p))
        else:
            result[p.name] = 0

    return result


@router.get("/usage-analytics")
def usage_analytics():
    import pandas as pd
    from pathlib import Path

    path = Path("data/usage_metrics.csv")

    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")

@router.post("/admin/run-history-snapshot")
def admin_run_history_snapshot():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "jobs/history_snapshot.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "error",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

@router.get("/dashboard-v5-readiness")
def dashboard_v5_readiness():
    import pandas as pd
    from pathlib import Path

    history_rows = 0

    files = [
        "data/gpu_price_history.csv",
        "data/provider_health_history.csv",
        "data/provider_market_share_history.csv"
    ]

    for f in files:
        p = Path(f)

        if p.exists():
            history_rows += len(pd.read_csv(p))

    return {
        "product": "AI-RPCT",
        "version": "5.0",
        "status": "active",
        "historical_data_rows": history_rows,
        "live_providers": 2,
        "data_moat_active": True,
        "monetization_ready": True,
        "sales_ready": True,
        "api_catalog_active": True
    }

@router.get("/executive-dashboard")
def executive_dashboard():
    import pandas as pd
    from pathlib import Path

    history_rows = 0

    history_files = [
        "data/gpu_price_history.csv",
        "data/provider_health_history.csv",
        "data/provider_market_share_history.csv"
    ]

    for f in history_files:
        p = Path(f)

        if p.exists():
            history_rows += len(pd.read_csv(p))

    return {
        "company": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "live_providers": 2,
        "historical_records": history_rows,
        "market_share_tracking": True,
        "health_tracking": True,
        "price_tracking": True,
        "monetization": "active",
        "sales": "ready",
        "stage": "data_moat_building"
    }

@router.get("/provider-expansion-status")
def provider_expansion_status():
    import pandas as pd

    providers = pd.read_csv("data/provider_registry.csv")

    return {
        "total_providers": len(providers),
        "live_providers": int(len(providers[providers["live"] == True])),
        "planned_providers": int(len(providers[providers["live"] == False])),
        "providers": providers.to_dict(orient="records")
    }

@router.get("/provider-coverage-index")
def provider_coverage_index():
    import pandas as pd

    providers = pd.read_csv("data/provider_registry.csv")

    total = len(providers)
    live = len(providers[providers["live"] == True])

    score = round((live / total) * 100, 2)

    return {
        "coverage_score": score,
        "live_providers": live,
        "total_target_providers": total,
        "next_targets": [
            "CoreWeave",
            "Lambda",
            "Nebius",
            "Crusoe"
        ]
    }

@router.get("/gpu-forecast-signal")
def gpu_forecast_signal():
    import pandas as pd
    from pathlib import Path

    path = Path("data/gpu_price_forecast_signal.csv")

    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")


@router.post("/admin/run-forecasting-engine")
def admin_run_forecasting_engine():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "analytics/forecasting_engine.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "error",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

@router.get("/gpu-forecast-signal-safe")
def gpu_forecast_signal_safe():
    import pandas as pd
    from pathlib import Path

    path = Path("data/gpu_price_forecast_signal.csv")

    if not path.exists():
        return [{
            "signal": "no_file",
            "trend": "unknown",
            "volatility": 0,
            "latest_price_index": None,
            "previous_price_index": None,
            "change_pct": None
        }]

    try:
        return pd.read_csv(path).to_dict(orient="records")
    except Exception as e:
        return [{
            "signal": "read_error",
            "trend": "unknown",
            "error": str(e)
        }]
