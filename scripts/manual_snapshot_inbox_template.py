import json
import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from analytics.snapshot_collection_plan import build_snapshot_collection_plan


DATA_DIR = Path("data")
TEMPLATE_FILE = DATA_DIR / "manual_market_snapshot_inbox_template.csv"


def build_manual_snapshot_inbox_template(data_dir=DATA_DIR, limit=10):
    data_dir = Path(data_dir)
    plan = build_snapshot_collection_plan(data_dir, limit=limit)
    rows = []
    for _, target in plan.iterrows():
        rows.append({
            "snapshot_date": date.today().isoformat(),
            "provider": target.get("provider"),
            "gpu": target.get("gpu"),
            "region_code": target.get("region_code"),
            "price_per_hour": "",
            "availability": "",
            "delivery_time_days": "",
            "source_url": "",
            "source_type": "manual_public_snapshot",
            "claim_scope": "research_preview",
            "notes": "Fill price, availability, delivery_time_days and source_url before copying to inbox.",
        })
    return pd.DataFrame(rows)


def save_manual_snapshot_inbox_template(data_dir=DATA_DIR, limit=10):
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)
    template = build_manual_snapshot_inbox_template(data_dir, limit=limit)
    path = data_dir / "manual_market_snapshot_inbox_template.csv"
    template.to_csv(path, index=False)
    return {
        "product": "AI-RPCT",
        "report_type": "manual_snapshot_inbox_template",
        "status": "saved",
        "file": str(path),
        "row_count": int(len(template)),
        "claim_scope": "research_preview",
        "next_action": "Fill source-backed values, then copy completed rows to data/manual_market_snapshot_inbox.csv.",
    }


def main():
    print(json.dumps(save_manual_snapshot_inbox_template(), indent=2))


if __name__ == "__main__":
    main()
