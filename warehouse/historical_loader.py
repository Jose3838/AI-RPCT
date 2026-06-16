import pandas as pd
import sqlite3

conn = sqlite3.connect("data/airpct.db")

tables = [
    "rpct_scores",
    "provider_rankings",
    "forecasts"
]

for table in tables:
    try:
        df = pd.read_sql_query(
            f"SELECT * FROM {table}",
            conn
        )

        print(
            table,
            len(df),
            "rows loaded"
        )

    except Exception as e:
        print(table, e)

conn.close()
