from pathlib import Path

import pandas as pd

from analytics.manual_snapshot_quality import filter_valid_manual_snapshots, normalize, read_csv


DATA_DIR = Path("data")


def priority_items(frame, column, limit):
    if frame.empty or column not in frame:
        return []
    frame = frame.copy()
    if column == "provider" and "provider_type" in frame:
        type_weight = {
            "marketplace": 0,
            "cloud_gpu": 1,
            "public_cloud": 2,
        }
        frame["provider_type_weight"] = frame["provider_type"].map(type_weight).fillna(3)
        return frame.sort_values(
            ["tracking_priority", "provider_type_weight", column],
            ascending=[True, True, True],
        ).head(limit).to_dict(orient="records")
    sort_columns = ["tracking_priority", column] if "tracking_priority" in frame else [column]
    ascending = [True, True] if "tracking_priority" in frame else [True]
    return frame.sort_values(sort_columns, ascending=ascending).head(limit).to_dict(orient="records")


def already_collected(valid_snapshots):
    if valid_snapshots.empty:
        return set()
    return {
        (
            normalize(row.get("provider")),
            normalize(row.get("gpu")),
            normalize(row.get("region_code")),
        )
        for _, row in valid_snapshots.iterrows()
    }


def build_snapshot_collection_plan(data_dir=DATA_DIR, limit=25):
    data_dir = Path(data_dir)
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")
    snapshots = read_csv(data_dir / "manual_market_snapshots.csv")
    valid_snapshots = filter_valid_manual_snapshots(
        snapshots,
        gpu_universe,
        provider_universe,
        region_universe,
    )
    collected = already_collected(valid_snapshots)

    gpus = priority_items(gpu_universe, "gpu", 10)
    providers = priority_items(provider_universe, "provider", 8)
    regions = priority_items(region_universe, "region_code", 6)

    candidates = []
    for provider in providers:
        for gpu in gpus:
            for region in regions:
                key = (
                    normalize(provider.get("provider")),
                    normalize(gpu.get("gpu")),
                    normalize(region.get("region_code")),
                )
                if key in collected:
                    continue

                priority_score = round(
                    (4 - float(provider.get("tracking_priority", 3))) * 30
                    + (4 - float(gpu.get("tracking_priority", 3))) * 20
                    + (4 - float(region.get("tracking_priority", 3))) * 10,
                    2,
                )
                candidates.append({
                    "provider": provider.get("provider"),
                    "gpu": gpu.get("gpu"),
                    "region_code": region.get("region_code"),
                    "priority_score": priority_score,
                    "source_type": "manual_public_snapshot",
                    "claim_scope": "research_preview",
                    "recommended_action": "Find a public source page and add one source-labeled row to data/manual_market_snapshot_inbox.csv.",
                })

    candidates = sorted(candidates, key=lambda row: row["priority_score"], reverse=True)
    provider_order = [provider.get("provider") for provider in providers]
    plan = []
    while candidates and len(plan) < limit:
        added_this_round = False
        for provider in provider_order:
            if len(plan) >= limit:
                break
            for index, candidate in enumerate(candidates):
                if candidate["provider"] != provider:
                    continue
                plan.append(candidate)
                candidates.pop(index)
                added_this_round = True
                break
        if not added_this_round:
            break

    if not plan:
        plan.append({
            "provider": "n/a",
            "gpu": "n/a",
            "region_code": "n/a",
            "priority_score": 0.0,
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "recommended_action": "Maintain current valid snapshot coverage.",
        })

    return pd.DataFrame(plan)


def main():
    result = build_snapshot_collection_plan()
    result.to_csv(DATA_DIR / "snapshot_collection_plan.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
