import csv


def read_csv_file(file_name):
    try:
        with open(file_name, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def get_historical_data():
    return {
        "status": "ok",
        "version": "v1",
        "market_snapshots": read_csv_file("market_snapshot_history.csv"),
        "provider_expansion": read_csv_file("provider_expansion_history.csv"),
        "provider_activation_scores": read_csv_file("provider_activation_score_history.csv")
    }
