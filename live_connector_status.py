from providers.connectors.collector import collect_provider_data

data = collect_provider_data()

print("AI-RPCT LIVE CONNECTOR STATUS")
print("============================")
print(data["summary"])
print()

for p in data["providers"]:
    print(
        p["provider"],
        "| mode:", p.get("mode", "unknown"),
        "| live_ready:", p.get("live_ready", False),
        "| reason:", p.get("reason", "")
    )
