from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2
from provider_momentum_history import save_provider_momentum_snapshot


def run_intelligence_snapshot_v3():
    base_snapshot = run_intelligence_snapshot_v2()
    momentum_snapshot = save_provider_momentum_snapshot()

    return {
        "status": "ok",
        "version": "v3",
        "base_snapshot": base_snapshot,
        "provider_momentum_snapshot": momentum_snapshot
    }
