import csv


FILE_NAME = "market_snapshot_history.csv"


def load_history():
    try:
        with open(FILE_NAME, "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def get_window(records):
    history = load_history()

    if not history:
        return {
            "status": "no_data"
        }

    window = history[-records:]

    return {
        "status": "ok",
        "records": len(window),
        "data": window
    }


def get_7_day_window():
    return get_window(7)


def get_30_day_window():
    return get_window(30)


def get_90_day_window():
    return get_window(90)
