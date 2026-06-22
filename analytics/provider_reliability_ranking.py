from pathlib import Path

import pandas as pd


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, float(value)))


def reliability_band(score):
    if score >= 80:
        return "strong"
    if score >= 60:
        return "watch"
    if score >= 40:
        return "weak"
    return "critical"


def build_provider_reliability_ranking(health, daily_metrics=None):
    health = health.copy()
    health["health_score"] = pd.to_numeric(health["health_score"], errors="coerce").fillna(0)
    health["rows"] = pd.to_numeric(health["rows"], errors="coerce").fillna(0)
    health["freshness_hours"] = pd.to_numeric(health["freshness_hours"], errors="coerce").fillna(999)

    metric_rows = {}
    if daily_metrics is not None and not daily_metrics.empty:
        metrics = daily_metrics.copy()
        metrics["availability"] = pd.to_numeric(metrics["availability"], errors="coerce").fillna(0)
        metrics["price_per_hour"] = pd.to_numeric(metrics["price_per_hour"], errors="coerce").fillna(0)
        grouped = metrics.groupby("provider")
        for provider, group in grouped:
            avg_availability = group["availability"].mean()
            price_std = group["price_per_hour"].std()
            metric_rows[provider] = {
                "avg_availability": avg_availability,
                "price_std": 0 if pd.isna(price_std) else price_std,
                "history_days": group["date"].nunique() if "date" in group.columns else len(group),
            }

    rows = []
    for _, row in health.iterrows():
        provider = row.get("provider")
        metrics = metric_rows.get(provider, {})

        freshness_score = clamp(100 - (float(row["freshness_hours"]) * 2))
        depth_score = clamp((float(row["rows"]) / 100) * 100)
        availability_score = clamp((float(metrics.get("avg_availability", 0)) / 2500) * 100)
        price_stability_score = clamp(100 - (float(metrics.get("price_std", 0)) * 35))
        history_score = clamp((float(metrics.get("history_days", 0)) / 30) * 100)

        reliability_score = round(clamp(
            (float(row["health_score"]) * 0.35)
            + (freshness_score * 0.20)
            + (depth_score * 0.15)
            + (availability_score * 0.10)
            + (price_stability_score * 0.10)
            + (history_score * 0.10)
        ), 2)

        enriched = row.to_dict()
        enriched.update({
            "reliability_score": reliability_score,
            "reliability_band": reliability_band(reliability_score),
            "freshness_score": round(freshness_score, 2),
            "depth_score": round(depth_score, 2),
            "availability_score": round(availability_score, 2),
            "price_stability_score": round(price_stability_score, 2),
            "history_score": round(history_score, 2),
        })
        rows.append(enriched)

    ranking = pd.DataFrame(rows)
    return ranking.sort_values(
        ["reliability_score", "health_score", "rows"],
        ascending=False
    )


def main():
    health = pd.read_csv("data/provider_health.csv")
    metrics_path = Path("data/provider_daily_metrics.csv")
    daily_metrics = pd.read_csv(metrics_path) if metrics_path.exists() else None

    ranking = build_provider_reliability_ranking(health, daily_metrics)
    ranking.to_csv("data/provider_reliability_ranking.csv", index=False)
    print(ranking)


if __name__ == "__main__":
    main()
