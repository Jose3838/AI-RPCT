from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize(value):
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def coverage_pct(covered_count, total_count):
    if total_count <= 0:
        return 0.0
    return round((covered_count / total_count) * 100, 2)


def build_coverage_universe_status(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")
    gpu_data = read_csv(data_dir / "gpu_data.csv")
    manual_snapshots = read_csv(data_dir / "manual_market_snapshots.csv")
    provider_comparison = read_csv(data_dir / "provider_comparison.csv")

    tracked_gpus = set()
    if not gpu_data.empty and "gpu" in gpu_data:
        tracked_gpus |= {normalize(value) for value in gpu_data["gpu"].dropna()}
    if not manual_snapshots.empty and "gpu" in manual_snapshots:
        tracked_gpus |= {normalize(value) for value in manual_snapshots["gpu"].dropna()}

    tracked_providers = set()
    if not gpu_data.empty and "provider" in gpu_data:
        tracked_providers |= {normalize(value) for value in gpu_data["provider"].dropna()}
    if not provider_comparison.empty and "provider" in provider_comparison:
        tracked_providers |= {normalize(value) for value in provider_comparison["provider"].dropna()}
    if not manual_snapshots.empty and "provider" in manual_snapshots:
        tracked_providers |= {normalize(value) for value in manual_snapshots["provider"].dropna()}

    tracked_regions = set()
    if not manual_snapshots.empty and "region_code" in manual_snapshots:
        tracked_regions |= {normalize(value) for value in manual_snapshots["region_code"].dropna()}

    gpu_count = len(gpu_universe)
    provider_count = len(provider_universe)
    region_count = len(region_universe)

    covered_gpu_count = len([
        gpu for gpu in gpu_universe.get("gpu", [])
        if normalize(gpu) in tracked_gpus
    ])
    covered_provider_count = len([
        provider for provider in provider_universe.get("provider", [])
        if normalize(provider) in tracked_providers
    ])
    covered_region_count = len([
        region for region in region_universe.get("region_code", [])
        if normalize(region) in tracked_regions
    ])

    manual_snapshot_count = int(len(manual_snapshots))
    blockers = []
    if covered_gpu_count < 20:
        blockers.append("expand_tracked_gpu_snapshots")
    if covered_provider_count < 15:
        blockers.append("expand_tracked_provider_snapshots")
    if covered_region_count < 8:
        blockers.append("add_region_labeled_snapshots")
    if manual_snapshot_count == 0:
        blockers.append("add_manual_public_snapshots_with_sources")

    if not blockers:
        status = "coverage_ready_for_research_preview"
    elif gpu_count >= 20 and provider_count >= 15 and region_count >= 8:
        status = "universe_ready_snapshot_collection_needed"
    else:
        status = "coverage_universe_incomplete"

    return pd.DataFrame([{
        "status": status,
        "gpu_universe_count": gpu_count,
        "provider_universe_count": provider_count,
        "region_universe_count": region_count,
        "covered_gpu_count": covered_gpu_count,
        "covered_provider_count": covered_provider_count,
        "covered_region_count": covered_region_count,
        "gpu_coverage_pct": coverage_pct(covered_gpu_count, gpu_count),
        "provider_coverage_pct": coverage_pct(covered_provider_count, provider_count),
        "region_coverage_pct": coverage_pct(covered_region_count, region_count),
        "manual_snapshot_count": manual_snapshot_count,
        "claim_scope": "research_preview",
        "history_policy": "do_not_backfill_without_sources",
        "blockers": ", ".join(blockers) if blockers else "none",
        "next_action": (
            "Add source-labeled manual public snapshots for priority GPUs, providers and regions."
            if blockers
            else "Continue daily snapshot collection."
        ),
    }])


def main():
    result = build_coverage_universe_status()
    result.to_csv(DATA_DIR / "coverage_universe_status.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
