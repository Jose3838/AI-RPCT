import pandas as pd
from pathlib import Path

live_file = Path("data/live_provider_data.csv")

live_count = 0

if live_file.exists():
    try:
        live_count = len(pd.read_csv(live_file))
    except:
        live_count = 0

mode = "live" if live_count > 0 else "placeholder"

out = pd.DataFrame([{
    "provider_data_mode": mode,
    "live_providers_configured": 1 if live_count > 0 else 0,
    "live_provider_rows": live_count
}])

out.to_csv(
    "data/provider_data_mode.csv",
    index=False
)

print(out)
