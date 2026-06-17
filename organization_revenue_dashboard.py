from organizations import list_organizations


PLAN_PRICING = {
    "free": 0,
    "pro": 99,
    "enterprise": 999
}


def build_organization_revenue_dashboard():
    organizations = list_organizations()

    total_mrr = sum(
        PLAN_PRICING.get(org["plan"], 0)
        for org in organizations
    )

    return {
        "status": "ok",
        "total_organizations": len(organizations),
        "monthly_recurring_revenue": total_mrr,
        "annual_recurring_revenue": total_mrr * 12,
        "organizations": [
            {
                "name": org["name"],
                "plan": org["plan"],
                "mrr": PLAN_PRICING.get(org["plan"], 0)
            }
            for org in organizations
        ]
    }
