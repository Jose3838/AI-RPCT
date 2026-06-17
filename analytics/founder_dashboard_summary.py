import pandas as pd
from datetime import datetime

customer = pd.read_csv("data/customer_value_score.csv").iloc[-1]
pulse = pd.read_csv("data/ai_infrastructure_pulse.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]
provider_share = pd.read_csv("data/live_provider_market_share.csv")

summary = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "customer_value_score": customer["customer_value_score"],
    "positioning": customer["positioning"],
    "ai_infrastructure_pulse": pulse["ai_infrastructure_pulse"],
    "risk_level": pulse["risk_level"],
    "live_data_quality_score": quality["live_data_quality_score"],
    "providers_tracked": len(provider_share)
}

pd.DataFrame([summary]).to_csv(
    "data/founder_dashboard_summary.csv",
    index=False
)

print(summary)
