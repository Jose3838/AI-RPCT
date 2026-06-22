import pandas as pd
from pathlib import Path

from collectors.providers.runpod_real import RunPodRealProvider


def main():
    provider = RunPodRealProvider()
    rows = provider.fetch()
    df = pd.DataFrame(rows)
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/runpod_live_report.csv", index=False)
    print(f"RunPod live rows: {len(df)}")
    print(df.head() if not df.empty else "No live RunPod data yet")


if __name__ == "__main__":
    main()
