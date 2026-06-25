from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REGISTRIES = [
    ROOT / "data" / "amd_historical_gpu_registry.csv",
    ROOT / "data" / "intel_historical_gpu_registry.csv",
]

with SOURCE_REGISTRY.open(newline="", encoding="utf-8") as f:
    valid_sources = {
        row["source_id"]
        for row in csv.DictReader(f)
    }

errors = []

for registry in REGISTRIES:

    with registry.open(newline="", encoding="utf-8") as f:

        for row in csv.DictReader(f):

            sid = row.get("source_id", "")

            if sid not in valid_sources:
                errors.append(
                    f"{registry.name}: invalid source_id '{sid}'"
                )

if errors:

    print("Source validation failed:")

    for e in errors:
        print(e)

    raise SystemExit(1)

print("All source references are valid.")
