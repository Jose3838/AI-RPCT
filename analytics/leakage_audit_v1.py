from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path("data/training_dataset_v2.csv")
OUT = Path("data/leakage_audit_v1.csv")
REPORT = Path("reports/leakage_audit_v1.md")


def main() -> None:
    df = pd.read_csv(DATA)

    findings = []

    columns = set(df.columns)

    # Check 1: target existence
    target_exists = "future_market_regime" in columns

    # Check 2: source label present
    source_exists = "market_regime" in columns

    # Check 3: identical target/source
    identical = False
    if target_exists and source_exists:
        identical = (
            df["future_market_regime"].fillna("")
            .astype(str)
            .equals(
                df["market_regime"].fillna("").astype(str)
            )
        )

    findings.append({
        "check": "target_column_present",
        "status": "pass" if target_exists else "fail",
        "details": "future_market_regime exists"
    })

    findings.append({
        "check": "market_regime_feature_present",
        "status": "warning" if source_exists else "pass",
        "details": "market_regime used as feature"
    })

    findings.append({
        "check": "target_equals_feature",
        "status": "fail" if identical else "pass",
        "details": "future_market_regime identical to market_regime"
    })

    leakage_detected = identical

    summary = {
        "audit": "leakage_audit_v1",
        "rows": len(df),
        "leakage_detected": leakage_detected,
        "production_block": leakage_detected,
        "recommendation":
            "Create true future labels before benchmarking."
            if leakage_detected
            else
            "No obvious leakage detected.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.concat(
        [
            pd.DataFrame(findings),
            pd.DataFrame([summary])
        ],
        ignore_index=True,
        sort=False
    ).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Leakage Audit v1",
                "",
                f"Rows audited: {len(df)}",
                f"Leakage detected: {leakage_detected}",
                "",
                "## CTO Assessment",
                "",
                "Perfect ML scores require verification before being accepted.",
                "If the prediction target is derived from an input feature, all benchmark claims are invalid.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("LEAKAGE AUDIT V1")
    print("================")
    print(pd.DataFrame(findings))
    print()
    print(pd.DataFrame([summary]))


if __name__ == "__main__":
    main()
