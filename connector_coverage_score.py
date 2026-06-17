from connector_maturity_dashboard import build_connector_maturity_dashboard


def build_connector_coverage_score():
    dashboard = build_connector_maturity_dashboard()
    connectors = dashboard["connectors"]

    total = len(connectors)

    production = len([
        item for item in connectors
        if item["maturity"] == "production"
    ])

    integration_ready = len([
        item for item in connectors
        if item["maturity"] == "integration_ready"
    ])

    prototype = len([
        item for item in connectors
        if item["maturity"] == "prototype"
    ])

    score = round(
        ((production + integration_ready * 0.5) / total) * 100,
        2
    ) if total else 0

    return {
        "status": "ok",
        "version": "v1",
        "connector_coverage_score": score,
        "production_connectors": production,
        "integration_ready_connectors": integration_ready,
        "prototype_connectors": prototype,
        "total_connectors": total
    }
