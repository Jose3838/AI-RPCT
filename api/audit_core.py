from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


AUDIT_FILE = Path("data/audit_log.csv")
AUDIT_COLUMNS = [
    "timestamp",
    "actor_api_key",
    "action",
    "target_api_key",
    "target_account_id",
    "status",
]


def read_audit_records():
    if not AUDIT_FILE.exists() or AUDIT_FILE.stat().st_size <= 1:
        return []
    return pd.read_csv(AUDIT_FILE, on_bad_lines="skip").to_dict(orient="records")


def log_audit_event(actor_api_key, action, target_api_key="", target_account_id="", status="ok"):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = pd.DataFrame(read_audit_records(), columns=AUDIT_COLUMNS)
    row = pd.DataFrame([{
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_api_key": actor_api_key,
        "action": action,
        "target_api_key": target_api_key,
        "target_account_id": target_account_id,
        "status": status,
    }])
    pd.concat([existing, row], ignore_index=True).to_csv(AUDIT_FILE, index=False)


def build_audit_log(limit=100):
    records = read_audit_records()
    records = records[-int(limit):] if records else []
    action_counts = {}

    for record in records:
        action = record.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "audit_log",
        "summary": {
            "events": len(records),
            "action_counts": action_counts,
        },
        "events": list(reversed(records)),
    }
