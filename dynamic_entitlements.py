import sqlite3


DB_FILE = "ai_rpct.db"


DEMO_KEYS = {
    "demo-free-key": "free",
    "demo-pro-key": "pro",
    "demo-enterprise-key": "enterprise"
}


def get_plan_for_api_key(api_key):
    if api_key in DEMO_KEYS:
        return DEMO_KEYS[api_key]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT plan
        FROM api_keys
        WHERE api_key = ?
        AND status = 'active'
        LIMIT 1
        """,
        (api_key,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "unknown"

    return row[0]


def require_plan(api_key, allowed_plans):
    plan = get_plan_for_api_key(api_key)

    if plan not in allowed_plans:
        return {
            "allowed": False,
            "plan": plan,
            "error": "insufficient_plan"
        }

    return {
        "allowed": True,
        "plan": plan
    }
