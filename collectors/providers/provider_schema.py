from dataclasses import dataclass

@dataclass
class ProviderSnapshot:
    provider: str
    live: bool
    gpu_count: int
    avg_price: float
    market_share_pct: float
    health_score: float
