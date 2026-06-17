import csv


def load_market_snapshots():
    try:
        with open(
            "market_snapshot_history.csv",
            "r"
        ) as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def build_trend_intelligence():
    snapshots = load_market_snapshots()

    if len(snapshots) < 2:
        return {
            "status": "not_enough_data"
        }

    first = snapshots[0]
    latest = snapshots[-1]

    market_strength_change = round(
        float(latest["market_strength"])
        -
        float(first["market_strength"]),
        2
    )

    activation_change = round(
        float(latest["avg_activation_score"])
        -
        float(first["avg_activation_score"]),
        2
    )

    return {
        "status": "ok",
        "version": "v2",
        "market_strength_change": market_strength_change,
        "activation_change": activation_change,
        "trend_direction": (
            "up"
            if market_strength_change > 0
            else "down"
            if market_strength_change < 0
            else "flat"
        )
    }
