from main import (
    terminal_customer_decision_center_v1,
    terminal_intelligence_summary_v2
)


def daily_intelligence_brief_v1():

    summary = terminal_intelligence_summary_v2()
    decision = terminal_customer_decision_center_v1()

    collection = summary["collection_health"]["collection"]["status"]
    moat = summary["data_moat"]["data_moat"]["data_moat_score"]
    product = summary["product_readiness"]["product_readiness"]["product_readiness_score"]
    executive = summary["executive_scorecard"]["scorecard"]["executive_score"]

    return {
        "status": "ok",
        "version": "v1",
        "market_health": collection,
        "data_moat": moat,
        "product_readiness": product,
        "executive_score": executive,
        "headline": decision.get("headline"),
        "customer_decision": decision
    }
