from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException

ROOT = Path(__file__).resolve().parents[1]

app = FastAPI(
    title="AI-RPCT Registry API",
    version="2.0",
    description="Governed registry API for AI-RPCT.",
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
def registry(name: str):
    path = registry_path(name)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Registry not found: {name}",
        )

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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
