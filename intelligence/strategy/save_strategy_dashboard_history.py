import csv
from datetime import datetime, timezone
from pathlib import Path

FILE = Path("data/strategy_dashboard_history.csv")


def save_strategy_dashboard_history(strategy):
    FILE.parent.mkdir(parents=True, exist_ok=True)

    exists = FILE.exists()

    scores = strategy.get("scores", {})
    health = strategy.get("health", {})

    with FILE.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "stage",
                "product_readiness",
                "executive_score",
                "investor_readiness",
                "data_moat",
                "collection",
                "launchagent_installed"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            strategy.get("stage"),
            scores.get("product_readiness"),
            scores.get("executive_score"),
            scores.get("investor_readiness"),
            scores.get("data_moat"),
            health.get("collection"),
            health.get("launchagent_installed")
        ])

    return {
        "status": "saved",
        "file": str(FILE)
    }
