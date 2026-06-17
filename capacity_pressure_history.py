import csv

from capacity_pressure_index import build_capacity_pressure_index
from timestamp_utils import utc_timestamp


FILE_NAME = "capacity_pressure_history.csv"


def save_capacity_pressure_snapshot():
    pressure = build_capacity_pressure_index()
    timestamp = utc_timestamp()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            pressure["capacity_pressure_index"],
            pressure["pressure_status"],
            pressure["scarcity_index"],
            pressure["market_strength_index"],
            pressure["average_activation_score"]
        ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "pressure": pressure
    }


def load_capacity_pressure_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
