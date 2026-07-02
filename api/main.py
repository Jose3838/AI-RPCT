from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from copilot.models import (
    CopilotStatusResponseModel,
    ExecutiveDecisionCenterResponseModel,
    ExecutiveRecommendationResponseModel,
    RiskIntelligenceResponseModel,
    CopilotSummaryResponseModel,
    CopilotRecommendationResponseModel,
    CopilotDecisionResponseModel,
    CopilotTimelineResponseModel,
    CopilotAnalyticsResponseModel,
    DecisionIntelligenceResponseModel,
    ForecastIntelligenceResponseModel,
    ProviderIntelligenceResponseModel,
    CapacityIntelligenceResponseModel,
    ExecutiveIntelligenceResponseModel,
    ChangeIntelligenceResponseModel,
    ExecutiveSnapshotsResponseModel,
)

from copilot.service import (
    get_analytics,
    get_decision,
    get_decision_intelligence,
    get_decision_timeline,
    get_recommendation,
    get_status,
    get_summary,
    get_why,
    get_forecast_intelligence,
    get_provider_intelligence,
    get_capacity_intelligence,
    get_risk_intelligence,
    get_executive_intelligence,
    get_executive_insights,
    get_change_intelligence,
    get_executive_snapshots,
    run_executive_snapshot,
    get_executive_recommendation,
    get_executive_decision_center,
    get_executive_facade,
    get_executive_trend,
    get_historical_intelligence,
)

from copilot.intelligence_hub import get_intelligence_hub
from copilot.dashboard_executive import get_executive_dashboard
from copilot.dashboard_service import get_dashboard

ROOT = Path(__file__).resolve().parents[1]

app = FastAPI(
    title="AI-RPCT Registry API",
    version="2.0",
    description="Governed registry API for AI-RPCT.",
)

app.mount(
    "/web",
    StaticFiles(directory=ROOT / "web", html=True),
    name="web",
)


def load_csv(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset not found: {relative_path}",
        )

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def registry_path(name: str) -> Path:
    safe_name = name.replace("/", "").replace("\\", "")

    return ROOT / "data" / f"{safe_name}.csv"


@app.get("/")
def root():
    return {
        "service": "AI-RPCT Registry API",
        "status": "ok",
        "governance": "non_production",
        "version": "2.0",
    }


@app.get("/health")
def health():
    required = [
        ROOT / "data" / "registry_metadata.csv",
        ROOT / "data" / "feature_store.csv",
        ROOT / "data" / "forecast_engine_v1_output.csv",
    ]

    missing = [
        str(path.relative_to(ROOT))
        for path in required
        if not path.exists()
    ]

    return {
        "status": "ok" if not missing else "degraded",
        "missing": missing,
    }


@app.get("/pipeline")
def pipeline():
    return load_csv("data/pipeline_run_registry.csv")


@app.get("/registries")
def registries(
    search: str | None = None,
    sort: str | None = None,
    limit: int | None = None,
    offset: int = 0,
):
    rows = load_csv("data/registry_metadata.csv")

    if search:
        needle = search.lower()
        rows = [
            row
            for row in rows
            if any(needle in str(value).lower() for value in row.values())
        ]

    if sort:
        if rows and sort not in rows[0]:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown sort key: {sort}",
            )

        rows = sorted(rows, key=lambda row: row.get(sort, ""))

    if offset:
        rows = rows[offset:]

    if limit is not None:
        rows = rows[:limit]

    return rows


@app.get("/registry/{name}")
def registry(
    name: str,
    key: str | None = None,
    value: str | None = None,
    sort: str | None = None,
    limit: int | None = None,
    offset: int = 0,
):
    path = registry_path(name)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Registry not found: {name}",
        )

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if key is not None or value is not None:
        if key is None or value is None:
            raise HTTPException(
                status_code=400,
                detail="Both key and value must be provided.",
            )

        if rows and key not in rows[0]:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown filter key: {key}",
            )

        rows = [
            row
            for row in rows
            if row.get(key) == value
        ]

    if sort is not None:
        if rows and sort not in rows[0]:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown sort column: {sort}",
            )

        rows = sorted(rows, key=lambda r: r.get(sort, ""))

    rows = rows[offset:]

    if limit is not None:
        rows = rows[:limit]

    return rows


@app.get("/providers")
def providers():
    return load_csv("data/provider_entity_registry.csv")


@app.get("/capacity")
def capacity():
    return load_csv("data/historical_capacity_registry.csv")


@app.get("/forecast")
def forecast():
    return load_csv("data/forecast_engine_v1_output.csv")


@app.get("/features")
def features():
    return load_csv("data/feature_store.csv")


