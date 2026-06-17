import pandas as pd
from pathlib import Path

alerts = []

# Price movement alert
if Path("data/gpu_market_movers.csv").exists():
    movers = pd.read_csv("data/gpu_market_movers.csv").iloc[-1]

    if abs(float(movers["change_pct"])) >= 5:
        alerts.append({
            "type": "price_move",
            "severity": "high",
            "message": f"GPU price index moved {movers['change_pct']}%"
        })

# Scarcity alert
if Path("data/gpu_scarcity_index.csv").exists():
    scarcity = pd.read_csv("data/gpu_scarcity_index.csv").iloc[-1]

    if float(scarcity["gpu_scarcity_index"]) >= 60:
        alerts.append({
            "type": "scarcity",
            "severity": "high",
            "message": f"GPU scarcity index elevated: {scarcity['gpu_scarcity_index']}"
        })

# Provider mode alert
if Path("data/provider_data_mode.csv").exists():
    mode = pd.read_csv("data/provider_data_mode.csv").iloc[-1]

    if mode["provider_data_mode"] != "live":
        alerts.append({
            "type": "provider_data",
            "severity": "medium",
            "message": "Provider data is not live"
        })

df = pd.DataFrame(alerts)

if df.empty:
    df = pd.DataFrame([{
        "type": "none",
        "severity": "low",
        "message": "No live GPU alerts"
    }])

df.to_csv("data/live_gpu_alerts.csv", index=False)

print(df)
