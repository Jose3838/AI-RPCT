from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "forecast_accuracy.csv"


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def build_forecast_accuracy(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    history = read_csv(data_dir / "core_signal_history.csv")
    required = {"date", "capacity_forecast_score", "gpu_scarcity_index"}
    if history.empty or not required.issubset(history.columns) or len(history) < 2:
        return pd.DataFrame([{
            "status": "insufficient_history",
            "evaluation_count": 0,
            "directional_accuracy_pct": 0.0,
            "claim_scope": "research_preview",
            "paid_safe": False,
            "next_action": "Collect at least two daily core signal history rows before evaluating forecast accuracy.",
        }])

    frame = history.copy()
    frame["capacity_forecast_score"] = pd.to_numeric(frame["capacity_forecast_score"], errors="coerce")
    frame["gpu_scarcity_index"] = pd.to_numeric(frame["gpu_scarcity_index"], errors="coerce")
    frame = frame.dropna(subset=["capacity_forecast_score", "gpu_scarcity_index"])
    if len(frame) < 2:
        return pd.DataFrame([{
            "status": "insufficient_valid_history",
            "evaluation_count": 0,
            "directional_accuracy_pct": 0.0,
            "claim_scope": "research_preview",
            "paid_safe": False,
            "next_action": "Fix numeric forecast and scarcity history rows before evaluating accuracy.",
        }])

    hits = 0
    evaluations = 0
    rows = frame.to_dict(orient="records")
    for current, following in zip(rows[:-1], rows[1:]):
        predicted_pressure = float(current["capacity_forecast_score"]) >= 50
        actual_pressure_up = float(following["gpu_scarcity_index"]) >= float(current["gpu_scarcity_index"])
        if predicted_pressure == actual_pressure_up:
            hits += 1
        evaluations += 1

    accuracy = round((hits / evaluations) * 100, 2) if evaluations else 0.0
    paid_safe = evaluations >= 30 and accuracy >= 55
    status = "forecast_accuracy_ready" if evaluations >= 2 else "thin_forecast_history"

    return pd.DataFrame([{
        "status": status,
        "evaluation_count": int(evaluations),
        "directional_accuracy_pct": accuracy,
        "claim_scope": "research_preview",
        "paid_safe": bool(paid_safe),
        "next_action": (
            "Maintain forecast validation history until at least 30 evaluations are available."
            if not paid_safe
            else "Forecast accuracy gate can support controlled paid-beta review."
        ),
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_forecast_accuracy()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
