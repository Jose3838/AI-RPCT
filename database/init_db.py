from database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS rpct_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    score REAL,
    regime TEXT,
    drivers TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS provider_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT,
    price_per_hour REAL,
    availability REAL,
    score REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latest_rpct REAL,
    shortage_probability REAL,
    forecast_score REAL,
    outlook TEXT
)
""")

conn.commit()
conn.close()

print("SQLite database initialized.")
