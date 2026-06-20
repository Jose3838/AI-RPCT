import pandas as pd

FILE = "data/forecast_accuracy_history.csv"


def forecast_accuracy_trend():
    try:
        df = pd.read_csv(FILE)
    except Exception:
        return {
            "status": "no_accuracy_history",
            "forecast_quality_score": 0
        }

    if df.empty:
        return {
            "status": "empty_accuracy_history",
            "forecast_quality_score": 0
        }

    df["accuracy_score"] = pd.to_numeric(
        df["accuracy_score"],
        errors="coerce"
    )

    df["forecast_rows"] = pd.to_numeric(
        df["forecast_rows"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["accuracy_score"]
    )

    if df.empty:
        return {
            "status": "invalid_accuracy_history",
            "forecast_quality_score": 0
        }

    latest = float(df.iloc[-1]["accuracy_score"])
    average = float(df["accuracy_score"].mean())
    best = float(df["accuracy_score"].max())
    worst = float(df["accuracy_score"].min())

    trend = "flat"
    delta = 0.0

    if len(df) >= 2:
        previous = float(df.iloc[-2]["accuracy_score"])
        delta = round(latest - previous, 2)

        if delta > 1:
            trend = "improving"
        elif delta < -1:
            trend = "declining"

    rows = int(len(df))

    quality_score = 0

    if rows >= 3:
        quality_score += 20
    if rows >= 10:
        quality_score += 20
    if rows >= 30:
        quality_score += 20
    if latest >= 50:
        quality_score += 20
    if trend in ["flat", "improving"]:
        quality_score += 20

    return {
        "status": "ok",
        "version": "v1",
        "rows": rows,
        "latest_accuracy": round(latest, 2),
        "average_accuracy": round(average, 2),
        "best_accuracy": round(best, 2),
        "worst_accuracy": round(worst, 2),
        "trend": trend,
        "delta": delta,
        "forecast_quality_score": quality_score
    }
