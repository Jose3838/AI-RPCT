from __future__ import annotations

from pathlib import Path
import pandas as pd

OUT = Path("data/historical_source_registry_v1.csv")
REPORT = Path("reports/historical_source_registry_v1.md")

SOURCES = [
    {
        "source": "AWS",
        "category": "hyperscaler",
        "automation": "api_or_scraper",
        "priority": "critical",
        "target": "pricing, gpu catalog, regions",
        "status": "planned",
    },
    {
        "source": "Azure",
        "category": "hyperscaler",
        "automation": "api_or_scraper",
        "priority": "critical",
        "target": "vm pricing, gpu catalog",
        "status": "planned",
    },
    {
        "source": "Google Cloud",
        "category": "hyperscaler",
        "automation": "api_or_scraper",
        "priority": "critical",
        "target": "accelerators, pricing",
        "status": "planned",
    },
    {
        "source": "CoreWeave",
        "category": "gpu_cloud",
        "automation": "scraper",
        "priority": "high",
        "target": "gpu inventory",
        "status": "planned",
    },
    {
        "source": "Lambda",
        "category": "gpu_cloud",
        "automation": "scraper",
        "priority": "high",
        "target": "pricing",
        "status": "planned",
    },
    {
        "source": "Crusoe",
        "category": "gpu_cloud",
        "automation": "scraper",
        "priority": "high",
        "target": "gpu catalog",
        "status": "planned",
    },
    {
        "source": "Nebius",
        "category": "gpu_cloud",
        "automation": "scraper",
        "priority": "medium",
        "target": "gpu catalog",
        "status": "planned",
    },
]

def main():
    df = pd.DataFrame(SOURCES)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        f"""# Historical Source Registry v1

Sources: {len(df)}

## Purpose

Central registry for all historical data collectors.

Every future collector should register here before entering the production pipeline.

This registry becomes the control center of the AI-RPCT data moat.
""",
        encoding="utf-8",
    )

    print("HISTORICAL SOURCE REGISTRY V1")
    print("=============================")
    print(df)

if __name__ == "__main__":
    main()
