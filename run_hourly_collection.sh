#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================="
echo "AI-RPCT HOURLY COLLECTION"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "=============================="

if [ -d "venv" ]; then
  source venv/bin/activate
fi

python - <<'PY'
from intelligence.master_intelligence_collector import (
    run_master_intelligence_collector
)

import json

result = run_master_intelligence_collector()

print(json.dumps(result, indent=2, default=str))

if result.get("status") not in ["ok", "completed", "success"]:
    raise SystemExit("Hourly collection failed")
PY

echo ""
echo "Hourly collection completed successfully"
echo ""
