import pandas as pd

gpu = pd.read_csv("data/gpu_data.csv")

avg_price = gpu["price_per_hour"].mean()
avg_availability = gpu["availability"].mean()

scarcity_score = 0

if avg_price > 2:
    scarcity_score += 40
elif avg_price > 1:
    scarcity_score += 20

if avg_availability < 1000:
    scarcity_score += 40
elif avg_availability < 2500:
    scarcity_score += 20

scarcity_score = min(scarcity_score, 100)

result = pd.DataFrame([{
    "gpu_scarcity_index": scarcity_score,
    "avg_price_per_hour": round(avg_price, 4),
    "avg_availability": round(avg_availability, 2)
}])

result.to_csv("data/gpu_scarcity_index.csv", index=False)

print(result)
