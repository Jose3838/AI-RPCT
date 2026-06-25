from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

SOURCE_REGISTRY = ROOT / "data" / "historical_source_registry.csv"

REGISTRIES = [
    ROOT / "data" / "amd_historical_gpu_registry.csv",
    ROOT / "data" / "intel_historical_gpu_registry.csv",
    ROOT / "data" / "historical_entity_registry.csv",
    ROOT / "data" / "historical_relationship_registry.csv",
]

with SOURCE_REGISTRY.open(newline="", encoding="utf-8") as f:
    valid_sources = {row["source_id"] for row in csv.DictReader(f)}

errors = []
warnings = []

for registry in REGISTRIES:
    if not registry.exists():
        continue

    with registry.open(newline="", encoding="utf-8") as f:
        for idx, row in enumerate(csv.DictReader(f), start=2):
            sid = row.get("source_id", "")

            if not sid:
                warnings.append(f"{registry.name}:{idx}: missing source_id")
                continue

            if sid not in valid_sources:
                errors.append(f"{registry.name}:{idx}: invalid source_id '{sid}'")

if warnings:
    print("Source validation warnings:")
    for warning in warnings:
        print(warning)

if errors:
    print("Source validation failed:")
    for error in errors:
        print(error)
    raise SystemExit(1)

print("All available source references are valid.")
