#!/bin/bash

cd "$(dirname "$0")"

if [ -d "venv" ]; then
  source venv/bin/activate
fi

python - <<'PY'
from intelligence.master_intelligence_collector import (
    run_master_intelligence_collector
)

print(
    run_master_intelligence_collector()
)
PY

echo ""
echo "Hourly collection completed"
echo ""
