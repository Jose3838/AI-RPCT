from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "region_scarcity_heatmap.csv"


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def scarcity_band(score):
    if score >= 75:
        return "critical"
    if score >= 50:
        return "elevated"
    if score >= 25:
        return "watch"
    return "stable"


def build_region_scarcity_heatmap(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    snapshots = read_csv(data_dir / "manual_market_snapshots.csv")
    required = {"region_code", "price_per_hour", "availability", "source_url"}
    if snapshots.empty or not required.issubset(snapshots.columns):
        return pd.DataFrame([{
            "region_code": "unknown",
            "status": "no_region_snapshots",
            "region_scarcity_score": 0.0,
            "scarcity_band": "unknown",
            "snapshot_count": 0,
            "source_labeled_count": 0,
            "avg_price_per_hour": 0.0,
            "avg_availability": 0.0,
            "claim_scope": "research_preview",
            "next_action": "Collect source-labeled manual snapshots by region before using regional heatmaps.",
        }])

    frame = snapshots.copy()
    frame["price_per_hour"] = pd.to_numeric(frame["price_per_hour"], errors="coerce").fillna(0)
    frame["availability"] = pd.to_numeric(frame["availability"], errors="coerce").fillna(0)
    frame["has_source_url"] = frame["source_url"].astype(str).str.startswith(("http://", "https://"))

    rows = []
    for region, group in frame.groupby("region_code"):
        avg_price = float(group["price_per_hour"].mean())
        avg_availability = float(group["availability"].mean())
        price_pressure = min(100.0, max(0.0, ((avg_price - 0.75) / 2.75) * 100))
        availability_pressure = min(100.0, max(0.0, ((2500 - avg_availability) / 2500) * 100))
        source_penalty = 0 if bool(group["has_source_url"].all()) else 10
        score = round(min(100.0, (price_pressure * 0.45) + (availability_pressure * 0.45) + source_penalty), 2)
        rows.append({
            "region_code": region,
            "status": "region_heatmap_ready",
            "region_scarcity_score": score,
            "scarcity_band": scarcity_band(score),
            "snapshot_count": int(len(group)),
            "source_labeled_count": int(group["has_source_url"].sum()),
            "avg_price_per_hour": round(avg_price, 4),
            "avg_availability": round(avg_availability, 2),
            "claim_scope": "research_preview",
            "next_action": "Continue collecting region-level source-labeled snapshots.",
        })

    return pd.DataFrame(rows).sort_values("region_scarcity_score", ascending=False)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_region_scarcity_heatmap()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
