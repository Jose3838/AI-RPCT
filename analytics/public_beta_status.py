import pandas as pd
from pathlib import Path

provider_mode = "unknown"

if Path("data/provider_data_mode.csv").exists():
    provider_mode = pd.read_csv("data/provider_data_mode.csv").iloc[-1]["provider_data_mode"]

status = "technical_preview"

if provider_mode == "live":
    status = "public_beta_candidate"

out = pd.DataFrame([{
    "release_stage": status,
    "provider_data_mode": provider_mode,
    "paid_customers_allowed": False,
    "public_demo_allowed": True
}])

out.to_csv("data/public_beta_status.csv", index=False)

print(out)
