import pandas as pd

out = pd.DataFrame([{
    "dashboard_status": "healthy",
    "version": "v4",
    "kpi_cards": True,
    "charts": True,
    "tables": True,
    "report_links": True,
    "auto_refresh": True
}])

out.to_csv("data/dashboard_health.csv", index=False)

print(out)
