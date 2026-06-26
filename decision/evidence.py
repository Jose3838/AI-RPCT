from __future__ import annotations

import csv
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

@dataclass
class EvidenceItem:
    category: str
    description: str
    record_count: int

def load_csv(filename: str) -> list[dict[str, str]]:
    path = DATA / filename

    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def collect_evidence() -> list[EvidenceItem]:
    evidence = []

    forecast_rows = load_csv("forecast_engine_v1_output.csv")
    scarcity_rows = load_csv("gpu_scarcity_index.csv")
    provider_rows = load_csv("provider_health.csv")
    ranking_rows = load_csv("provider_rankings.csv")

    if forecast_rows:
        evidence.append(f"Forecast output available: {len(forecast_rows)} records")

    if scarcity_rows:
        evidence.append(f"GPU scarcity signal available: {len(scarcity_rows)} records")

    if provider_rows:
        evidence.append(f"Provider health data available: {len(provider_rows)} records")

    if ranking_rows:
        evidence.append(f"Provider ranking data available: {len(ranking_rows)} records")

    return evidence
