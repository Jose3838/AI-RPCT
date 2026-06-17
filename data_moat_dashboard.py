import csv


FILES = [
    "market_snapshot_history.csv",
    "provider_expansion_history.csv",
    "provider_activation_score_history.csv",
    "gpu_scarcity_history.csv",
    "capacity_pressure_history.csv",
    "risk_signal_history.csv",
    "forecast_history.csv"
]


def count_records(file_name):
    try:
        with open(file_name, "r") as file:
            return max(
                len(list(csv.reader(file))) - 1,
                0
            )
    except FileNotFoundError:
        return 0


def build_data_moat_dashboard():

    details = {}

    total = 0

    for file_name in FILES:
        records = count_records(file_name)

        details[file_name] = records

        total += records

    moat_score = min(
        round(total / 25, 2),
        100
    )

    return {
        "status": "ok",
        "version": "v1",
        "total_records": total,
        "data_moat_score": moat_score,
        "datasets": details
    }
