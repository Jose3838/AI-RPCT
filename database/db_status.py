import sqlite3
from pathlib import Path

DB_FILE = "data/airpct.db"

if not Path(DB_FILE).exists():
    print("Database not found:", DB_FILE)
    raise SystemExit(1)

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

tables = [
    "rpct_scores",
    "provider_rankings",
    "forecasts"
]

print("AI-RPCT DATABASE STATUS")
print("=======================")

for table in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"{table}: {count} rows")
    except Exception as e:
        print(f"{table}: ERROR {e}")

conn.close()
