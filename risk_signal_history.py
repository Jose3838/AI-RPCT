import csv

from infrastructure_risk_signal import build_infrastructure_risk_signal
from timestamp_utils import utc_timestamp


FILE_NAME = "risk_signal_history.csv"


def save_risk_signal_snapshot():
    risk = build_infrastructure_risk_signal()
    timestamp = utc_timestamp()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            risk["risk_level"],
            risk["capacity_pressure_index"],
            risk["forecast_signal"],
            risk["data_trust_index"]
        ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "risk": risk
    }


def load_risk_signal_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
