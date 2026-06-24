from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

snapshots = read_csv(DATA_DIR / "manual_market_snapshots.csv")
gpus = read_csv(DATA_DIR / "gpu_universe.csv")
providers = read_csv(DATA_DIR / "provider_universe.csv")
regions = read_csv(DATA_DIR / "region_universe.csv")

covered_gpus = set(snapshots.get("gpu", pd.Series(dtype=str)).dropna().astype(str))
covered_providers = set(snapshots.get("provider", pd.Series(dtype=str)).dropna().astype(str))
covered_regions = set(snapshots.get("region_code", pd.Series(dtype=str)).dropna().astype(str))

rows = []

for _, row in gpus.iterrows():
    if row["gpu"] not in covered_gpus:
        rows.append({
            "gap_type": "gpu",
            "target": row["gpu"],
            "priority": row.get("tracking_priority", 3),
            "recommended_action": f"Add source-labeled snapshot for GPU {row['gpu']}"
        })

for _, row in providers.iterrows():
    if row["provider"] not in covered_providers:
        rows.append({
            "gap_type": "provider",
            "target": row["provider"],
            "priority": row.get("tracking_priority", 3),
            "recommended_action": f"Add source-labeled snapshot for provider {row['provider']}"
        })

for _, row in regions.iterrows():
    if row["region_code"] not in covered_regions:
        rows.append({
            "gap_type": "region",
            "target": row["region_code"],
            "priority": row.get("tracking_priority", 3),
            "recommended_action": f"Add source-labeled snapshot for region {row['region_code']}"
        })

plan = pd.DataFrame(rows).sort_values(["gap_type", "priority", "target"])
plan.to_csv(DATA_DIR / "coverage_gap_plan.csv", index=False)

with open(REPORTS_DIR / "coverage_gap_plan.md", "w") as f:
    f.write("# AI-RPCT Coverage Gap Plan\n\n")
    f.write(f"Open gaps: {len(plan)}\n\n")
    for _, row in plan.iterrows():
        f.write(f"- [{row['gap_type']}] {row['target']} — {row['recommended_action']}\n")

print(plan)
