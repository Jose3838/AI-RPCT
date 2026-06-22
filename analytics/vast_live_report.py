import pandas as pd
from pathlib import Path

from collectors.providers.vast_real import VastRealProvider


def main():
    provider = VastRealProvider()
    rows = provider.fetch()
    df = pd.DataFrame(rows)
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/vast_live_report.csv", index=False)
    print(f"Vast live rows: {len(df)}")
    print(df.head() if not df.empty else "No live Vast data yet")


if __name__ == "__main__":
    main()
