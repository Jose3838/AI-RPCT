import pandas as pd
from datetime import datetime

offers = pd.read_csv("data/live_offer_summary.csv")

top_expensive = offers.sort_values(
    "avg_price",
    ascending=False
).head(3)

top_available = offers.sort_values(
    "offers",
    ascending=False
).head(3)

brief = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "most_expensive_gpu": top_expensive.iloc[0]["gpu"],
    "highest_avg_price": round(top_expensive.iloc[0]["avg_price"], 2),
    "most_available_gpu": top_available.iloc[0]["gpu"],
    "highest_offer_count": int(top_available.iloc[0]["offers"])
}

pd.DataFrame([brief]).to_csv(
    "data/gpu_market_brief.csv",
    index=False
)

print(brief)