@app.get("/decision/latest")
def latest_decision():
    path = ROOT / "data" / "decision_summary.csv"

    if not path.exists():
        return {"status": "no decision available"}

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return {"status": "empty"}

    return rows[0]


@app.get("/copilot/why")
def copilot_why():
    return get_why()


@app.get(
    "/copilot/status",
    response_model=CopilotStatusResponseModel,
)
def copilot_status():
    return get_status()


@app.get(
    "/copilot/decision",
    response_model=CopilotDecisionResponseModel,
)
def copilot_decision():
    return get_decision()


@app.get(
    "/copilot/summary",
    response_model=CopilotSummaryResponseModel,
)
def copilot_summary():
    return get_summary()


@app.get(
    "/copilot/recommendation",
    response_model=CopilotRecommendationResponseModel,
)
def copilot_recommendation():
    return get_recommendation()


@app.get(
    "/copilot/timeline",
    response_model=CopilotTimelineResponseModel,
)
def copilot_timeline():
    return get_decision_timeline()


@app.get(
    "/copilot/analytics",
    response_model=CopilotAnalyticsResponseModel,
)
def copilot_analytics():
    return get_analytics()


@app.get(
    "/copilot/decision-intelligence",
    response_model=DecisionIntelligenceResponseModel,
)
def copilot_decision_intelligence():
    return get_decision_intelligence()


@app.get(
    "/copilot/forecast-intelligence",
    response_model=ForecastIntelligenceResponseModel,
)
def copilot_forecast_intelligence():
    return get_forecast_intelligence()


@app.get(
    "/copilot/provider-intelligence",
    response_model=ProviderIntelligenceResponseModel,
)
def copilot_provider_intelligence():
    return get_provider_intelligence()


@app.get(
    "/copilot/capacity-intelligence",
    response_model=CapacityIntelligenceResponseModel,
)
def copilot_capacity_intelligence():
    return get_capacity_intelligence()


@app.get(
    "/copilot/risk-intelligence",
    response_model=RiskIntelligenceResponseModel,
)
def copilot_risk_intelligence():
    return get_risk_intelligence()


@app.get(
    "/copilot/executive-intelligence",
    response_model=ExecutiveIntelligenceResponseModel,
)
def copilot_executive_intelligence():
    return get_executive_intelligence()


@app.get(
    "/copilot/change-intelligence",
    response_model=ChangeIntelligenceResponseModel,
)
def copilot_change_intelligence():
    return get_change_intelligence()


@app.get(
    "/copilot/executive-snapshots",
    response_model=ExecutiveSnapshotsResponseModel,
)
def copilot_executive_snapshots():
    return get_executive_snapshots()


@app.post("/copilot/executive-snapshot")
def copilot_run_executive_snapshot():
    return run_executive_snapshot()


@app.get(
    "/copilot/executive-recommendation",
    response_model=ExecutiveRecommendationResponseModel,
)
def copilot_executive_recommendation():
    return get_executive_recommendation()


@app.get(
    "/copilot/executive-decision-center",
    response_model=ExecutiveDecisionCenterResponseModel,
)
def copilot_executive_decision_center():
    return get_executive_decision_center()


@app.get("/copilot/executive-trend")
def copilot_executive_trend():
    return get_executive_trend()


@app.get("/copilot/executive-insights")
def copilot_executive_insights():
    return get_executive_insights()


@app.get("/copilot/executive-facade")
def copilot_executive_facade():
    return get_executive_facade()


@app.get("/copilot/historical")
def copilot_historical():
    return get_historical_intelligence()


@app.get("/pipeline-health")
def pipeline_health():
    rows = load_csv("data/pipeline_intelligence.csv")

    if not rows:
        return {
            "status": "pipeline health unavailable",
            "pipeline_health": 0,
        }

    return rows[0]


@app.get("/pipeline-history")
def pipeline_history():
    return load_csv("data/pipeline_history.csv")


@app.get("/copilot/intelligence-hub")
def copilot_intelligence_hub():
    return get_intelligence_hub()


@app.get("/dashboard/executive")
def dashboard_executive():
    return get_executive_dashboard()


@app.get("/dashboard")
def dashboard():
    return get_dashboard()


@app.get("/provider-rankings")
def provider_rankings():
    return load_csv("data/provider_rankings.csv")


@app.get("/provider-marketshare")
def provider_marketshare():
    return load_csv("data/provider_marketshare.csv")


@app.get("/registry-info/{name}")
def registry_info(name: str):
    path = registry_path(name)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Registry not found: {name}",
        )

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    columns = list(rows[0].keys()) if rows else []

    return {
        "registry_name": name,
        "rows": len(rows),
        "columns": len(columns),
        "column_names": columns,
        "status": "active",
    }
