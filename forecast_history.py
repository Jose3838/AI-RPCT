import csv

from forecast_engine_v3 import build_forecast_engine_v3
from timestamp_utils import utc_timestamp


FILE_NAME = "forecast_history.csv"


def save_forecast_snapshot():
    forecast = build_forecast_engine_v3()
    timestamp = utc_timestamp()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            forecast["forecast_score"],
            forecast["forecast_signal"],
            forecast["risk_level"],
            forecast["data_trust"]
        ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "forecast": forecast
    }


def load_forecast_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
