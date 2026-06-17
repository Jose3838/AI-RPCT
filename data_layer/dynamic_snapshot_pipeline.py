import csv

from provider_coverage_engine_v3 import get_provider_coverage_v3
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores
from data_layer.market_strength_pipeline import build_dynamic_market_strength_index
from timestamp_utils import utc_timestamp


SNAPSHOT_FILE = "market_snapshot_history.csv"


def save_dynamic_market_snapshot():
    timestamp = utc_timestamp()

    coverage_data = get_provider_coverage_v3()
    provider_scores = build_dynamic_provider_activation_scores()
    market_strength_data = build_dynamic_market_strength_index()

    activation_scores = [
        item["activation_score"]
        for item in provider_scores
    ]

    avg_activation_score = round(
        sum(activation_scores) / len(activation_scores),
        2
    ) if activation_scores else 0

    with open(
        SNAPSHOT_FILE,
        "a",
        newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            coverage_data["coverage_percentage"],
            market_strength_data["market_strength_index"],
            avg_activation_score
        ])

    return {
        "status": "saved",
        "version": "v2",
        "timestamp": timestamp,
        "coverage_percentage": coverage_data["coverage_percentage"],
        "market_strength_index": market_strength_data["market_strength_index"],
        "avg_activation_score": avg_activation_score
    }
