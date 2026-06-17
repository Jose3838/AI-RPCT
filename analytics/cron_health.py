from pathlib import Path
from datetime import datetime
import pandas as pd

checks = {
    "cron_log_exists": Path("logs/cron.log").exists(),
    "manual_log_exists": Path("logs/manual_run.log").exists(),
    "snapshots_exist": Path("warehouse/snapshots").exists() and any(Path("warehouse/snapshots").iterdir()),
    "provider_history_exists": Path("data/provider_daily_metrics.csv").exists(),
    "index_history_exists": Path("data/index_history.csv").exists()
}

status = "healthy" if all(checks.values()) else "needs_attention"

out = pd.DataFrame([{
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": status,
    **checks
}])

out.to_csv("data/cron_health.csv", index=False)

print(out)
