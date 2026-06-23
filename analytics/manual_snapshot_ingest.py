from pathlib import Path

import pandas as pd

from analytics.coverage_universe_status import build_coverage_universe_status
from analytics.manual_snapshot_quality import (
    REQUIRED_COLUMNS,
    build_manual_snapshot_quality,
    filter_valid_manual_snapshots,
    read_csv,
    row_blockers,
    normalize,
)


DATA_DIR = Path("data")
INBOX_FILE = DATA_DIR / "manual_market_snapshot_inbox.csv"
MASTER_FILE = DATA_DIR / "manual_market_snapshots.csv"
REJECTED_FILE = DATA_DIR / "manual_market_snapshot_rejections.csv"
DEDUP_COLUMNS = ["snapshot_date", "provider", "gpu", "region_code", "source_url"]


def empty_snapshot_frame():
    return pd.DataFrame(columns=[*REQUIRED_COLUMNS, "notes"])


def ensure_columns(frame):
    frame = frame.copy()
    for column in [*REQUIRED_COLUMNS, "notes"]:
        if column not in frame.columns:
            frame[column] = ""
    return frame[[*REQUIRED_COLUMNS, "notes"]]


def rejection_rows(inbox, gpu_universe, provider_universe, region_universe):
    gpu_names = {normalize(value) for value in gpu_universe.get("gpu", [])}
    provider_names = {normalize(value) for value in provider_universe.get("provider", [])}
    region_codes = {normalize(value) for value in region_universe.get("region_code", [])}

    rejected = []
    for _, row in inbox.iterrows():
        blockers = row_blockers(row, gpu_names, provider_names, region_codes)
        if blockers:
            rejected.append({
                **row.to_dict(),
                "rejection_reason": ", ".join(blockers),
            })
    return pd.DataFrame(rejected)


def build_manual_snapshot_ingest(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    inbox_path = data_dir / "manual_market_snapshot_inbox.csv"
    master_path = data_dir / "manual_market_snapshots.csv"
    rejected_path = data_dir / "manual_market_snapshot_rejections.csv"

    inbox = ensure_columns(read_csv(inbox_path)) if inbox_path.exists() else empty_snapshot_frame()
    master = ensure_columns(read_csv(master_path)) if master_path.exists() else empty_snapshot_frame()
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")

    valid_inbox = filter_valid_manual_snapshots(
        inbox,
        gpu_universe,
        provider_universe,
        region_universe,
    )
    rejected = rejection_rows(inbox, gpu_universe, provider_universe, region_universe)

    before_count = len(master)
    combined = pd.concat([master, ensure_columns(valid_inbox)], ignore_index=True)
    duplicate_count = 0
    if not combined.empty:
        duplicate_count = int(combined.duplicated(subset=DEDUP_COLUMNS).sum())
        combined = combined.drop_duplicates(subset=DEDUP_COLUMNS, keep="first")

    combined = ensure_columns(combined)
    data_dir.mkdir(exist_ok=True)
    combined.to_csv(master_path, index=False)
    rejected.to_csv(rejected_path, index=False)

    quality = build_manual_snapshot_quality(data_dir)
    quality.to_csv(data_dir / "manual_snapshot_quality.csv", index=False)
    coverage = build_coverage_universe_status(data_dir)
    coverage.to_csv(data_dir / "coverage_universe_status.csv", index=False)

    imported_count = len(combined) - before_count
    status = "imported" if imported_count > 0 else "nothing_imported"
    if len(inbox) == 0:
        status = "empty_inbox"

    return {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_ingest",
        "status": status,
        "inbox_count": int(len(inbox)),
        "valid_inbox_count": int(len(valid_inbox)),
        "imported_count": int(imported_count),
        "duplicate_count": duplicate_count,
        "rejected_count": int(len(rejected)),
        "master_snapshot_count": int(len(combined)),
        "quality_status": quality.iloc[0]["status"] if not quality.empty else "unknown",
        "coverage_status": coverage.iloc[0]["status"] if not coverage.empty else "unknown",
        "rejections_file": str(rejected_path),
        "next_action": (
            "Add source-labeled rows to data/manual_market_snapshot_inbox.csv."
            if len(inbox) == 0
            else "Review rejected rows and continue collecting source-labeled snapshots."
        ),
    }


def main():
    result = build_manual_snapshot_ingest()
    print(pd.DataFrame([result]))


if __name__ == "__main__":
    main()
