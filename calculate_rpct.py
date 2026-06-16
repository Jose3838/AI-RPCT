import pandas as pd
from datetime import datetime
from pathlib import Path

score = 50
drivers = []

# Market data
market = pd.read_csv("data/market_data.csv")

for asset in ["NVDA", "BTC", "ETH", "AKT"]:
    asset_df = market[market["asset"] == asset].copy()

    if len(asset_df) < 2:
        continue

    current = asset_df.iloc[-1]["price"]
    previous = asset_df.iloc[-2]["price"]
    change_pct = ((current - previous) / previous) * 100

    if change_pct > 1:
        score += 7
        drivers.append(f"{asset} momentum +{change_pct:.2f}%")
    elif change_pct < -1:
        score -= 7
        drivers.append(f"{asset} momentum {change_pct:.2f}%")

# GPU data
gpu = pd.read_csv("data/gpu_data.csv")

for gpu_name in ["H100", "A100"]:
    gpu_df = gpu[gpu["gpu"] == gpu_name].copy()

    if len(gpu_df) < 2:
        continue

    current_price = gpu_df.iloc[-1]["price_per_hour"]
    previous_price = gpu_df.iloc[-2]["price_per_hour"]

    current_avail = gpu_df.iloc[-1]["availability"]
    previous_avail = gpu_df.iloc[-2]["availability"]

    price_change = ((current_price - previous_price) / previous_price) * 100
    availability_change = ((current_avail - previous_avail) / previous_avail) * 100

    if price_change > 2:
        score += 10
        drivers.append(f"{gpu_name} price stress +{price_change:.2f}%")

    if availability_change < -5:
        score += 10
        drivers.append(f"{gpu_name} availability down {availability_change:.2f}%")

score = max(0, min(score, 100))

if score < 40:
    regime = "Stable"
elif score < 60:
    regime = "Watch"
elif score < 80:
    regime = "Stress"
else:
    regime = "Critical"

row = pd.DataFrame([{
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "score": score,
    "regime": regime,
    "drivers": ", ".join(drivers) if drivers else "No major stress drivers"
}])

file_path = "data/rpct_scores.csv"

if Path(file_path).exists():
    old = pd.read_csv(file_path)
    out = pd.concat([old, row], ignore_index=True)
else:
    out = row

out.to_csv(file_path, index=False)

print("\nAI-RPCT")
print("========")
print(f"Score: {score}")
print(f"Regime: {regime}")
print(f"Drivers: {', '.join(drivers) if drivers else 'No major stress drivers'}")
print("\nSaved to data/rpct_scores.csv")
