import pandas as pd

FORECAST_FILE = "data/forecast_snapshot_history.csv"

def forecast_outcome_tracker():

    try:
        df = pd.read_csv(
            FORECAST_FILE
        )

    except Exception:
        return {
            "status": "no_data"
        }

    return {
        "snapshots": len(df),
        "avg_alpha_candidates":
            round(
                df["alpha_candidates"]
                .astype(float)
                .mean(),
                2
            )
    }
