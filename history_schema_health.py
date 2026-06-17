FILES = [
    "market_snapshot_history.csv",
    "provider_expansion_history.csv",
    "gpu_scarcity_history.csv",
    "capacity_pressure_history.csv",
    "risk_signal_history.csv",
    "forecast_history.csv"
]


def build_history_schema_health():
    results = []

    for file_name in FILES:
        try:
            with open(file_name, "r") as file:
                header = file.readline().strip()
        except FileNotFoundError:
            results.append({
                "file": file_name,
                "status": "missing"
            })
            continue

        results.append({
            "file": file_name,
            "header": header,
            "timestamp_ready": header.startswith("timestamp,")
        })

    return {
        "status": "ok",
        "version": "v1",
        "files": results
    }
