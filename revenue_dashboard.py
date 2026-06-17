from billing_engine import build_billing_summary


def build_revenue_dashboard():

    billing = build_billing_summary()

    total_accounts = len(billing)

    total_mrr = sum(
        item["monthly_price"]
        for item in billing
    )

    pro_mrr = sum(
        item["monthly_price"]
        for item in billing
        if item["plan"] == "pro"
    )

    enterprise_mrr = sum(
        item["monthly_price"]
        for item in billing
        if item["plan"] == "enterprise"
    )

    free_accounts = len([
        item
        for item in billing
        if item["plan"] == "free"
    ])

    pro_accounts = len([
        item
        for item in billing
        if item["plan"] == "pro"
    ])

    enterprise_accounts = len([
        item
        for item in billing
        if item["plan"] == "enterprise"
    ])

    return {
        "status": "ok",
        "total_accounts": total_accounts,
        "monthly_recurring_revenue": total_mrr,
        "annual_recurring_revenue": total_mrr * 12,
        "free_accounts": free_accounts,
        "pro_accounts": pro_accounts,
        "enterprise_accounts": enterprise_accounts,
        "pro_mrr": pro_mrr,
        "enterprise_mrr": enterprise_mrr
    }
