from fastapi import APIRouter

router = APIRouter()


@router.get("/executive-status")
def executive_status():
    return {
        "platform": "AI-RPCT",
        "stage": "beta",
        "version": "21.4"
    }


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


@router.get("/terminal-summary")
def terminal_summary():
    import pandas as pd

    return pd.read_csv(
        "data/terminal_summary.csv"
    ).to_dict(orient="records")


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


@router.get("/terminal-trend-history")
def terminal_trend_history():
    import pandas as pd
    return pd.read_csv("data/terminal_trend_history.csv").to_dict(orient="records")


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


@router.get("/history-summary")
def history_summary():
    import pandas as pd
    return pd.read_csv("data/history_summary.csv").to_dict(orient="records")


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
