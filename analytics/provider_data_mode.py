import pandas as pd
from pathlib import Path

live_status = pd.read_csv("data/live_provider_status.csv")

live_count = live_status["configured"].sum()

mode = "live" if live_count > 0 else "placeholder"

out = pd.DataFrame([{
    "provider_data_mode": mode,
    "live_providers_configured": int(live_count)
}])

out.to_csv("data/provider_data_mode.csv", index=False)

print(out)
