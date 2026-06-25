from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


GRAPH = """
# AI-RPCT Dependency Graph

Historical Source Registry
        |
        v
Historical Entity Registry
        |
        v
Provider Entity Registry
        |
        v
Provider Relationship Registry
        |
        +-------------------+
        |                   |
        v                   v
Unified Accelerator     Historical Capacity
        |                   |
        +---------+---------+
                  |
                  v
           Feature Store
                  |
                  v
         Forecast Dataset
                  |
                  v
      Forecast Engine v1
                  |
                  v
   Forecast Explanations
                  |
                  +------------------------+
                  |                        |
                  v                        v
      Data Quality Metrics      Pipeline Health
                  |                        |
                  +------------+-----------+
                               |
                               v
                     Pipeline Dashboard
"""


def main():
    output = ROOT / "reports" / "dependency_graph.md"

    output.write_text(GRAPH.strip() + "\n", encoding="utf-8")

    print("Dependency graph generated.")
    print(output)


if __name__ == "__main__":
    main()
