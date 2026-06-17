import sqlite3
from datetime import datetime


DB_FILE = "ai_rpct.db"


def create_organization(
    name,
    plan,
    api_key
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO organizations
        (
            name,
            plan,
            api_key,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            plan,
            api_key,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {
        "status": "created",
        "name": name,
        "plan": plan,
        "api_key": api_key
    }


def list_organizations():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            plan,
            api_key,
            created_at
        FROM organizations
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "plan": row[2],
            "api_key": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]
