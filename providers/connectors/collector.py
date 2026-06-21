from providers.connectors.registry import CONNECTORS
from intelligence.normalization.offer_normalizer import normalize_provider_result
from intelligence.live_offer_history import append_live_offer_history


def collect_provider_data():
    raw_results = []
    normalized_results = []

    for connector in CONNECTORS:
        try:
            result = connector.fetch()
        except Exception as error:
            result = {
                "provider": getattr(connector, "provider_name", "unknown"),
                "mode": "error",
                "source": "connector_exception",
                "error": str(error),
            }

        raw_results.append(result)

        offers = normalize_provider_result(result)

        normalized_results.append({
            "provider": result.get("provider") or getattr(connector, "provider_name", "unknown"),
            "mode": result.get("mode", "live" if "live_api" in result.get("source", "") else "demo"),
            "live_ready": result.get("live_ready", "live_api" in result.get("source", "")),
            "offers": offers,
            "raw": result,
        })

    history = append_live_offer_history(normalized_results)

    return {
        "providers": raw_results,
        "normalized_providers": normalized_results,
        "history": history,
        "summary": {
            "total_connectors": len(CONNECTORS),
            "live_ready": sum(1 for r in normalized_results if r.get("live_ready")),
            "demo_mode": sum(1 for r in normalized_results if r.get("mode") == "demo"),
            "total_normalized_offers": sum(len(r.get("offers", [])) for r in normalized_results),
        },
    }
