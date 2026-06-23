import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.manual_snapshot_ingest import ensure_columns, rejection_rows
from analytics.manual_snapshot_quality import (
    filter_valid_manual_snapshots,
    read_csv,
)


DATA_DIR = Path("data")
TEMPLATE_FILE = DATA_DIR / "manual_market_snapshot_inbox_template.csv"


def build_manual_snapshot_template_check(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    template_path = data_dir / "manual_market_snapshot_inbox_template.csv"
    template = ensure_columns(read_csv(template_path)) if template_path.exists() else pd.DataFrame()
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")

    valid = filter_valid_manual_snapshots(
        template,
        gpu_universe,
        provider_universe,
        region_universe,
    )
    rejected = rejection_rows(template, gpu_universe, provider_universe, region_universe)

    if template.empty:
        status = "template_missing_or_empty"
        next_action = "Run venv/bin/python scripts/manual_snapshot_inbox_template.py."
    elif len(valid) == len(template):
        status = "ready_to_copy"
        next_action = "Copy completed template rows to data/manual_market_snapshot_inbox.csv, then run analytics/manual_snapshot_ingest.py."
    elif len(valid) == 0:
        status = "template_needs_sources"
        next_action = "Fill price_per_hour, availability, delivery_time_days and source_url with public source evidence."
    else:
        status = "template_partially_ready"
        next_action = "Copy only valid rows or fix rejected rows before ingest."

    return {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_template_check",
        "status": status,
        "template_file": str(template_path),
        "template_row_count": int(len(template)),
        "valid_row_count": int(len(valid)),
        "rejected_row_count": int(len(rejected)),
        "claim_scope": "research_preview",
        "top_rejection_reasons": (
            rejected["rejection_reason"].head(5).to_list()
            if not rejected.empty and "rejection_reason" in rejected
            else []
        ),
        "next_action": next_action,
    }


def main():
    print(json.dumps(build_manual_snapshot_template_check(), indent=2))


if __name__ == "__main__":
    main()
