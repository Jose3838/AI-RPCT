from providers.connectors.registry import CONNECTORS


def collect_provider_data():

    results = []

    live_count = 0
    demo_count = 0

    for connector in CONNECTORS:

        data = connector.fetch()

        if data.get("live_ready"):
            live_count += 1
        else:
            demo_count += 1

        results.append(data)

    return {
        "providers": results,
        "summary": {
            "total_connectors": len(CONNECTORS),
            "live_ready": live_count,
            "demo_mode": demo_count
        }
    }

