from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

gap = pd.read_csv(DATA_DIR / "coverage_gap_plan.csv")

def impact_score(row):
    gap_type = row["gap_type"]
    priority = int(row["priority"])

    base = 100 - ((priority - 1) * 20)

    if gap_type == "gpu":
        return base + 10
    if gap_type == "provider":
        return base + 5
    if gap_type == "region":
        return base
    return base

gap["impact_score"] = gap.apply(impact_score, axis=1)
gap["recommended_order"] = gap["impact_score"].rank(method="first", ascending=False).astype(int)

gap = gap.sort_values(["recommended_order"])

gap.to_csv(DATA_DIR / "coverage_gap_priority.csv", index=False)

print(gap)
