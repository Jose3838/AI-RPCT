from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision.history import append_history


def main() -> None:
    append_history()
    print("Decision history updated.")


if __name__ == "__main__":
    main()
