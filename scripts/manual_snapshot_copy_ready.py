import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.manual_snapshot_ingest import DEDUP_COLUMNS, empty_snapshot_frame, ensure_columns, rejection_rows
from analytics.manual_snapshot_quality import filter_valid_manual_snapshots, read_csv


DATA_DIR = Path("data")


def build_manual_snapshot_copy_ready(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    template_path = data_dir / "manual_market_snapshot_inbox_template.csv"
    inbox_path = data_dir / "manual_market_snapshot_inbox.csv"
    template_rejections_path = data_dir / "manual_market_snapshot_template_rejections.csv"

    template = ensure_columns(read_csv(template_path)) if template_path.exists() else empty_snapshot_frame()
    inbox = ensure_columns(read_csv(inbox_path)) if inbox_path.exists() else empty_snapshot_frame()
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")

    valid = ensure_columns(filter_valid_manual_snapshots(
        template,
        gpu_universe,
        provider_universe,
        region_universe,
    ))
    rejected = rejection_rows(template, gpu_universe, provider_universe, region_universe)

    before_count = len(inbox)
    combined = ensure_columns(pd.concat([inbox, valid], ignore_index=True))
    duplicate_count = 0
    if not combined.empty:
        duplicate_count = int(combined.duplicated(subset=DEDUP_COLUMNS).sum())
        combined = combined.drop_duplicates(subset=DEDUP_COLUMNS, keep="first")

    data_dir.mkdir(exist_ok=True)
    combined.to_csv(inbox_path, index=False)
    rejected.to_csv(template_rejections_path, index=False)

    copied_count = max(0, len(combined) - before_count)
    if template.empty:
        status = "template_missing_or_empty"
        next_action = "Run venv/bin/python scripts/manual_snapshot_inbox_template.py."
    elif copied_count > 0 and len(rejected) > 0:
        status = "partially_copied"
        next_action = "Run venv/bin/python analytics/manual_snapshot_ingest.py, then fix rejected template rows."
    elif copied_count > 0:
        status = "copied"
        next_action = "Run venv/bin/python analytics/manual_snapshot_ingest.py."
    elif len(valid) > 0:
        status = "no_new_rows"
        next_action = "Rows are already in the inbox. Run venv/bin/python analytics/manual_snapshot_ingest.py."
    else:
        status = "no_valid_template_rows"
        next_action = "Fill price_per_hour, availability, delivery_time_days and source_url with public source evidence."

    return {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_copy_ready",
        "status": status,
        "template_file": str(template_path),
        "inbox_file": str(inbox_path),
        "template_row_count": int(len(template)),
        "valid_template_row_count": int(len(valid)),
        "copied_count": int(copied_count),
        "duplicate_count": duplicate_count,
        "rejected_template_row_count": int(len(rejected)),
        "template_rejections_file": str(template_rejections_path),
        "next_action": next_action,
    }


def main():
    print(json.dumps(build_manual_snapshot_copy_ready(), indent=2))


if __name__ == "__main__":
    main()
