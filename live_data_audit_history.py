import csv

from live_data_snapshot_auditor import build_live_data_snapshot_audit


FILE_NAME = "live_data_audit_history.csv"


def save_live_data_audit_snapshot():
    audit = build_live_data_snapshot_audit()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            audit["timestamp"],
            audit["live_connectors"],
            audit["fallback_connectors"],
            audit["demo_connectors"]
        ])

    return {
        "status": "saved",
        "audit": audit
    }


def load_live_data_audit_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
