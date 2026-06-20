import pandas as pd

FILE = "data/forecast_audit_history.csv"


def forecast_backtesting_v2():

    try:
        df = pd.read_csv(FILE)
    except Exception:
        return {
            "status": "no_forecast_audit_data",
            "backtest_readiness_score": 0
        }

    if df.empty:
        return {
            "status": "empty_forecast_audit_data",
            "backtest_readiness_score": 0
        }

    df["recent_price"] = pd.to_numeric(df["recent_price"], errors="coerce")
    df["historical_price"] = pd.to_numeric(df["historical_price"], errors="coerce")

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
            "backtest_readiness_score": 0
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

    total_rows = int(len(df))
    gpu_models = int(df["gpu_model"].nunique())
    signal_types = int(df["signal"].nunique())
    accuracy_pct = round(df["correct"].mean() * 100, 2)

    by_signal = []

    for signal in sorted(df["signal"].dropna().unique()):
        signal_df = df[df["signal"] == signal]

        by_signal.append({
            "signal": signal,
            "rows": int(len(signal_df)),
            "accuracy_pct": round(signal_df["correct"].mean() * 100, 2)
        })

    by_gpu = []

    for gpu in sorted(df["gpu_model"].dropna().unique()):
        gpu_df = df[df["gpu_model"] == gpu]

        by_gpu.append({
            "gpu_model": gpu,
            "rows": int(len(gpu_df)),
            "accuracy_pct": round(gpu_df["correct"].mean() * 100, 2),
            "latest_signal": gpu_df.iloc[-1]["signal"],
            "avg_delta_pct": round(gpu_df["price_delta_pct"].mean(), 2)
        })

    best_gpu_forecasts = sorted(
        by_gpu,
        key=lambda x: (x["accuracy_pct"], x["rows"]),
        reverse=True
    )[:10]

    weakest_gpu_forecasts = sorted(
        by_gpu,
        key=lambda x: (x["accuracy_pct"], -x["rows"])
    )[:10]

    readiness = 0

    if total_rows >= 25:
        readiness += 25
    if total_rows >= 100:
        readiness += 25
    if gpu_models >= 10:
        readiness += 25
    if signal_types >= 3:
        readiness += 25

    return {
        "status": "ok",
        "version": "v2",
        "forecast_rows": total_rows,
        "gpu_models": gpu_models,
        "signal_types": signal_types,
        "accuracy_pct": accuracy_pct,
        "backtest_readiness_score": readiness,
        "by_signal": by_signal,
        "best_gpu_forecasts": best_gpu_forecasts,
        "weakest_gpu_forecasts": weakest_gpu_forecasts
    }
