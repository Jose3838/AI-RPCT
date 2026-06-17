from data_layer.trend_engine import build_market_trend_summary
from data_layer.market_strength_pipeline import build_dynamic_market_strength_index
from data_layer.executive_intelligence_pipeline import build_dynamic_executive_intelligence_summary


def build_weekly_infrastructure_report():
    trend = build_market_trend_summary()
    market = build_dynamic_market_strength_index()
    executive = build_dynamic_executive_intelligence_summary()

    return {
        "status": "ok",
        "version": "v1",
        "report_type": "weekly_infrastructure_report",
        "market_strength": market,
        "trend_summary": trend,
        "executive_summary": executive,
        "cto_recommendation": "Continue provider expansion and increase historical snapshot frequency."
    }
