import csv

from gpu_scarcity_index import build_gpu_scarcity_index
from timestamp_utils import utc_timestamp


FILE_NAME = "gpu_scarcity_history.csv"


def save_gpu_scarcity_snapshot():
    scarcity = build_gpu_scarcity_index()
    timestamp = utc_timestamp()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            scarcity["gpu_scarcity_index"],
            scarcity["scarcity_status"],
            scarcity["average_capacity"],
            scarcity["provider_count"]
        ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "scarcity": scarcity
    }


def load_gpu_scarcity_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
