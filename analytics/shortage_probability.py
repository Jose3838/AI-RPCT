import pandas as pd

gpu = pd.read_csv("data/gpu_data.csv")

avg_price = gpu["price_per_hour"].mean()
avg_availability = gpu["availability"].mean()

probability = 0

if avg_price > 2:
    probability += 40

if avg_availability < 1500:
    probability += 40

probability = min(probability, 100)

result = pd.DataFrame([{
    "shortage_probability": probability,
    "avg_price": avg_price,
    "avg_availability": avg_availability
}])

result.to_csv(
    "data/shortage_probability.csv",
    index=False
)

print(result)
