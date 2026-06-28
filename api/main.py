from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from copilot.service import (
    get_analytics,
    get_decision,
    get_decision_timeline,
    get_recommendation,
    get_status,
    get_summary,
    get_why,
)

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
def registries():
    return load_csv("data/registry_metadata.csv")


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


@app.get("/copilot/status")
def copilot_status():
    return get_status()


@app.get("/copilot/decision")
def copilot_decision():
    return get_decision()


@app.get("/copilot/summary")
def copilot_summary():
    return get_summary()


@app.get("/copilot/recommendation")
def copilot_recommendation():
    return get_recommendation()


@app.get("/copilot/timeline")
def copilot_timeline():
    return get_decision_timeline()


@app.get("/copilot/analytics")
def copilot_analytics():
    return get_analytics()
