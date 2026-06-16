from pathlib import Path

required = [
    "data/provider_rankings.csv",
    "data/provider_marketshare.csv",
    "data/data_quality.csv"
]

for file in required:
    print(file, "OK" if Path(file).exists() else "MISSING")
