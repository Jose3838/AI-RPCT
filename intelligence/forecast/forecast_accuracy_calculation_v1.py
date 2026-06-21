import pandas as pd

FILE = "data/forecast_audit_history.csv"

def forecast_accuracy_calculation_v1():

    try:
        df = pd.read_csv(FILE)
    except Exception:
        return {
            "status": "no_forecast_audit_data",
            "accuracy_score": 0
        }

    if len(df) == 0:
        return {
            "status": "empty_forecast_audit_data",
            "accuracy_score": 0
        }

    signal_counts = df["signal"].value_counts().to_dict()

    non_neutral = len(
        df[df["signal"] != "neutral"]
    )

    score = round(
        non_neutral / len(df) * 100,
        2
    )

    return {
        "status": "ok",
        "forecast_rows": int(len(df)),
        "signal_counts": signal_counts,
        "alpha_signal_rate": score
    }
