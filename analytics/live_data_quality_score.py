from pathlib import Path
import pandas as pd

checks = {
    "vast_live_data": Path("data/live_provider_data.csv").exists(),
    "runpod_live_data": Path("data/runpod_live_report.csv").exists(),
    "provider_health": Path("data/provider_health.csv").exists(),
    "gpu_price_history": Path("data/live_gpu_price_history.csv").exists(),
    "warehouse_metrics": Path("data/warehouse_metrics.csv").exists(),
    "weekly_report": any(Path("reports").glob("weekly_infrastructure_report_*.txt")) if Path("reports").exists() else False
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "live_data_quality_score": score,
    **checks
}])

out.to_csv("data/live_data_quality_score.csv", index=False)

print(out)
