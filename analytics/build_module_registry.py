from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DATA = ROOT / "data" / "module_registry.csv"
OUTPUT_WAREHOUSE = ROOT / "warehouse" / "metadata" / "module_registry.csv"

COLUMNS = [
    "module_path",
    "layer",
    "module_type",
    "status",
]


def classify(path: Path) -> str:
    text = str(path)

    if text.startswith("collectors/") or "connector" in text:
        return "collection"

    if text.startswith("analytics/build_") or "registry" in text:
        return "registry"

    if "forecast" in text:
        return "forecast"

    if any(word in text for word in ["signal", "scarcity", "ranking", "intelligence"]):
        return "intelligence"

    if any(word in text for word in ["decision", "recommendation", "executive"]):
        return "decision"

    if text.startswith("api/"):
        return "api"

    if text.startswith("web/") or "dashboard" in text:
        return "web"

    if text.startswith("reports/"):
        return "reports"

    return "platform"


def module_type(path: Path) -> str:
    if path.suffix == ".py":
        return "python"
    if path.suffix == ".csv":
        return "dataset"
    if path.suffix == ".md":
        return "report"
    if path.suffix == ".html":
        return "web"
    if path.suffix == ".json":
        return "json"
    return "other"


def discover() -> list[dict[str, str]]:
    rows = []

    roots = ["analytics", "api", "collectors", "providers", "data_layer", "web", "reports"]

    for root_name in roots:
        root = ROOT / root_name
        if not root.exists():
            continue

        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue

            if "__pycache__" in path.parts:
                continue

            rel = path.relative_to(ROOT)

            rows.append(
                {
                    "module_path": str(rel),
                    "layer": classify(rel),
                    "module_type": module_type(path),
                    "status": "active",
                }
            )

    return rows


def write(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = discover()

    write(OUTPUT_DATA, rows)
    write(OUTPUT_WAREHOUSE, rows)

    print(f"Wrote {len(rows)} module registry records.")
    print(OUTPUT_DATA)
    print(OUTPUT_WAREHOUSE)


if __name__ == "__main__":
    main()
