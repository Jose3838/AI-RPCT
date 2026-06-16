import pandas as pd
from pathlib import Path

checks = {
    "api": Path("main.py").exists(),
    "dashboard": Path("dashboard.html").exists(),
    "database": Path("data/airpct.db").exists(),
    "logs": Path("data/system.log").exists(),
    "pipeline": Path("run_daily.sh").exists()
}

status = "operational" if all(checks.values()) else "degraded"

pd.DataFrame([{
    "status": status,
    **checks
}]).to_csv("data/operational_status.csv", index=False)

print(status)
