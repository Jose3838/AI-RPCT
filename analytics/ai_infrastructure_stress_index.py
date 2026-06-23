from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "ai_infrastructure_stress_index.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, float(value)))


def stress_band(score):
    if score >= 75:
        return "critical"
    if score >= 55:
        return "elevated"
    if score >= 30:
        return "watch"
    return "stable"


def build_ai_infrastructure_stress_index(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    scarcity = read_latest(data_dir / "gpu_scarcity_index.csv")
    forecast = read_latest(data_dir / "forecast_signal.csv")
    dislocation = read_latest(data_dir / "price_dislocation_signal.csv")
    reliability = read_latest(data_dir / "provider_reliability_ranking.csv")

    scarcity_score = as_float(scarcity.get("gpu_scarcity_index"))
    forecast_score = as_float(forecast.get("forecast_score"))
    dislocation_score = as_float(dislocation.get("price_dislocation_score"))
    reliability_stress = clamp(100 - as_float(reliability.get("reliability_score")))

    stress_score = round(clamp(
        (scarcity_score * 0.35)
        + (forecast_score * 0.30)
        + (dislocation_score * 0.20)
        + (reliability_stress * 0.15)
    ), 2)

    return pd.DataFrame([{
        "status": "stress_index_ready",
        "ai_infrastructure_stress_index": stress_score,
        "stress_band": stress_band(stress_score),
        "gpu_scarcity_component": round(scarcity_score, 2),
        "capacity_forecast_component": round(forecast_score, 2),
        "price_dislocation_component": round(dislocation_score, 2),
        "provider_reliability_stress_component": round(reliability_stress, 2),
        "claim_scope": "research_preview",
        "next_action": "Validate stress-index usefulness against future market moves before paid claims.",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_ai_infrastructure_stress_index()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
