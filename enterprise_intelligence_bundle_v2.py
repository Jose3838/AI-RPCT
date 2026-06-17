from sales_enterprise_bundle import build_sales_enterprise_bundle
from data_trust_index import build_data_trust_index
from provider_freshness import build_provider_freshness_report
from providers.connectors.collector import collect_provider_data


def build_enterprise_intelligence_bundle_v2():
    providers = collect_provider_data()

    return {
        "status": "ok",
        "version": "v2",
        "bundle_type": "enterprise_intelligence_bundle",
        "positioning": "Institutional-grade AI Infrastructure Intelligence",
        "data_trust": build_data_trust_index(),
        "provider_freshness": build_provider_freshness_report(providers),
        "sales_bundle": build_sales_enterprise_bundle(),
        "commercial_signal": "ready_for_enterprise_pilots"
    }
