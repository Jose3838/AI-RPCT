from main import (
    terminal_daily_intelligence_brief_v1,
    terminal_data_moat_v2,
    terminal_forecast_accuracy_trend_v1,
    terminal_customer_decision_center_v1
)


def weekly_market_report_v1():

    brief = terminal_daily_intelligence_brief_v1()
    moat = terminal_data_moat_v2()
    forecast = terminal_forecast_accuracy_trend_v1()
    decision = terminal_customer_decision_center_v1()

    return {
        "status": "ok",
        "version": "v1",
        "headline": "Weekly GPU infrastructure market intelligence report",
        "daily_brief": brief.get("brief"),
        "data_moat": moat.get("data_moat"),
        "forecast_trend": forecast.get("trend"),
        "customer_decision": decision,
        "summary": (
            f"Market health is {brief.get('brief', {}).get('market_health')}. "
            f"Data moat score is {brief.get('brief', {}).get('data_moat')}. "
            f"Decision headline: {decision.get('headline')}."
        )
    }
