from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "price_dislocation_signal.csv"


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def latest_snapshot(frame):
    if frame.empty or "timestamp" not in frame.columns:
        return frame.copy()
    snapshot = frame.copy()
    snapshot["timestamp"] = pd.to_datetime(snapshot["timestamp"], errors="coerce")
    latest = snapshot["timestamp"].max()
    if pd.isna(latest):
        return frame.copy()
    return snapshot[snapshot["timestamp"] == latest].copy()


def dislocation_band(score):
    if score >= 75:
        return "extreme"
    if score >= 50:
        return "wide"
    if score >= 25:
        return "watch"
    return "normal"


def build_price_dislocation_signal(gpu_data):
    snapshot = latest_snapshot(gpu_data)
    required = {"provider", "gpu", "price_per_hour"}
    if snapshot.empty or not required.issubset(snapshot.columns):
        return pd.DataFrame([{
            "status": "no_price_data",
            "price_dislocation_score": 0,
            "dislocation_band": "unknown",
            "tracked_gpu_count": 0,
            "tracked_offer_count": 0,
            "max_spread_pct": 0,
            "top_gpu": "",
            "cheapest_provider": "",
            "most_expensive_provider": "",
            "claim_scope": "research_preview",
            "next_action": "Collect source-labeled price observations before claiming dislocation signals.",
        }])

    snapshot = snapshot.copy()
    snapshot["price_per_hour"] = pd.to_numeric(snapshot["price_per_hour"], errors="coerce")
    snapshot = snapshot.dropna(subset=["price_per_hour"])
    snapshot = snapshot[snapshot["price_per_hour"] > 0]
    if snapshot.empty:
        return pd.DataFrame([{
            "status": "no_valid_prices",
            "price_dislocation_score": 0,
            "dislocation_band": "unknown",
            "tracked_gpu_count": 0,
            "tracked_offer_count": 0,
            "max_spread_pct": 0,
            "top_gpu": "",
            "cheapest_provider": "",
            "most_expensive_provider": "",
            "claim_scope": "research_preview",
            "next_action": "Fix price_per_hour values before calculating dislocation.",
        }])

    rows = []
    for gpu, group in snapshot.groupby("gpu"):
        if len(group) < 2:
            continue
        cheapest = group.sort_values("price_per_hour").iloc[0]
        expensive = group.sort_values("price_per_hour", ascending=False).iloc[0]
        median_price = float(group["price_per_hour"].median())
        min_price = float(cheapest["price_per_hour"])
        max_price = float(expensive["price_per_hour"])
        if median_price <= 0:
            continue
        spread_pct = round(((max_price - min_price) / median_price) * 100, 2)
        rows.append({
            "gpu": gpu,
            "offer_count": int(len(group)),
            "median_price_per_hour": round(median_price, 4),
            "min_price_per_hour": round(min_price, 4),
            "max_price_per_hour": round(max_price, 4),
            "spread_pct": spread_pct,
            "cheapest_provider": cheapest.get("provider", ""),
            "most_expensive_provider": expensive.get("provider", ""),
        })

    if not rows:
        return pd.DataFrame([{
            "status": "insufficient_cross_provider_prices",
            "price_dislocation_score": 0,
            "dislocation_band": "unknown",
            "tracked_gpu_count": int(snapshot["gpu"].nunique()),
            "tracked_offer_count": int(len(snapshot)),
            "max_spread_pct": 0,
            "top_gpu": "",
            "cheapest_provider": "",
            "most_expensive_provider": "",
            "claim_scope": "research_preview",
            "next_action": "Collect at least two provider prices per priority GPU.",
        }])

    detail = pd.DataFrame(rows).sort_values("spread_pct", ascending=False)
    top = detail.iloc[0]
    score = round(min(100.0, float(top["spread_pct"])), 2)
    band = dislocation_band(score)

    return pd.DataFrame([{
        "status": "price_dislocation_signal_ready",
        "price_dislocation_score": score,
        "dislocation_band": band,
        "tracked_gpu_count": int(detail["gpu"].nunique()),
        "tracked_offer_count": int(snapshot.shape[0]),
        "max_spread_pct": float(top["spread_pct"]),
        "top_gpu": top["gpu"],
        "cheapest_provider": top["cheapest_provider"],
        "most_expensive_provider": top["most_expensive_provider"],
        "claim_scope": "research_preview",
        "next_action": "Track source-labeled price spreads daily and validate persistence before paid claims.",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    gpu_data = read_csv(DATA_DIR / "gpu_data.csv")
    result = build_price_dislocation_signal(gpu_data)
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
