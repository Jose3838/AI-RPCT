from fastapi import APIRouter

router = APIRouter()


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


@router.get("/providers-active")
def providers_active():
    from integrations.provider_registry import active_providers

    return {
        "providers": active_providers()
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


@router.get("/data-sources")
def data_sources():
    import pandas as pd
    return pd.read_csv("data/data_source_status.csv").to_dict(orient="records")


@router.get("/provider-dominance")
def provider_dominance():
    import pandas as pd

    return pd.read_csv(
        "data/provider_dominance_index.csv"
    ).to_dict(orient="records")


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


@router.get("/provider-history")
def provider_history():
    import pandas as pd
    return pd.read_csv(
        "data/provider_daily_metrics.csv"
    ).to_dict(orient="records")


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


@router.get("/provider-coverage")
def provider_coverage():
    import pandas as pd
    return pd.read_csv("data/provider_coverage_score.csv").to_dict(orient="records")


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


@router.get("/live-provider-market-share-history")
def live_provider_market_share_history():
    import pandas as pd
    return pd.read_csv("data/live_provider_market_share_history.csv").to_dict(orient="records")


@router.get("/live-provider-dominance")
def live_provider_dominance():
    import pandas as pd
    return pd.read_csv("data/live_provider_dominance.csv").to_dict(orient="records")


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


@router.get("/provider-registry")
def provider_registry():

    from collectors.providers.provider_registry import PROVIDERS

    return {
        "providers": PROVIDERS,
        "count": len(PROVIDERS)
    }


@router.get("/provider-coverage-engine-v2")
def provider_coverage_engine_v2():
    providers = [
        {"provider": "vast", "status": "active", "live": True, "priority": 1},
        {"provider": "runpod", "status": "active", "live": True, "priority": 1},
        {"provider": "coreweave", "status": "planned", "live": False, "priority": 2},
        {"provider": "lambda", "status": "planned", "live": False, "priority": 2},
        {"provider": "nebius", "status": "planned", "live": False, "priority": 2},
        {"provider": "crusoe", "status": "planned", "live": False, "priority": 2},
    ]

    total = len(providers)
    live = len([p for p in providers if p["live"]])
    planned = total - live

    return {
        "product": "AI-RPCT",
        "coverage_engine": "v2",
        "live_providers": live,
        "planned_providers": planned,
        "total_target_providers": total,
        "coverage_pct": round((live / total) * 100, 2),
        "status": "expanding",
        "next_activation_targets": [
            "coreweave",
            "lambda",
            "nebius",
            "crusoe"
        ],
        "providers": providers
    }
