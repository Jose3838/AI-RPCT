import math

from fastapi import APIRouter, Header
import pandas as pd
from pathlib import Path


def _json_safe(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def read_csv(path):
    if not Path(path).exists():
        return []
    records = pd.read_csv(path).to_dict(orient="records")
    return [
        {key: _json_safe(value) for key, value in row.items()}
        for row in records
    ]

router = APIRouter()


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


@router.get("/cron-health")
def cron_health():
    import pandas as pd
    return pd.read_csv("data/cron_health.csv").to_dict(orient="records")


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


@router.get("/api-inventory")
def api_inventory():
    import pandas as pd
    return pd.read_csv("data/api_inventory_runtime.csv").to_dict(orient="records")


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


@router.get("/sales-demo-bundle")
def sales_demo_bundle():
    return {
        "product": "AI-RPCT",
        "vision": "Bloomberg for AI Infrastructure",

        "product_status": {
            "dashboard": True,
            "api_catalog": True,
            "monetization": True,
            "enterprise_reports": True
        },

        "market_coverage": {
            "live_providers": 2,
            "target_providers": 6,
            "coverage_pct": 33.33
        },

        "data_moat": {
            "historical_tracking": True,
            "gpu_price_history": True,
            "provider_health_history": True,
            "market_share_history": True
        },

        "intelligence": {
            "forecasting_engine": True,
            "volatility_engine": True,
            "market_intelligence": True
        },

        "commercial": {
            "free_plan": True,
            "pro_plan": True,
            "enterprise_plan": True,
            "api_key_gating": True
        },

        "current_stage": "commercial_launch_ready"
    }
