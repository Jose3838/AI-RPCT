import sqlite3
from datetime import datetime
import secrets


DB_FILE = "ai_rpct.db"


def create_api_key(
    organization_id,
    plan
):
    api_key = "airpct_" + secrets.token_hex(16)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO api_keys
        (
            organization_id,
            api_key,
            plan,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            organization_id,
            api_key,
            plan,
            "active",
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {
        "status": "created",
        "organization_id": organization_id,
        "api_key": api_key,
        "plan": plan
    }


def list_api_keys():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            organization_id,
            api_key,
            plan,
            status,
            created_at
        FROM api_keys
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "organization_id": row[1],
            "api_key": row[2],
            "plan": row[3],
            "status": row[4],
            "created_at": row[5]
        }
        for row in rows
    ]
