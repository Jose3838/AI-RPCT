import pandas as pd
from pathlib import Path
from datetime import datetime

from collectors.providers.manual import ManualProvider
from collectors.providers.runpod import RunPodProvider
from collectors.providers.vast import VastProvider

providers = [
    ManualProvider(),
    RunPodProvider(),
    VastProvider()
]

rows = []

for provider in providers:
    try:
        rows.extend(provider.fetch())
    except Exception as e:
        print(f"Provider failed: {provider.name} | {e}")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for row in rows:
    row["timestamp"] = timestamp

Path("data").mkdir(exist_ok=True)

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
