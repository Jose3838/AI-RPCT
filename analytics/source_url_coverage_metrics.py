from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "source_url_coverage_metrics.csv"


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def is_source_url(value):
    return str(value or "").startswith(("http://", "https://"))


def build_source_url_coverage_metrics(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    snapshots = read_csv(data_dir / "manual_market_snapshots.csv")
    if snapshots.empty:
        return pd.DataFrame([{
            "status": "no_manual_snapshots",
            "snapshot_count": 0,
            "source_url_count": 0,
            "source_url_coverage_pct": 0.0,
            "provider_with_source_count": 0,
            "gpu_with_source_count": 0,
            "region_with_source_count": 0,
            "claim_scope": "research_preview",
            "next_action": "Collect source-labeled public snapshots before claiming source coverage.",
        }])

    snapshots = snapshots.copy()
    snapshots["has_source_url"] = snapshots.get("source_url", "").map(is_source_url)
    source_rows = snapshots[snapshots["has_source_url"]]
    snapshot_count = len(snapshots)
    source_count = len(source_rows)
    coverage_pct = round((source_count / snapshot_count) * 100, 2) if snapshot_count else 0.0
    status = "source_coverage_ready" if coverage_pct == 100 else "source_coverage_incomplete"

    return pd.DataFrame([{
        "status": status,
        "snapshot_count": int(snapshot_count),
        "source_url_count": int(source_count),
        "source_url_coverage_pct": coverage_pct,
        "provider_with_source_count": int(source_rows["provider"].nunique()) if "provider" in source_rows else 0,
        "gpu_with_source_count": int(source_rows["gpu"].nunique()) if "gpu" in source_rows else 0,
        "region_with_source_count": int(source_rows["region_code"].nunique()) if "region_code" in source_rows else 0,
        "claim_scope": "research_preview",
        "next_action": "Keep every manual snapshot tied to a public source URL.",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_source_url_coverage_metrics()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
