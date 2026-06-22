import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def build_history_backfill_plan():
    audit = read_latest(DATA_DIR / "core_history_audit.csv")
    missing = [
        item.strip()
        for item in str(audit.get("missing_recent_days", "")).split(",")
        if item.strip() and item.strip() != "none"
    ]

    return {
        "product": "AI-RPCT",
        "policy": "do_not_fake_history",
        "days_collected": audit.get("days_collected", 0),
        "days_remaining": audit.get("days_remaining", 30),
        "progress_pct": audit.get("progress_pct", 0),
        "missing_recent_days": missing,
        "recommended_action": "Run the core intelligence pipeline daily with real provider inputs; do not synthesize missing history for paid claims.",
        "allowed_backfill": "Only import externally verifiable historical provider observations with source provenance.",
    }


def main():
    print(json.dumps(build_history_backfill_plan(), indent=2, default=str))


if __name__ == "__main__":
    main()
