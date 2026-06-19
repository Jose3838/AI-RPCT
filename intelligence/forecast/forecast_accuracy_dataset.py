import pandas as pd

FILE = "data/forecast_audit_history.csv"

def forecast_accuracy_dataset():

    try:

        df = pd.read_csv(FILE)

    except Exception:

        return {
            "rows": 0
        }

    return {
        "rows": len(df),
        "gpu_models":
            df["gpu_model"]
            .nunique(),
        "signals":
            df["signal"]
            .nunique()
    }
