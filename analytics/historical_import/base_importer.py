from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


class BaseHistoricalImporter(ABC):
    source_name: str = "unknown"
    category: str = "unknown"
    trust_grade: str = "C"
    output_dir: Path = Path("warehouse/historical/metadata")

    @abstractmethod
    def fetch_rows(self) -> list[dict]:
        raise NotImplementedError

    def enrich_rows(self, rows: list[dict]) -> list[dict]:
        created_at = datetime.now(UTC).isoformat()
        enriched = []

        for row in rows:
            item = dict(row)
            item.setdefault("source", self.source_name)
            item.setdefault("category", self.category)
            item.setdefault("trust_grade", self.trust_grade)
            item.setdefault("created_at", created_at)
            enriched.append(item)

        return enriched

    def output_path(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = self.source_name.lower().replace(" ", "_").replace(".", "")
        return self.output_dir / f"{safe_name}_{self.category}.csv"

    def run(self) -> Path:
        rows = self.enrich_rows(self.fetch_rows())
        df = pd.DataFrame(rows)
        out = self.output_path()
        df.to_csv(out, index=False)
        print(f"{self.__class__.__name__}: wrote {len(df)} rows to {out}")
        return out
