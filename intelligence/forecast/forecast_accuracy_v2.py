import pandas as pd

FILE = "data/forecast_audit_history.csv"


def forecast_accuracy_v2():

    try:
        df = pd.read_csv(FILE)
    except Exception:
        return {
            "status": "no_forecast_audit_data",
            "accuracy_score": 0
        }

    if df.empty:
        return {
            "status": "empty_forecast_audit_data",
            "accuracy_score": 0
        }

    df["recent_price"] = pd.to_numeric(
        df["recent_price"],
        errors="coerce"
    )

    df["historical_price"] = pd.to_numeric(
        df["historical_price"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "gpu_model",
            "signal",
            "recent_price",
            "historical_price"
        ]
    )

    if df.empty:
        return {
            "status": "invalid_forecast_audit_data",
            "accuracy_score": 0
        }

    df["price_delta_pct"] = (
        (df["recent_price"] - df["historical_price"])
        / df["historical_price"].replace(0, pd.NA)
        * 100
    )

    def expected_signal(delta):
        if delta > 5:
            return "bullish"
        if delta < -5:
            return "bearish"
        return "neutral"

    df["expected_signal"] = df["price_delta_pct"].apply(expected_signal)
    df["correct"] = df["signal"] == df["expected_signal"]

    total = len(df)
    correct = int(df["correct"].sum())

    signal_counts = df["signal"].value_counts().to_dict()

    by_signal = {}

    for signal in sorted(df["signal"].dropna().unique()):
        signal_df = df[df["signal"] == signal]

        by_signal[signal] = {
            "rows": int(len(signal_df)),
            "accuracy_pct": round(
                signal_df["correct"].mean() * 100,
                2
            )
        }

    by_gpu = []

    for gpu in sorted(df["gpu_model"].dropna().unique()):
        gpu_df = df[df["gpu_model"] == gpu]

        by_gpu.append({
            "gpu_model": gpu,
            "rows": int(len(gpu_df)),
            "accuracy_pct": round(
                gpu_df["correct"].mean() * 100,
                2
            ),
            "latest_signal": gpu_df.iloc[-1]["signal"]
        })

    by_gpu = sorted(
        by_gpu,
        key=lambda x: x["rows"],
        reverse=True
    )

    return {
        "status": "ok",
        "version": "v2",
        "forecast_rows": int(total),
        "correct_rows": correct,
        "accuracy_score": round(correct / total * 100, 2),
        "signal_counts": signal_counts,
        "by_signal": by_signal,
        "by_gpu": by_gpu[:20]
    }
