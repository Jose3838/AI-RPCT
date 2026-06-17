import csv
from collections import defaultdict


def read_csv(file_name):
    try:
        with open(file_name, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def build_market_history_summary():
    rows = read_csv("market_snapshot_history.csv")

    if not rows:
        return {
            "status": "no_data"
        }

    first = rows[0]
    latest = rows[-1]

    return {
        "status": "ok",
        "records": len(rows),
        "first_date": first["date"],
        "latest_date": latest["date"],
        "coverage_change": round(
            float(latest["coverage"]) - float(first["coverage"]),
            2
        ),
        "market_strength_change": round(
            float(latest["market_strength"]) - float(first["market_strength"]),
            2
        ),
        "activation_score_change": round(
            float(latest["avg_activation_score"]) - float(first["avg_activation_score"]),
            2
        )
    }


def build_provider_performance_history():
    rows = read_csv("provider_activation_score_history.csv")

    grouped = defaultdict(list)

    for row in rows:
        grouped[row["provider"]].append(
            float(row["activation_score"])
        )

    providers = []

    for provider, scores in grouped.items():
        providers.append({
            "provider": provider,
            "records": len(scores),
            "first_score": scores[0],
            "latest_score": scores[-1],
            "score_change": round(scores[-1] - scores[0], 2),
            "avg_score": round(sum(scores) / len(scores), 2)
        })

    return {
        "status": "ok",
        "providers": providers
    }


def build_historical_intelligence():
    return {
        "status": "ok",
        "version": "v1",
        "market_history": build_market_history_summary(),
        "provider_performance": build_provider_performance_history()
    }
