from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "forecast_validation_history.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def build_forecast_validation_history():
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    accuracy = read_latest(DATA_DIR / "forecast_accuracy.csv")
    history = read_records(DATA_DIR / "core_signal_history.csv")

    enough_history = len(history) >= 30
    directional_accuracy = float(accuracy.get("directional_accuracy_pct", 0) or 0)
    confidence_score = float(forecast.get("confidence_score", 0) or 0)
    validation_score = round((directional_accuracy * 0.60) + (min(len(history), 30) / 30 * 100 * 0.40), 2)

    if enough_history and directional_accuracy >= 55:
        validation_band = "validated_research"
    elif len(history) >= 7:
        validation_band = "early_validation"
    else:
        validation_band = "thin_history"

    blockers = []
    if not enough_history:
        blockers.append("collect_30_days_of_core_signal_history")
    if directional_accuracy < 55:
        blockers.append("directional_accuracy_below_paid_claim_threshold")
    if confidence_score < 70:
        blockers.append("forecast_confidence_below_paid_claim_threshold")

    return pd.DataFrame([{
        "validation_band": validation_band,
        "forecast_score": forecast.get("forecast_score", 0),
        "capacity_shock_band": forecast.get("capacity_shock_band", "unknown"),
        "directional_accuracy_pct": directional_accuracy,
        "forecast_confidence_score": confidence_score,
        "history_records": len(history),
        "validation_score": validation_score,
        "paid_claim_safe": enough_history and directional_accuracy >= 55 and confidence_score >= 70,
        "blockers": ", ".join(blockers) if blockers else "none",
        "evidence_files": "data/forecast_signal.csv,data/forecast_accuracy.csv,data/core_signal_history.csv",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_forecast_validation_history()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
