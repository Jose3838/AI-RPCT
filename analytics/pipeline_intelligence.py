from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


manifest_path = Path("data/pipeline_manifest.json")
output_path = Path("data/pipeline_intelligence.csv")

if not manifest_path.exists():
    pd.DataFrame(
        [
            {
                "pipeline_health": 0,
                "status": "missing_manifest",
                "success_rate": 0,
                "passed": 0,
                "total": 0,
                "total_duration": 0,
                "slowest_step": "",
                "slowest_duration": 0,
            }
        ]
    ).to_csv(output_path, index=False)

    print("Pipeline intelligence unavailable: missing manifest")
else:
    manifest = json.loads(manifest_path.read_text())

    steps = manifest.get("steps", [])
    total = int(manifest.get("total", len(steps)))
    passed = int(manifest.get("passed", 0))

    success_rate = round((passed / total) * 100, 2) if total else 0
    pipeline_health = success_rate

    slowest = max(
        steps,
        key=lambda step: float(step.get("duration", 0)),
        default={},
    )

    pd.DataFrame(
        [
            {
                "pipeline_health": pipeline_health,
                "status": manifest.get("status", "UNKNOWN"),
                "success_rate": success_rate,
                "passed": passed,
                "total": total,
                "total_duration": manifest.get("duration_seconds", 0),
                "slowest_step": slowest.get("script", ""),
                "slowest_duration": slowest.get("duration", 0),
            }
        ]
    ).to_csv(output_path, index=False)

    print(pd.read_csv(output_path))
