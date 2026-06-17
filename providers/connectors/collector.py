from providers.connectors.registry import CONNECTORS


def collect_provider_data():

    results = []

    for connector in CONNECTORS:
        results.append(
            connector.fetch()
        )

    return results
