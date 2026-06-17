import csv


def count_rows(file_name):
    try:
        with open(file_name, "r") as file:
            return max(
                len(list(csv.reader(file))) - 1,
                0
            )
    except FileNotFoundError:
        return 0


def build_historical_intelligence_score():

    market_rows = count_rows(
        "market_snapshot_history.csv"
    )

    provider_rows = count_rows(
        "provider_expansion_history.csv"
    )

    activation_rows = count_rows(
        "provider_activation_score_history.csv"
    )

    scarcity_rows = count_rows(
        "gpu_scarcity_history.csv"
    )

    total_records = (
        market_rows
        +
        provider_rows
        +
        activation_rows
        +
        scarcity_rows
    )

    score = min(
        round(total_records / 10, 2),
        100
    )

    if score >= 80:
        moat_status = "institutional_data_moat"

    elif score >= 60:
        moat_status = "strong_data_moat"

    elif score >= 40:
        moat_status = "growing_data_moat"

    else:
        moat_status = "early_data_moat"

    return {
        "status": "ok",
        "version": "v1",
        "historical_intelligence_score": score,
        "total_records": total_records,
        "moat_status": moat_status
    }
