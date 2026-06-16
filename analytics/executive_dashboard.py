import pandas as pd

files = [
    "data/provider_rankings.csv",
    "data/shortage_probability.csv",
    "data/investor_metrics.csv"
]

summary = []

for file in files:
    try:
        df = pd.read_csv(file)
        summary.append({
            "file": file,
            "rows": len(df)
        })
    except:
        pass

pd.DataFrame(summary).to_csv(
    "data/executive_dashboard.csv",
    index=False
)
