import pandas as pd
from datetime import datetime
from pathlib import Path

score = 50
drivers = []

market = pd.read_csv("data/market_data.csv")
gpu = pd.read_csv("data/gpu_data.csv")

latest_market = market.groupby("asset").last()
latest_gpu = gpu.groupby("gpu").last()

def add_driver(condition, points, label):
    global score
    if condition:
        score += points
        drivers.append(label)

# Market stress / AI infrastructure sentiment
add_driver(latest_market.loc["NVDA", "price"] > 200, 12, "NVDA above 200")
add_driver(latest_market.loc["BTC", "price"] > 60000, 8, "BTC above 60k")
add_driver(latest_market.loc["ETH", "price"] > 1800, 6, "ETH above 1800")
add_driver(latest_market.loc["AKT", "price"] > 0.75, 8, "AKT above 0.75")

# GPU stress placeholders
add_driver(latest_gpu.loc["H100", "price_per_hour"] > 2.0, 10, "H100 price above $2/hr")
add_driver(latest_gpu.loc["A100", "price_per_hour"] > 1.0, 6, "A100 price above $1/hr")
add_driver(latest_gpu.loc["H100", "availability"] < 1200, 10, "H100 availability constrained")
add_driver(latest_gpu.loc["A100", "availability"] < 3000, 6, "A100 availability constrained")

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

print("\nAI-RPCT v0.5")
print("============")
print(f"Score: {score}")
print(f"Regime: {regime}")
print(f"Drivers: {', '.join(drivers) if drivers else 'No major stress drivers'}")
print("\nSaved to data/rpct_scores.csv")
