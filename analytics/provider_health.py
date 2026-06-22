import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


def normalize_provider_name(provider):
    provider = str(provider).strip().lower()
    if provider.endswith("_real"):
        provider = provider[:-5]
    if provider == "lambda":
        return "lambda_labs"
    return provider


def freshness_band(hours):
    if hours is None:
        return "missing"
    if hours <= 6:
        return "fresh"
    if hours <= 24:
        return "usable"
    if hours <= 72:
        return "stale"
    return "expired"


def freshness_score(hours):
    if hours is None:
        return 0
    return max(0, min(100, 100 - (float(hours) * 2)))


def build_provider_health(provider_files, now=None):
    now = now or datetime.now()
    rows = []

    for provider, file_path in provider_files:
        provider = normalize_provider_name(provider)
        status = "offline"
        rows_count = 0
        freshness_hours = None
        error = ""

        path = Path(file_path)

        if path.exists():
            try:
                df = pd.read_csv(path)
                if "provider" in df.columns:
                    df["provider"] = df["provider"].map(normalize_provider_name)

                rows_count = len(df)
                if rows_count > 0:
                    status = "online"

                if "timestamp" in df.columns and rows_count > 0:
                    latest = pd.to_datetime(df["timestamp"], errors="coerce").max()
                    if pd.notna(latest):
                        if latest.tzinfo is not None:
                            latest = latest.tz_convert(timezone.utc).tz_localize(None)
                        freshness_hours = round((now - latest).total_seconds() / 3600, 2)
                    else:
                        error = "timestamp_parse_failed"
                elif rows_count > 0:
                    error = "missing_timestamp"
            except Exception as exc:
                error = f"read_failed:{type(exc).__name__}"

        fresh_score = freshness_score(freshness_hours)
        depth_score = max(0, min(100, (rows_count / 100) * 100))
        health_score = round((fresh_score * 0.55) + (depth_score * 0.35) + (10 if status == "online" else 0), 2)

        rows.append({
            "provider": provider,
            "status": status,
            "rows": rows_count,
            "freshness_hours": freshness_hours,
            "freshness_band": freshness_band(freshness_hours),
            "freshness_score": round(fresh_score, 2),
            "depth_score": round(depth_score, 2),
            "health_score": health_score,
            "error": error
        })

    return pd.DataFrame(rows)


providers = [
    ("vast", "data/vast_live_report.csv"),
    ("runpod", "data/runpod_live_report.csv")
]


def main():
    health = build_provider_health(providers)
    health.to_csv(
        "data/provider_health.csv",
        index=False
    )
    print(health)


if __name__ == "__main__":
    main()
