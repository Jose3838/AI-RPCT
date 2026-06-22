from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_provider_reliability_gaps(ranking):
    if ranking.empty:
        return pd.DataFrame([{
            "provider": "all",
            "priority": "high",
            "gap": "missing_provider_reliability_ranking",
            "recommended_action": "Run provider_health, provider_daily_metrics and provider_reliability_ranking.",
            "evidence": "No provider reliability rows were available.",
        }])

    rows = []
    for _, provider in ranking.iterrows():
        name = provider.get("provider", "unknown")
        reliability_score = as_float(provider.get("reliability_score"))
        freshness_score = as_float(provider.get("freshness_score"))
        depth_score = as_float(provider.get("depth_score"))
        history_days = as_float(provider.get("history_days"))
        availability_score = as_float(provider.get("availability_score"))
        used_fallback = str(provider.get("used_fallback", "")).lower() in {"true", "1", "yes"}
        ingestion_status = str(provider.get("ingestion_status", "unknown"))

        if used_fallback or ingestion_status == "fallback":
            rows.append({
                "provider": name,
                "priority": "high",
                "gap": "provider_ingestion_using_fallback",
                "recommended_action": "Restore fresh live provider ingestion or rotate credentials before relying on the provider score.",
                "evidence": f"ingestion_status={ingestion_status}, used_fallback={used_fallback}",
            })

        if freshness_score < 60:
            rows.append({
                "provider": name,
                "priority": "high",
                "gap": "stale_provider_data",
                "recommended_action": "Refresh live provider ingestion and verify connector scheduling.",
                "evidence": f"freshness_score={freshness_score}, reliability_score={reliability_score}",
            })

        if history_days < 30:
            rows.append({
                "provider": name,
                "priority": "high" if history_days < 7 else "medium",
                "gap": "insufficient_reliability_history",
                "recommended_action": "Collect daily provider metrics until 30 distinct history days are available.",
                "evidence": f"history_days={history_days}",
            })

        if depth_score < 50:
            rows.append({
                "provider": name,
                "priority": "medium",
                "gap": "thin_provider_depth",
                "recommended_action": "Increase offer coverage or add a second source for this provider.",
                "evidence": f"depth_score={depth_score}",
            })

        if availability_score < 40:
            rows.append({
                "provider": name,
                "priority": "medium",
                "gap": "weak_availability_signal",
                "recommended_action": "Validate availability fields and capture offer-level capacity where possible.",
                "evidence": f"availability_score={availability_score}",
            })

    if not rows:
        rows.append({
            "provider": "all",
            "priority": "low",
            "gap": "none",
            "recommended_action": "Continue daily collection and monitor reliability drift.",
            "evidence": "All tracked providers meet current reliability thresholds.",
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    gaps = pd.DataFrame(rows)
    gaps["priority_sort"] = gaps["priority"].map(priority_order).fillna(9)
    return gaps.sort_values(["priority_sort", "provider", "gap"]).drop(columns=["priority_sort"])


def main():
    ranking_path = DATA_DIR / "provider_reliability_ranking.csv"
    ranking = pd.read_csv(ranking_path) if ranking_path.exists() else pd.DataFrame()
    gaps = build_provider_reliability_gaps(ranking)
    gaps.to_csv(DATA_DIR / "provider_reliability_gaps.csv", index=False)
    print(gaps)


if __name__ == "__main__":
    main()
