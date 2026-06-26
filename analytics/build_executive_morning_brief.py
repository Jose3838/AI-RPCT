from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUTS = [
    DATA / "executive_morning_brief.csv",
    ROOT / "warehouse" / "decision" / "executive_morning_brief.csv",
]

FIELDS = [
    "brief_id",
    "generated_at",
    "market_status",
    "capacity_risk",
    "procurement_recommendation",
    "forecast_status",
    "platform_health",
    "summary",
]


def load_csv(filename: str) -> list[dict[str, str]]:
    path = DATA / filename

    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def first_value(rows: list[dict[str, str]], key: str, default: str = "") -> str:
    if not rows:
        return default

    return rows[0].get(key, default)


def build_brief() -> dict[str, str]:
    decision = load_csv("decision_summary.csv")
    forecast = load_csv("forecast_engine_v1_output.csv")
    health = load_csv("pipeline_health_summary.csv")
    quality = load_csv("data_quality_metrics.csv")

    recommendation = first_value(
        decision,
        "recommendation",
        "Continue monitoring AI infrastructure signals",
    )

    confidence = first_value(decision, "confidence", "0.0")

    market_status = "stable"
    capacity_risk = "watch"
    forecast_status = "operational" if forecast else "missing"
    platform_health = "healthy" if health and quality else "degraded"

    summary = (
        f"AI-RPCT recommends: {recommendation}. "
        f"Decision confidence is {confidence}. "
        f"Forecast status is {forecast_status}. "
        f"Platform health is {platform_health}. "
        f"Capacity risk is currently marked as {capacity_risk}."
    )

    return {
        "brief_id": "brief-001",
        "generated_at": datetime.now(UTC).isoformat(),
        "market_status": market_status,
        "capacity_risk": capacity_risk,
        "procurement_recommendation": recommendation,
        "forecast_status": forecast_status,
        "platform_health": platform_health,
        "summary": summary,
    }


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    brief = build_brief()

    for output in OUTPUTS:
        write_csv(output, brief)

    print("Executive morning brief generated.")
    print(DATA / "executive_morning_brief.csv")
    print(ROOT / "warehouse" / "decision" / "executive_morning_brief.csv")


if __name__ == "__main__":
    main()
