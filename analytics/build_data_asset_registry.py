from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEARCH_DIRS = [
    "data",
    "warehouse",
]

OUTPUTS = [
    ROOT / "data" / "data_asset_registry.csv",
    ROOT / "warehouse" / "metadata" / "data_asset_registry.csv",
]

FIELDS = [
    "asset_path",
    "extension",
    "size_bytes",
    "category",
]


def category(path: Path) -> str:
    p = str(path).lower()

    if "forecast" in p:
        return "forecast"
    if "registry" in p:
        return "registry"
    if "provider" in p:
        return "provider"
    if "history" in p or "historical" in p:
        return "history"
    if "signal" in p:
        return "signal"
    if "dashboard" in p:
        return "dashboard"

    return "other"


rows = []

for folder in SEARCH_DIRS:
    root = ROOT / folder
    if not root.exists():
        continue

    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue

        rows.append(
            {
                "asset_path": str(file.relative_to(ROOT)),
                "extension": file.suffix,
                "size_bytes": file.stat().st_size,
                "category": category(file),
            }
        )

for output in OUTPUTS:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

print(f"Indexed {len(rows)} data assets.")
