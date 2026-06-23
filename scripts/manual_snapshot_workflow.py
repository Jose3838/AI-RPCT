import json
from datetime import date
from pathlib import Path

import pandas as pd

from analytics.snapshot_collection_plan import build_snapshot_collection_plan


DATA_DIR = Path("data")
INBOX_PATH = DATA_DIR / "manual_market_snapshot_inbox.csv"


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def priority_values(frame, column, limit=8):
    if frame.empty or column not in frame:
        return []
    if "tracking_priority" in frame:
        frame = frame.sort_values(["tracking_priority", column], ascending=[True, True])
    return [str(value) for value in frame[column].dropna().head(limit)]


def build_manual_snapshot_workflow(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")
    collection_plan = build_snapshot_collection_plan(data_dir, limit=10)

    return {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_workflow",
        "inbox_path": str(data_dir / "manual_market_snapshot_inbox.csv"),
        "master_path": str(data_dir / "manual_market_snapshots.csv"),
        "rejections_path": str(data_dir / "manual_market_snapshot_rejections.csv"),
        "required_columns": [
            "snapshot_date",
            "provider",
            "gpu",
            "region_code",
            "price_per_hour",
            "availability",
            "delivery_time_days",
            "source_url",
            "source_type",
            "claim_scope",
            "notes",
        ],
        "fixed_values": {
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
        },
        "priority_collection": {
            "gpus": priority_values(gpu_universe, "gpu"),
            "providers": priority_values(provider_universe, "provider"),
            "regions": priority_values(region_universe, "region_code"),
        },
        "next_snapshot_targets": collection_plan.to_dict(orient="records"),
        "example_row": {
            "snapshot_date": date.today().isoformat(),
            "provider": "vast",
            "gpu": "H100 SXM",
            "region_code": "us-east",
            "price_per_hour": 0.0,
            "availability": 0,
            "delivery_time_days": 0,
            "source_url": "https://example.com/source-page",
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "notes": "Replace example values with public source evidence.",
        },
        "daily_commands": [
            "venv/bin/python scripts/manual_snapshot_inbox_template.py",
            "venv/bin/python scripts/manual_snapshot_template_check.py",
            "venv/bin/python analytics/manual_snapshot_ingest.py",
            "venv/bin/python analytics/manual_snapshot_quality.py",
            "venv/bin/python analytics/coverage_universe_status.py",
            "venv/bin/python scripts/core_status.py",
        ],
        "rules": [
            "Do not invent historical rows.",
            "Use only public source pages or source-backed manual observations.",
            "Keep claim_scope=research_preview until paid data gates are green.",
            "Leave unknown values out rather than guessing.",
        ],
    }


def main():
    print(json.dumps(build_manual_snapshot_workflow(), indent=2))


if __name__ == "__main__":
    main()
