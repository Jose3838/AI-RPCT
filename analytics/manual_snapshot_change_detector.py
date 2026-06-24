from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
HISTORY_DIR = Path("warehouse/manual_snapshot_history")

REPORTS_DIR.mkdir(exist_ok=True)

def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

def normalize_key(df):
    if df.empty:
        return df
    df = df.copy()
    df["snapshot_key"] = (
        df["provider"].astype(str).str.lower().str.strip()
        + "|" + df["gpu"].astype(str).str.lower().str.strip()
        + "|" + df["region_code"].astype(str).str.lower().str.strip()
    )
    return df

files = sorted(HISTORY_DIR.glob("manual_snapshot_*.csv"))
current = normalize_key(read_csv(DATA_DIR / "manual_market_snapshots.csv"))

rows = []

if len(files) >= 1 and not current.empty:
    previous = normalize_key(read_csv(files[-1]))

    prev_keys = set(previous["snapshot_key"]) if not previous.empty else set()
    curr_keys = set(current["snapshot_key"])

    for key in sorted(curr_keys - prev_keys):
        row = current[current["snapshot_key"] == key].iloc[0]
        rows.append({
            "change_type": "new_snapshot",
            "provider": row["provider"],
            "gpu": row["gpu"],
            "region_code": row["region_code"],
            "old_price_per_hour": "",
            "new_price_per_hour": row["price_per_hour"],
            "price_delta_pct": "",
            "old_availability": "",
            "new_availability": row["availability"],
            "source_url": row["source_url"],
            "claim_scope": row["claim_scope"]
        })

    for key in sorted(prev_keys & curr_keys):
        old = previous[previous["snapshot_key"] == key].iloc[0]
        new = current[current["snapshot_key"] == key].iloc[0]

        try:
            old_price = float(old["price_per_hour"])
            new_price = float(new["price_per_hour"])
            price_delta_pct = round(((new_price - old_price) / old_price) * 100, 2) if old_price else 0
        except Exception:
            old_price = old.get("price_per_hour", "")
            new_price = new.get("price_per_hour", "")
            price_delta_pct = ""

        try:
            old_avail = float(old["availability"])
            new_avail = float(new["availability"])
            availability_delta = new_avail - old_avail
        except Exception:
            old_avail = old.get("availability", "")
            new_avail = new.get("availability", "")
            availability_delta = ""

        if price_delta_pct not in ("", 0) or availability_delta not in ("", 0):
            rows.append({
                "change_type": "changed_snapshot",
                "provider": new["provider"],
                "gpu": new["gpu"],
                "region_code": new["region_code"],
                "old_price_per_hour": old_price,
                "new_price_per_hour": new_price,
                "price_delta_pct": price_delta_pct,
                "old_availability": old_avail,
                "new_availability": new_avail,
                "source_url": new["source_url"],
                "claim_scope": new["claim_scope"]
            })

    for key in sorted(prev_keys - curr_keys):
        row = previous[previous["snapshot_key"] == key].iloc[0]
        rows.append({
            "change_type": "removed_snapshot",
            "provider": row["provider"],
            "gpu": row["gpu"],
            "region_code": row["region_code"],
            "old_price_per_hour": row["price_per_hour"],
            "new_price_per_hour": "",
            "price_delta_pct": "",
            "old_availability": row["availability"],
            "new_availability": "",
            "source_url": row["source_url"],
            "claim_scope": row["claim_scope"]
        })

changes = pd.DataFrame(rows)
changes.to_csv(DATA_DIR / "manual_snapshot_changes.csv", index=False)

with open(REPORTS_DIR / "manual_snapshot_changes.md", "w") as f:
    f.write("# AI-RPCT Manual Snapshot Changes\n\n")
    f.write(f"Change count: {len(changes)}\n\n")
    if changes.empty:
        f.write("No changes detected.\n")
    else:
        for _, row in changes.iterrows():
            f.write(
                f"- {row['change_type']}: {row['provider']} / {row['gpu']} / {row['region_code']} "
                f"price {row['old_price_per_hour']} -> {row['new_price_per_hour']} "
                f"delta {row['price_delta_pct']}\n"
            )

print(changes)
