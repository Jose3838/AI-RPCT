from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


PIPELINE = [
    ("collector", "collectors/collect_market_data.py"),
    ("collector", "collectors/collect_gpu_data.py"),
    ("engine", "engine/calculate_rpct.py"),
    ("analytics", "analytics/provider_rankings.py"),
    ("analytics", "analytics/provider_marketshare.py"),
    ("analytics", "analytics/provider_concentration.py"),
    ("analytics", "analytics/shortage_probability.py"),
    ("forecast", "analytics/forecast_signal.py"),
    ("forecast", "analytics/time_series_forecast.py"),
    ("analytics", "analytics/market_regime.py"),
    ("analytics", "analytics/predictor.py"),
    ("forecast", "analytics/forecast_accuracy.py"),
]


def run(group: str, script: str) -> dict:
    print(f"\n▶ [{group}] {script}")
    start = time.time()

    result = subprocess.run(
        ["python", script],
        check=False,
        env={**os.environ, "PYTHONPATH": "."},
    )

    duration = round(time.time() - start, 2)
    status = "PASS" if result.returncode == 0 else "FAIL"

    print(f"   {status} ({duration}s)")

    return {
        "group": group,
        "script": script,
        "status": status,
        "duration": duration,
    }


def main() -> None:
    start = time.time()

    results = [run(group, script) for group, script in PIPELINE]
    passed = sum(1 for result in results if result["status"] == "PASS")
    overall_status = "SUCCESS" if passed == len(results) else "FAILED"

    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": overall_status,
        "passed": passed,
        "total": len(results),
        "duration_seconds": round(time.time() - start, 2),
        "steps": results,
    }

    Path("data").mkdir(exist_ok=True)

    with open("data/pipeline_manifest.json", "w") as file:
        json.dump(manifest, file, indent=2)

    print("\n==============================")
    print("PIPELINE SUMMARY")
    print("==============================")

    for result in results:
        print(
            f"{result['status']:4} | "
            f"{result['group']:10} | "
            f"{result['duration']:>5}s | "
            f"{result['script']}"
        )

    print("==============================")
    print(f"Passed   : {passed}/{len(results)}")
    print(f"Duration : {time.time() - start:.1f}s")
    print("Overall  : " + overall_status)
    print("Manifest : data/pipeline_manifest.json")


if __name__ == "__main__":
    main()
