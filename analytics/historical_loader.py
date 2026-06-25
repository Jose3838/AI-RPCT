from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path("warehouse/historical")
OUTPUT = Path("data/historical_master_dataset.csv")


def load_all_history():
    dfs = []

    for csv in ROOT.rglob("*.csv"):
        try:
            df = pd.read_csv(csv)

            df["dataset"] = csv.parent.name
            df["source_file"] = csv.name

            dfs.append(df)

        except Exception as e:
            print(f"Skipped {csv}: {e}")

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True, sort=False)


def main():

    df = load_all_history()

    OUTPUT.parent.mkdir(exist_ok=True)

    df.to_csv(OUTPUT, index=False)

    print("HISTORICAL MASTER DATASET")
    print("=========================")
    print(f"Datasets : {df['dataset'].nunique() if not df.empty else 0}")
    print(f"Rows     : {len(df)}")
    print(f"Columns  : {len(df.columns)}")
    print(f"CSV      : {OUTPUT}")


if __name__ == "__main__":
    main()
