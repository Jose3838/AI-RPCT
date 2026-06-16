import pandas as pd
from pathlib import Path
from datetime import datetime

from providers.runpod import get_gpu_data as runpod_data
from providers.vast import get_gpu_data as vast_data


def collect_all_gpu_data():
    data = []

    data.extend(runpod_data())
    data.extend(vast_data())

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for row in data:
        row["timestamp"] = timestamp

    return data


if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)

    new_data = pd.DataFrame(collect_all_gpu_data())
    file_path = "data/gpu_data.csv"

    if Path(file_path).exists():
        old_data = pd.read_csv(file_path)
        final_data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        final_data = new_data

    final_data.to_csv(file_path, index=False)

    print("GPU data saved to data/gpu_data.csv")
    print(new_data)
