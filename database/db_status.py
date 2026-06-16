import sqlite3
from database.db import DB_FILE

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

tables = ["rpct_scores", "provider_rankings", "forecasts"]

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
