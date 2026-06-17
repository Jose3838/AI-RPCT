import pandas as pd

out = pd.DataFrame([{
    "dashboard_status": "healthy",
    "version": "v2",
    "charts": True
}])

out.to_csv("data/dashboard_health.csv", index=False)

print(out)
