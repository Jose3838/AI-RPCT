import pandas as pd

out = pd.DataFrame([{
    "dashboard_status": "healthy",
    "version": "v3",
    "kpi_cards": True,
    "charts": True,
    "tables": True
}])

out.to_csv("data/dashboard_health.csv", index=False)

print(out)
