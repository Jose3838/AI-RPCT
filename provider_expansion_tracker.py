import csv

from provider_coverage_engine_v3 import get_provider_coverage_v3
from timestamp_utils import utc_timestamp


FILE_NAME = "provider_expansion_history.csv"


def save_provider_expansion():
    timestamp = utc_timestamp()
    coverage = get_provider_coverage_v3()

    with open(
        FILE_NAME,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            coverage["live_providers"],
            coverage["total_target_providers"],
            coverage["coverage_percentage"]
        ])

    return {
        "status": "saved",
        "timestamp": timestamp,
        "coverage": coverage
    }
