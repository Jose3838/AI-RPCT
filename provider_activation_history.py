import csv
from datetime import datetime


HISTORY_FILE = "provider_activation_score_history.csv"


def append_activation_score(
    provider,
    activation_score
):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")

    with open(
        HISTORY_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            provider,
            activation_score
        ])

    return {
        "status": "saved",
        "provider": provider,
        "score": activation_score
    }
