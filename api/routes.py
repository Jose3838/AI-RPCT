from fastapi import APIRouter
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
