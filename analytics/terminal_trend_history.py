import pandas as pd
from pathlib import Path
from datetime import datetime

rows = []

def add_metric(name, file, column):
    if Path(file).exists():
        df = pd.read_csv(file)
        if not df.empty and column in df.columns:
            rows.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "metric": name,
                "value": df.iloc[-1][column]
            })

add_metric("ai_infrastructure_index", "data/ai_infrastructure_index.csv", "ai_infrastructure_index")
add_metric("gpu_price_index", "data/live_gpu_price_index.csv", "gpu_price_index")
add_metric("terminal_risk_score", "data/terminal_risk_score.csv", "terminal_risk_score")
add_metric("live_data_quality_score", "data/live_data_quality_score.csv", "live_data_quality_score")

out = pd.DataFrame(rows)

history_file = "data/terminal_trend_history.csv"

if Path(history_file).exists():
    old = pd.read_csv(history_file)
    out = pd.concat([old, out], ignore_index=True)

out.to_csv(history_file, index=False)

print(out.tail())
