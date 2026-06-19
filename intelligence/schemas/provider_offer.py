from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any

@dataclass
class ProviderOffer:
    provider: str
    gpu_model: str
    region: Optional[str]
    price_usd_per_gpu_hour: Optional[float]
    available: Optional[bool]
    source: str
    mode: str  # live | demo | error
    raw: Dict[str, Any]
    observed_at: str

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return asdict(self)
