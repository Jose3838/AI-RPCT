from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from collectors.providers.live_registry import get_configured_providers
from collectors.providers.loader import load_provider
from integrations.provider_schema import validate_provider_rows
from collectors.providers.normalizer import normalize_provider_rows

rows = []

for provider_config in get_configured_providers():
    provider = load_provider(provider_config)

    try:
        provider_rows = provider.fetch()
        provider_rows = normalize_provider_rows(provider_rows)

        errors = validate_provider_rows(provider_rows)

        if errors:
            print(f"Schema errors for {provider.name}: {errors}")
            continue

        rows.extend(provider_rows)

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

final_data["price_per_hour"] = pd.to_numeric(
    final_data["price_per_hour"],
    errors="coerce",
).fillna(0.0)

final_data["availability"] = pd.to_numeric(
    final_data["availability"],
    errors="coerce",
).fillna(0).astype(int)

final_data.to_csv(file_path, index=False)

print("GPU data saved to data/gpu_data.csv")
print(new_data)
