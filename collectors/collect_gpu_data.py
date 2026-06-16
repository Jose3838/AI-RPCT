import pandas as pd
from datetime import datetime
from pathlib import Path

Path("data").mkdir(exist_ok=True)

rows = [
    {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": "manual",
        "gpu": "H100",
        "price_per_hour": 2.15,
        "availability": 1000
    },
    {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": "manual",
        "gpu": "A100",
        "price_per_hour": 1.05,
        "availability": 2500
    }
]

new_data = pd.DataFrame(rows)
file_path = "data/gpu_data.csv"

if Path(file_path).exists():
    old_data = pd.read_csv(file_path)
    final_data = pd.concat([old_data, new_data], ignore_index=True)
else:
    final_data = new_data

final_data.to_csv(file_path, index=False)

print("GPU data saved to data/gpu_data.csv")
print(new_data)
