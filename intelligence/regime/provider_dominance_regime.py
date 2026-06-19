import pandas as pd

FILE = "data/provider_market_share_history.csv"


def provider_dominance_regime():

    df = pd.read_csv(FILE)

    if df.empty:
        return {
            "status": "empty",
            "regime": "unknown"
        }

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True
    )

    df["market_share_pct"] = pd.to_numeric(
        df["market_share_pct"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "timestamp",
            "provider",
            "market_share_pct"
        ]
    )

    if df.empty:
        return {
            "status": "invalid_data",
            "regime": "unknown"
        }

    latest_ts = df["timestamp"].max()

    latest = df[
        df["timestamp"] == latest_ts
    ].copy()

    if latest.empty:
        return {
            "status": "no_latest_snapshot",
            "regime": "unknown"
        }

    leader = latest.sort_values(
        "market_share_pct",
        ascending=False
    ).iloc[0]

    share = float(
        leader["market_share_pct"]
    )

    if share >= 90:
        regime = "extreme_dominance"
    elif share >= 70:
        regime = "dominant_provider"
    elif share >= 50:
        regime = "concentrated_market"
    else:
        regime = "fragmented_market"

    provider = leader["provider"]

    provider_history = df[
        df["provider"] == provider
    ].sort_values("timestamp")

    trend = "flat"

    if len(provider_history) >= 2:
        previous = float(
            provider_history.iloc[-2]["market_share_pct"]
        )

        delta = round(
            share - previous,
            4
        )

        if delta > 1:
            trend = "rising"
        elif delta < -1:
            trend = "falling"
        else:
            trend = "flat"
    else:
        delta = 0.0

    first_ts = provider_history["timestamp"].min()

    hours_active = round(
        (latest_ts - first_ts).total_seconds() / 3600,
        2
    )

    return {
        "status": "ok",
        "dominant_provider": provider,
        "market_share_pct": round(share, 4),
        "regime": regime,
        "trend": trend,
        "delta_pct": delta,
        "hours_observed": hours_active,
        "latest_timestamp": latest_ts.isoformat(),
        "provider_count": int(latest["provider"].nunique())
    }
