from intelligence.customer.customer_value_dashboard_v1 import customer_value_dashboard_v1
from intelligence.customer.gpu_budget_advisor_v1 import gpu_budget_advisor_v1
from intelligence.customer.provider_switching_advisor_v1 import provider_switching_advisor_v1
from intelligence.customer.gpu_risk_advisor_v1 import gpu_risk_advisor_v1
from intelligence.signals.data_moat_score_v2 import data_moat_score_v2
from intelligence.product.product_readiness_snapshot_v1 import product_readiness_snapshot_v1
from intelligence.executive.executive_scorecard_v1 import executive_scorecard_v1
from intelligence.operations.collection_health import collection_health


def customer_demo_snapshot_v1():
    customer_value = customer_value_dashboard_v1()
    budget = gpu_budget_advisor_v1()
    provider = provider_switching_advisor_v1()
    risk = gpu_risk_advisor_v1()
    moat = data_moat_score_v2()
    product = product_readiness_snapshot_v1()
    executive = executive_scorecard_v1()
    collection = collection_health()

    return {
        "status": "ok",
        "version": "v1",
        "headline": (
            f"AI-RPCT detects {customer_value.get('buy_count', 0)} GPU buy signals. "
            f"Budget decision: {budget.get('decision')}. "
            f"Provider decision: {provider.get('decision')}."
        ),
        "scores": {
            "data_moat": moat.get("data_moat_score"),
            "product_readiness": product.get("product_readiness_score"),
            "executive_score": executive.get("executive_score"),
            "collection": collection.get("status")
        },
        "customer_decision": {
            "budget_advisor": budget,
            "provider_switching": provider,
            "gpu_risk": risk,
            "customer_value": customer_value
        }
    }
