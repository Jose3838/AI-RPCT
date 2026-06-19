import csv
import os
from datetime import datetime, timezone

HISTORY_FILE = "data/live_offers/provider_live_offer_history.csv"

FIELDS = [
    "observed_at",
    "provider",
    "gpu_model",
    "region",
    "price_usd_per_gpu_hour",
    "available",
    "source",
    "mode",
    "fingerprint",
]

def append_live_offer_history(provider_results):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    exists = os.path.exists(HISTORY_FILE)

    rows = []
    for result in provider_results:
        for offer in result.get("offers", []):
            rows.append({k: offer.get(k) for k in FIELDS})

    if not rows:
        return {"written": 0, "file": HISTORY_FILE}

    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)

    return {"written": len(rows), "file": HISTORY_FILE}
