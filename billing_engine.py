import sqlite3


DB_FILE = "ai_rpct.db"


PLAN_PRICING = {
    "free": 0,
    "pro": 99,
    "enterprise": 999
}


API_KEYS = {
    "demo-free-key": "free",
    "demo-pro-key": "pro",
    "demo-enterprise-key": "enterprise"
}


def build_billing_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            api_key,
            COUNT(*)
        FROM api_usage
        GROUP BY api_key
        """
    )

    rows = cursor.fetchall()

    conn.close()

    result = []

    for api_key, usage_count in rows:

        plan = API_KEYS.get(
            api_key,
            "free"
        )

        monthly_price = PLAN_PRICING.get(
            plan,
            0
        )

        result.append({
            "api_key": api_key,
            "plan": plan,
            "monthly_price": monthly_price,
            "usage_count": usage_count
        })

    return result
