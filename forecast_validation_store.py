import csv


def load_forecasts():
    try:
        with open("forecast_history.csv", "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def load_market_history():
    try:
        with open("market_snapshot_history.csv", "r") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
