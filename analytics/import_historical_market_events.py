from __future__ import annotations

from pathlib import Path

from historical_import.base_importer import BaseHistoricalImporter
from historical_import.provenance import append_provenance
from historical_import.validators import validate_rows


class HistoricalMarketEventsImporter(BaseHistoricalImporter):
    source_name = "Market Events"
    category = "market_events"
    trust_grade = "A"
    output_dir = Path("warehouse/historical/market_events")

    def fetch_rows(self) -> list[dict]:
        return [
            {
                "date": "2006-06-23",
                "event_name": "CUDA introduced",
                "event_type": "platform",
                "impact_area": "gpu_compute",
                "description": "CUDA created the foundation for general-purpose GPU computing.",
            },
            {
                "date": "2012-09-30",
                "event_name": "AlexNet wins ImageNet",
                "event_type": "ai_breakthrough",
                "impact_area": "deep_learning_demand",
                "description": "Deep learning accelerated demand for GPU compute.",
            },
            {
                "date": "2017-05-10",
                "event_name": "NVIDIA Volta V100 announced",
                "event_type": "gpu_launch",
                "impact_area": "training_compute",
                "description": "V100 became a major accelerator for AI training.",
            },
            {
                "date": "2020-05-14",
                "event_name": "NVIDIA Ampere A100 announced",
                "event_type": "gpu_launch",
                "impact_area": "training_compute",
                "description": "A100 became a major cloud AI infrastructure GPU.",
            },
            {
                "date": "2022-11-30",
                "event_name": "ChatGPT launched",
                "event_type": "market_demand",
                "impact_area": "ai_infrastructure_demand",
                "description": "Generative AI accelerated demand for GPU infrastructure.",
            },
            {
                "date": "2023-03-21",
                "event_name": "NVIDIA H100 cloud demand accelerates",
                "event_type": "capacity_pressure",
                "impact_area": "h100_availability",
                "description": "H100 became a high-demand GPU for frontier AI workloads.",
            },
            {
                "date": "2024-03-18",
                "event_name": "NVIDIA Blackwell announced",
                "event_type": "gpu_launch",
                "impact_area": "next_generation_compute",
                "description": "Blackwell introduced the next major AI accelerator generation.",
            },
        ]


def main() -> None:
    importer = HistoricalMarketEventsImporter()
    rows = importer.enrich_rows(importer.fetch_rows())
    errors = validate_rows(rows, importer.category)
    if errors:
        raise ValueError(errors)

    out = importer.run()
    append_provenance(
        source=importer.source_name,
        category=importer.category,
        output_file=str(out),
        row_count=len(rows),
        trust_grade=importer.trust_grade,
    )


if __name__ == "__main__":
    main()
