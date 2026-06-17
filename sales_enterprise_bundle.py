from enterprise_report_index import build_enterprise_report_index
from data_layer.executive_intelligence_pipeline import build_dynamic_executive_intelligence_summary
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores


def build_sales_enterprise_bundle():
    return {
        "status": "ok",
        "version": "v1",
        "bundle_type": "sales_enterprise_bundle",
        "positioning": "Bloomberg-style AI Infrastructure Intelligence",
        "target_customer": [
            "AI labs",
            "cloud GPU buyers",
            "infrastructure investors",
            "enterprise procurement teams"
        ],
        "value_proposition": [
            "Provider activation scoring",
            "Market strength index",
            "Historical market snapshots",
            "Weekly infrastructure intelligence",
            "Enterprise-ready reporting"
        ],
        "provider_scores": build_dynamic_provider_activation_scores(),
        "executive_summary": build_dynamic_executive_intelligence_summary(),
        "enterprise_report": build_enterprise_report_index(),
        "commercial_status": "ready_for_paid_enterprise_demo"
    }
