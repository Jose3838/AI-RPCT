from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path("data/training_dataset_v2.csv")
GB = Path("data/gradient_boosting_model_v1.csv")

OUT = Path("data/leakage_audit_v2.csv")
REPORT = Path("reports/leakage_audit_v2.md")


TARGET = "future_market_regime"

SUSPICIOUS_FEATURES = [
    "market_regime",
    "forecast_signal",
    "forecast_score",
]


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    df = read(DATA)
    gb = read(GB)

    if df.empty:
        raise SystemExit("training_dataset_v2.csv missing or empty")

    findings = []

    target_exists = TARGET in df.columns

    findings.append({
        "check": "target_column_present",
        "status": "pass" if target_exists else "fail",
        "details": f"{TARGET} exists={target_exists}",
    })

    if not target_exists:
        leakage_detected = True
        production_block = True
        recommendation = "Create true future outcome labels before training."
    else:
        leakage_detected = False
        production_block = False
        recommendation = "No hard leakage detected, but warnings must be reviewed."

        for feature in SUSPICIOUS_FEATURES:
            exists = feature in df.columns
            findings.append({
                "check": f"suspicious_feature_{feature}",
                "status": "warning" if exists else "pass",
                "details": f"{feature} exists={exists}",
            })

        if "market_regime" in df.columns:
            identical = (
                df[TARGET].fillna("").astype(str)
                == df["market_regime"].fillna("").astype(str)
            ).all()

            findings.append({
                "check": "target_equals_market_regime",
                "status": "fail" if identical else "pass",
                "details": f"all_rows_identical={identical}",
            })

            if identical:
                leakage_detected = True
                production_block = True
                recommendation = "Target is identical to market_regime; rebuild labels from future observations."

        if "forecast_signal" in df.columns:
            overlap = (
                df[TARGET].fillna("").astype(str)
                == df["forecast_signal"].fillna("").astype(str)
            ).mean()

            findings.append({
                "check": "target_forecast_signal_overlap",
                "status": "warning" if overlap > 0.5 else "pass",
                "details": f"overlap_ratio={round(float(overlap), 4)}",
            })

        if not gb.empty and "prediction_correct" in gb.columns:
            split_scores = (
                gb.groupby("evaluation_split")["prediction_correct"]
                .mean()
                .mul(100)
                .round(2)
                .to_dict()
            )

            perfect_all = all(float(v) >= 99.99 for v in split_scores.values())

            findings.append({
                "check": "perfect_model_scores",
                "status": "warning" if perfect_all else "pass",
                "details": str(split_scores),
            })

            if perfect_all and not leakage_detected:
                recommendation = "Perfect scores detected; require true future-label validation before production claims."

    summary = {
        "check": "summary",
        "status": "fail" if production_block else "warning",
        "details": recommendation,
        "leakage_detected": leakage_detected,
        "production_block": production_block,
        "recommendation": recommendation,
    }

    out = pd.concat(
        [
            pd.DataFrame(findings),
            pd.DataFrame([summary]),
        ],
        ignore_index=True,
        sort=False,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Leakage Audit v2",
            "",
            f"Rows audited: {len(df)}",
            f"Leakage detected: {leakage_detected}",
            f"Production block: {production_block}",
            "",
            "## Recommendation",
            "",
            recommendation,
            "",
            "## CTO Assessment",
            "",
            "Leakage Audit v2 fixes the v1 target-column status bug and adds checks for suspicious target-adjacent features and perfect model scores.",
            "Any perfect ML benchmark must be treated as provisional until true future outcome labels exist.",
            "",
        ]),
        encoding="utf-8",
    )

    print("LEAKAGE AUDIT V2")
    print("================")
    print(out)


if __name__ == "__main__":
    main()
