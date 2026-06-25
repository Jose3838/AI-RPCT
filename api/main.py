from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]

app = FastAPI(
    title="AI-RPCT Registry API",
    version="1.0",
    description="Governed registry API for AI-RPCT.",
)


def load_csv(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@app.get("/")
def root():
    return {
        "service": "AI-RPCT Registry API",
        "status": "ok",
        "governance": "non_production",
    }


@app.get("/registries")
def registries():
    return load_csv("data/registry_metadata.csv")


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
