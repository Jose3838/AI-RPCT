from __future__ import annotations

from pathlib import Path

from historical_import.base_importer import BaseHistoricalImporter
from historical_import.provenance import append_provenance
from historical_import.validators import validate_rows


class HistoricalCloudGpuInstancesImporter(BaseHistoricalImporter):
    source_name = "Cloud GPU Instances"
    category = "provider_pricing"
    trust_grade = "A"
    output_dir = Path("warehouse/historical/provider_pricing")

    def fetch_rows(self) -> list[dict]:
        return [
            {"date": "2017-01-01", "provider": "AWS", "gpu": "K80", "instance": "p2", "price_per_hour": 0, "region": "global"},
            {"date": "2017-10-01", "provider": "AWS", "gpu": "V100", "instance": "p3", "price_per_hour": 0, "region": "global"},
            {"date": "2020-11-01", "provider": "AWS", "gpu": "A100", "instance": "p4d", "price_per_hour": 0, "region": "global"},
            {"date": "2023-09-01", "provider": "AWS", "gpu": "H100", "instance": "p5", "price_per_hour": 0, "region": "global"},
            {"date": "2017-01-01", "provider": "Azure", "gpu": "K80", "instance": "NC", "price_per_hour": 0, "region": "global"},
            {"date": "2018-01-01", "provider": "Azure", "gpu": "V100", "instance": "NCv3", "price_per_hour": 0, "region": "global"},
            {"date": "2020-01-01", "provider": "Azure", "gpu": "A100", "instance": "ND A100 v4", "price_per_hour": 0, "region": "global"},
            {"date": "2023-01-01", "provider": "Azure", "gpu": "H100", "instance": "ND H100 v5", "price_per_hour": 0, "region": "global"},
            {"date": "2017-01-01", "provider": "Google Cloud", "gpu": "K80", "instance": "k80", "price_per_hour": 0, "region": "global"},
            {"date": "2018-01-01", "provider": "Google Cloud", "gpu": "V100", "instance": "v100", "price_per_hour": 0, "region": "global"},
            {"date": "2021-01-01", "provider": "Google Cloud", "gpu": "A100", "instance": "a2", "price_per_hour": 0, "region": "global"},
            {"date": "2023-01-01", "provider": "Google Cloud", "gpu": "H100", "instance": "a3", "price_per_hour": 0, "region": "global"},
        ]


def main() -> None:
    importer = HistoricalCloudGpuInstancesImporter()
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
