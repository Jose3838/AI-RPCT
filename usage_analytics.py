import sqlite3


DB_FILE = "ai_rpct.db"


def get_usage_analytics():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            api_key,
            endpoint,
            COUNT(*) as request_count
        FROM api_usage
        GROUP BY api_key, endpoint
        ORDER BY request_count DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "api_key": row[0],
            "endpoint": row[1],
            "request_count": row[2]
        }
        for row in rows
    ]
