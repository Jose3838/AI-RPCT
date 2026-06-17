from datetime import datetime

from integrations.provider_adapter_contract import validate_adapter_output

sample = [
    {
        "provider": "sample",
        "gpu": "H100",
        "price_per_hour": 2.50,
        "availability": 100,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

errors = validate_adapter_output(sample)

if errors:
    print("FAILED")
    print(errors)
    raise SystemExit(1)

print("Provider adapter contract test passed.")
