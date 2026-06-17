from collectors.providers.vast_real import VastRealProvider
from integrations.provider_adapter_contract import (
    validate_adapter_output
)

provider = VastRealProvider()

rows = provider.fetch()

errors = validate_adapter_output(rows)

if errors:
    print("FAILED")
    print(errors)
    raise SystemExit(1)

print(f"Vast connector returned {len(rows)} rows.")
print("Vast connector contract valid.")
