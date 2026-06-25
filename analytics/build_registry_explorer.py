from __future__ import annotations

from pathlib import Path

from builders.csv_loader import load_csv

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "registry_metadata.csv"

OUTPUT = ROOT / "reports" / "registry_explorer.md"


def main():
    rows = load_csv(INPUT)

    lines = [
        "# AI-RPCT Registry Explorer",
        "",
        "| Registry | Rows | Warehouse | Status |",
        "|-----------|------|-----------|--------|",
    ]

    for row in rows:
        lines.append(
            f"| {row['registry_name']} | "
            f"{row['row_count']} | "
            f"{row['warehouse_group']} | "
            f"{row['status']} |"
        )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print("Registry explorer generated.")
    print(OUTPUT)


if __name__ == "__main__":
    main()
