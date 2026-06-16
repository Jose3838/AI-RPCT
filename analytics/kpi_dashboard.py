import pandas as pd

kpis = {
    "providers": len(pd.read_csv("data/provider_rankings.csv")),
    "market_share_entries": len(pd.read_csv("data/provider_marketshare.csv")),
    "alerts": len(pd.read_csv("data/alerts.csv")),
    "data_quality": pd.read_csv("data/data_quality.csv")["data_quality_score"].iloc[0]
}

pd.DataFrame([kpis]).to_csv(
    "data/kpi_dashboard.csv",
    index=False
)

print(kpis)
