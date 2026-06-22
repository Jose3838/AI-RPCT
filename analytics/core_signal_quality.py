from pathlib import Path

import pandas as pd

from analytics.core_signal_history import build_core_signal_history_summary


DATA_DIR = Path("data")


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def band(score):
    if score >= 85:
        return "strong"
    if score >= 65:
        return "usable"
    if score >= 40:
        return "needs_work"
    return "weak"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_first(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[0].to_dict()


def build_core_signal_quality():
    history = build_core_signal_history_summary()
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    reliability = read_first(DATA_DIR / "provider_reliability_ranking.csv")

    history_score = min(100.0, (history.get("days_collected", 0) / 30) * 100)
    scarcity_explainability = 100.0 if all(
        key in scarcity
        for key in [
            "availability_pressure_score",
            "price_pressure_score",
            "frontier_pressure_score",
            "provider_depth_score",
        ]
    ) else 40.0
    forecast_confidence = as_float(forecast.get("confidence_score"))
    reliability_score = as_float(reliability.get("reliability_score"))

    quality_score = round(
        (history_score * 0.35)
        + (scarcity_explainability * 0.20)
        + (forecast_confidence * 0.25)
        + (reliability_score * 0.20),
        2
    )

    blockers = []
    if history.get("days_collected", 0) < 30:
        blockers.append("collect_30_days_of_core_signal_history")
    if forecast_confidence < 70:
        blockers.append("increase_forecast_confidence")
    if reliability_score < 60:
        blockers.append("improve_provider_reliability_depth")

    return pd.DataFrame([{
        "core_signal_quality_score": quality_score,
        "quality_band": band(quality_score),
        "days_collected": history.get("days_collected", 0),
        "history_coverage_band": history.get("coverage_band"),
        "scarcity_explainability_score": scarcity_explainability,
        "forecast_confidence_score": forecast_confidence,
        "top_provider_reliability_score": reliability_score,
        "paid_beta_signal_ready": quality_score >= 75 and history.get("days_collected", 0) >= 30,
        "blockers": ", ".join(blockers) if blockers else "none",
    }])


def main():
    result = build_core_signal_quality()
    result.to_csv(DATA_DIR / "core_signal_quality.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
