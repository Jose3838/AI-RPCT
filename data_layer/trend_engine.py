import csv


SNAPSHOT_FILE = "market_snapshot_history.csv"


def load_market_snapshots():
    rows = []

    try:
        with open(SNAPSHOT_FILE, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append({
                    "date": row["timestamp"],
                    "coverage": float(row["coverage"]),
                    "market_strength": float(row["market_strength"]),
                    "avg_activation_score": float(row["avg_activation_score"])
                })

    except FileNotFoundError:
        return []

    return rows


def calculate_change(current, previous):
    return round(current - previous, 2)


def build_market_trend_summary():
    snapshots = load_market_snapshots()

    if len(snapshots) < 2:
        return {
            "status": "not_enough_data",
            "message": "At least 2 snapshots are required."
        }

    latest = snapshots[-1]
    previous = snapshots[-2]

    market_strength_change = calculate_change(
        latest["market_strength"],
        previous["market_strength"]
    )

    activation_score_change = calculate_change(
        latest["avg_activation_score"],
        previous["avg_activation_score"]
    )

    coverage_change = calculate_change(
        latest["coverage"],
        previous["coverage"]
    )

    if market_strength_change > 0:
        trend_signal = "improving"
    elif market_strength_change < 0:
        trend_signal = "declining"
    else:
        trend_signal = "stable"

    return {
        "status": "ok",
        "version": "v1",
        "latest_date": latest["date"],
        "previous_date": previous["date"],
        "market_strength_change": market_strength_change,
        "avg_activation_score_change": activation_score_change,
        "coverage_change": coverage_change,
        "trend_signal": trend_signal
    }
