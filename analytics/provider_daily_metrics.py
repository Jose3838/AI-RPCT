import pandas as pd
from datetime import datetime
from pathlib import Path


def normalize_provider_name(provider):
    provider = str(provider).strip().lower()
    if provider.endswith("_real"):
        provider = provider[:-5]
    if provider == "lambda":
        return "lambda_labs"
    return provider


def build_provider_daily_metrics(rankings, run_date=None):
    run_date = run_date or datetime.now().strftime("%Y-%m-%d")
    rankings = rankings.copy()
    rankings["provider"] = rankings["provider"].map(normalize_provider_name)
    rankings["price_per_hour"] = pd.to_numeric(rankings["price_per_hour"], errors="coerce").fillna(0)
    rankings["availability"] = pd.to_numeric(rankings["availability"], errors="coerce").fillna(0)
    rankings["score"] = pd.to_numeric(rankings["score"], errors="coerce").fillna(0)
    rankings["date"] = run_date
    return rankings.sort_values(["provider", "score"], ascending=[True, False]).drop_duplicates(
        subset=["date", "provider"],
        keep="first"
    )


def append_provider_daily_metrics(history_file="data/provider_daily_metrics.csv"):
    rankings = build_provider_daily_metrics(pd.read_csv("data/provider_rankings.csv"))

    if Path(history_file).exists():
        old = pd.read_csv(history_file)
        if "provider" in old.columns:
            old["provider"] = old["provider"].map(normalize_provider_name)
        rankings = pd.concat(
            [old, rankings],
            ignore_index=True
        )
        rankings = rankings.drop_duplicates(subset=["date", "provider"], keep="last")

    rankings.to_csv(
        history_file,
        index=False
    )
    return rankings


def main():
    rankings = append_provider_daily_metrics()
    print(rankings.tail())


if __name__ == "__main__":
    main()
