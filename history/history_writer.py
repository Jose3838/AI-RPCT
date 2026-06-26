from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def append_row(
    output: Path,
    fieldnames: list[str],
    row: dict[str, str],
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    exists = output.exists()

    with output.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not exists:
            writer.writeheader()

        writer.writerow(row)


def append_many(
    outputs: Iterable[Path],
    fieldnames: list[str],
    row: dict[str, str],
) -> None:
    for output in outputs:
        append_row(output, fieldnames, row)
