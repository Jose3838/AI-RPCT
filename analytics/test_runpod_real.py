from collectors.providers.runpod_real import RunPodRealProvider
from integrations.provider_adapter_contract import validate_adapter_output

provider = RunPodRealProvider()
rows = provider.fetch()

errors = validate_adapter_output(rows)

if errors:
    print("FAILED")
    print(errors)
    raise SystemExit(1)

print(f"RunPod connector returned {len(rows)} rows.")
print("RunPod connector contract valid.")
