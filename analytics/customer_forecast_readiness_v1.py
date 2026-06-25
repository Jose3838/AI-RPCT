from __future__ import annotations

from pathlib import Path

import pandas as pd

SELECTOR = Path("data/production_forecast_model_v1.csv")

OUT = Path("data/customer_forecast_readiness_v1.csv")
REPORT = Path("reports/customer_forecast_readiness_v1.md")


def main() -> None:
    if not SELECTOR.exists():
        raise SystemExit("production_forecast_model_v1.csv missing")

    selector = pd.read_csv(SELECTOR).iloc[0]

    production_status = str(selector["production_status"])

    if production_status == "production_ready":
        preview_ready = True
        paid_ready = True
        maturity = "production"
        allowed_claim = "Production-ready AI forecast engine."
        blocked_claim = ""
    elif production_status == "watch":
        preview_ready = True
        paid_ready = False
        maturity = "pilot"
        allowed_claim = (
            "Early directional forecast preview based on historical and live infrastructure signals."
        )
        blocked_claim = (
            "Do not claim validated predictive AI or guaranteed forecasting performance."
        )
    else:
        preview_ready = False
        paid_ready = False
        maturity = "research"
        allowed_claim = "Internal research only."
        blocked_claim = "No customer-facing forecasting claims."

    row = {
        "selected_model": selector["selected_model"],
        "production_status": production_status,
        "customer_preview_ready": preview_ready,
        "paid_production_ready": paid_ready,
        "product_maturity": maturity,
        "allowed_claim": allowed_claim,
        "blocked_claim": blocked_claim,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Customer Forecast Readiness v1",
                "",
                f"Selected model: {row['selected_model']}",
                f"Production status: {production_status}",
                f"Product maturity: {maturity}",
                "",
                f"Customer preview ready: {preview_ready}",
                f"Paid production ready: {paid_ready}",
                "",
                "## Allowed Claim",
                "",
                allowed_claim,
                "",
                "## Blocked Claim",
                "",
                blocked_claim,
                "",
                "## CTO Assessment",
                "",
                "The forecasting capability is suitable for customer demonstrations and preview reports.",
                "Commercial production claims remain blocked until broader validation data is available.",
            ]
        ),
        encoding="utf-8",
    )

    print("CUSTOMER FORECAST READINESS V1")
    print("==============================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
