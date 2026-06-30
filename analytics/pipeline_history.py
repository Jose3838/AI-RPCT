from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


manifest_path = Path("data/pipeline_manifest.json")
history_path = Path("data/pipeline_history.csv")

if not manifest_path.exists():
    print("Pipeline history unavailable: missing manifest")
else:
    manifest = json.loads(manifest_path.read_text())

    total = int(manifest.get("total", 0))
    passed = int(manifest.get("passed", 0))
    success_rate = round((passed / total) * 100, 2) if total else 0

    row = pd.DataFrame(
        [
            {
                "timestamp": manifest.get("timestamp", ""),
                "status": manifest.get("status", "UNKNOWN"),
                "pipeline_health": success_rate,
                "success_rate": success_rate,
                "passed": passed,
                "total": total,
                "duration_seconds": manifest.get("duration_seconds", 0),
            }
        ]
    )

    if history_path.exists():
        old = pd.read_csv(history_path)
        data = pd.concat([old, row], ignore_index=True)
    else:
        data = row

    data.to_csv(history_path, index=False)
    print(data.tail(5))
