import csv
from datetime import datetime


SNAPSHOT_FILE = "market_snapshot_history.csv"


def save_market_snapshot(
    coverage,
    market_strength,
    avg_activation_score
):
    date = datetime.utcnow().strftime("%Y-%m-%d")

    with open(
        SNAPSHOT_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            date,
            coverage,
            market_strength,
            avg_activation_score
        ])

    return {
        "status": "saved",
        "date": date
    }
