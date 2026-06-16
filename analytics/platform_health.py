from pathlib import Path

checks = [
    "data/provider_rankings.csv",
    "data/provider_marketshare.csv",
    "data/data_quality.csv",
    "data/alerts.csv"
]

ok = 0

for item in checks:
    if Path(item).exists():
        ok += 1

print(
    f"Platform health: {ok}/{len(checks)}"
)
