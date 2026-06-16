import pandas as pd

sources = [
    {
        "source": "Yahoo Finance",
        "type": "market_data",
        "status": "live_external"
    },
    {
        "source": "RunPod",
        "type": "gpu_provider",
        "status": "placeholder"
    },
    {
        "source": "Vast.ai",
        "type": "gpu_provider",
        "status": "placeholder"
    },
    {
        "source": "Lambda Labs",
        "type": "gpu_provider",
        "status": "placeholder"
    },
    {
        "source": "CoreWeave",
        "type": "gpu_provider",
        "status": "placeholder"
    }
]

df = pd.DataFrame(sources)
df.to_csv("data/data_source_status.csv", index=False)

print(df)
