import pandas as pd
from pathlib import Path

checks = {
    "vast_live_data": Path("data/live_provider_data.csv").exists(),
    "runpod_live_data": Path("data/runpod_live_report.csv").exists(),
    "gpu_price_history": Path("data/live_gpu_price_history.csv").exists(),
    "provider_health": Path("data/provider_health.csv").exists(),
    "gpu_rankings": Path("data/live_gpu_most_expensive.csv").exists(),
    "weekly_report": any(Path("reports").glob("weekly_infrastructure_report_*.txt")) if Path("reports").exists() else False
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "market_data_moat_score": score,
    **checks
}])

out.to_csv("data/market_data_moat_status.csv", index=False)

print(out)
