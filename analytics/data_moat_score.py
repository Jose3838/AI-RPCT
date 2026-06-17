from pathlib import Path
import pandas as pd

checks = {
    "snapshots": Path("warehouse/snapshots").exists() and any(Path("warehouse/snapshots").iterdir()),
    "index_history": Path("data/index_history.csv").exists(),
    "provider_history": Path("data/provider_daily_metrics.csv").exists(),
    "ai_index": Path("data/ai_infrastructure_index.csv").exists(),
    "gpu_scarcity": Path("data/gpu_scarcity_index.csv").exists()
}

score = round(sum(checks.values()) / len(checks) * 100, 2)

out = pd.DataFrame([{
    "data_moat_score": score,
    **checks
}])

out.to_csv("data/data_moat_score.csv", index=False)

print(out)
