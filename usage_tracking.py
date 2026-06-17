import sqlite3
from datetime import datetime


DB_FILE = "ai_rpct.db"


def track_usage(
    api_key,
    endpoint
):
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO api_usage
        (
            api_key,
            endpoint,
            timestamp
        )
        VALUES (?, ?, ?)
        """,
        (
            api_key,
            endpoint,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return True
