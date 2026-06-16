import sqlite3
import pandas as pd

conn = sqlite3.connect("data/airpct.db")

try:
    df = pd.read_sql_query(
        "SELECT * FROM rpct_scores",
        conn
    )

    print("Rows:", len(df))

    if "score" in df.columns:
        print("Average Score:", df["score"].mean())

except Exception as e:
    print(e)

conn.close()
