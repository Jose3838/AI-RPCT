import pandas as pd

vast = pd.read_csv("data/live_provider_data.csv")
runpod = pd.read_csv("data/runpod_live_report.csv")

vast_gpus = set(vast["gpu"].dropna().unique())
runpod_gpus = set(runpod["gpu"].dropna().unique())

all_gpus = vast_gpus.union(runpod_gpus)

coverage = []

for gpu in sorted(all_gpus):
    coverage.append({
        "gpu": gpu,
        "vast": gpu in vast_gpus,
        "runpod": gpu in runpod_gpus,
        "providers_count": int(gpu in vast_gpus) + int(gpu in runpod_gpus)
    })

df = pd.DataFrame(coverage)

df.to_csv("data/provider_coverage_score.csv", index=False)

print(df.head())
