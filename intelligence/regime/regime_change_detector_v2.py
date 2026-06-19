import pandas as pd

FILE = "data/regime_history.csv"

def regime_change_detector_v2():

    try:
        df = pd.read_csv(FILE)
    except Exception:
        return {
            "status": "no_regime_history",
            "changed": False
        }

    if len(df) < 2:
        return {
            "status": "insufficient_data",
            "changed": False
        }

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    changed = latest["regime"] != previous["regime"]

    return {
        "status": "ok",
        "changed": bool(changed),
        "previous_regime": previous["regime"],
        "current_regime": latest["regime"]
    }
