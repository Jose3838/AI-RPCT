import sqlite3

from organizations import list_organizations


DB_FILE = "ai_rpct.db"


def get_usage_count_for_api_key(api_key):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM api_usage
        WHERE api_key = ?
        """,
        (api_key,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def build_organization_usage_dashboard():
    organizations = list_organizations()

    return {
        "status": "ok",
        "organizations": [
            {
                "id": org["id"],
                "name": org["name"],
                "plan": org["plan"],
                "api_key": org["api_key"],
                "usage_count": get_usage_count_for_api_key(
                    org["api_key"]
                )
            }
            for org in organizations
        ]
    }
