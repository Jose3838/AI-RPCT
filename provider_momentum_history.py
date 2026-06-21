import csv

from provider_momentum import build_provider_momentum
from timestamp_utils import utc_timestamp


FILE_NAME = "provider_momentum_history.csv"


def save_provider_momentum_snapshot():
    momentum = build_provider_momentum()
    timestamp = utc_timestamp()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        for item in momentum["momentum"]:
            writer.writerow([
                timestamp,
                item["provider"],
                item["market_share_estimate"],
                item["momentum_signal"]
            ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "records_saved": len(momentum["momentum"])
    }


def load_provider_momentum_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
