from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "customer_watchlists.csv"


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def read_latest(path):
    records = read_records(path)
    return records[-1] if records else {}


def add_watch(rows, watch_type, name, priority, reason, evidence_file, next_action):
    rows.append({
        "watch_type": watch_type,
        "name": name,
        "priority": priority,
        "reason": reason,
        "evidence_file": evidence_file,
        "next_action": next_action,
    })


def build_customer_watchlists():
    rows = []
    snapshot_targets = read_records(DATA_DIR / "snapshot_collection_plan.csv")
    provider_gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv")
    region_heatmap = read_records(DATA_DIR / "region_scarcity_heatmap.csv")
    dislocation = read_latest(DATA_DIR / "price_dislocation_signal.csv")
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")

    for target in snapshot_targets[:10]:
        add_watch(
            rows,
            "snapshot_target",
            f"{target.get('provider')} / {target.get('gpu')} / {target.get('region_code')}",
            target.get("priority", "medium"),
            "Priority collection target for building the defensible daily evidence moat.",
            "data/snapshot_collection_plan.csv",
            "collect_source_labeled_snapshot",
        )

    for gap in provider_gaps[:10]:
        add_watch(
            rows,
            "provider",
            gap.get("provider", "unknown"),
            gap.get("priority", "medium"),
            gap.get("gap", "provider reliability gap"),
            "data/provider_reliability_gaps.csv",
            gap.get("recommended_action", "review_provider_reliability"),
        )

    for region in region_heatmap[:10]:
        add_watch(
            rows,
            "region",
            region.get("region_code", "unknown"),
            region.get("scarcity_band", "watch"),
            "Region-level scarcity pressure should be monitored for procurement decisions.",
            "data/region_scarcity_heatmap.csv",
            "collect_region_snapshot",
        )

    if dislocation:
        add_watch(
            rows,
            "price_dislocation",
            str(dislocation.get("top_gpu", "tracked GPUs")),
            dislocation.get("dislocation_band", "watch"),
            "Cross-provider price dispersion can create procurement or arbitrage signals.",
            "data/price_dislocation_signal.csv",
            "compare_provider_prices_before_buying",
        )

    if scarcity:
        add_watch(
            rows,
            "market_signal",
            "GPU Scarcity Index",
            scarcity.get("scarcity_band", "watch"),
            "Daily scarcity signal is a core customer decision watch item.",
            "data/gpu_scarcity_index.csv",
            "monitor_daily_scarcity_direction",
        )

    if not rows:
        add_watch(
            rows,
            "system",
            "watchlist_baseline",
            "medium",
            "No watchlist inputs are available yet.",
            "data/customer_watchlists.csv",
            "run_core_intelligence_pipeline",
        )

    priority_rank = {"critical": 0, "high": 1, "elevated": 2, "watch": 3, "medium": 4, "stable": 5, "low": 6}
    return pd.DataFrame(rows).sort_values(
        by="priority",
        key=lambda column: column.map(lambda value: priority_rank.get(str(value).lower(), 9)),
    )


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_customer_watchlists()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result.head(20))


if __name__ == "__main__":
    main()
