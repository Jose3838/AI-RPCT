from connector_health_dashboard import (
    build_connector_health_dashboard
)


def build_connector_maturity_dashboard():

    health = build_connector_health_dashboard()

    maturity = []

    for connector in health["connectors"]:

        if connector["status"] == "live":
            level = "production"

        elif connector["status"] == "fallback":
            level = "integration_ready"

        else:
            level = "prototype"

        maturity.append({
            "provider": connector["provider"],
            "maturity": level,
            "source": connector["source"]
        })

    return {
        "status": "ok",
        "version": "v1",
        "connectors": maturity
    }
