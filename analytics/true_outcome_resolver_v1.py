from __future__ import annotations

from pathlib import Path

import pandas as pd

LABELS = Path("data/true_outcome_labels_v1.csv")
MATURITY = Path("data/outcome_maturity_monitor_v1.csv")
REGIMES = Path("data/market_regime_v1.csv")

OUT = Path("data/true_outcome_labels_resolved_v1.csv")
SUMMARY = Path("data/true_outcome_resolver_summary_v1.csv")
REPORT = Path("reports/true_outcome_resolver_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def as_bool(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    labels = read_csv(LABELS)
    maturity = read_csv(MATURITY)
    regimes = read_csv(REGIMES)

    if labels.empty:
        raise SystemExit("true_outcome_labels_v1.csv missing or empty")

    resolved = labels.copy()

    if not maturity.empty:
        matured = maturity[maturity["window_matured"].apply(as_bool)].copy()
    else:
        matured = pd.DataFrame()

    resolved["resolved_market_regime"] = ""
    resolved["resolution_status"] = "pending_window_maturity"
    resolved["is_trainable"] = False

    resolved_count = 0

    if not matured.empty and not regimes.empty:
        regime_lookup = regimes[["provider", "gpu", "market_regime"]].drop_duplicates()

        candidates = matured.merge(
            regime_lookup,
            on=["provider", "gpu"],
            how="left",
        )

        for _, row in candidates.iterrows():
            mask = (
                (resolved["snapshot_id"] == row.get("snapshot_id"))
                & (resolved["provider"] == row.get("provider"))
                & (resolved["gpu"] == row.get("gpu"))
                & (resolved["window_days"].astype(str) == str(row.get("window_days")))
            )

            regime = str(row.get("market_regime", "")).strip()

            if regime and regime.lower() != "nan":
                resolved.loc[mask, "true_outcome_label"] = regime
                resolved.loc[mask, "resolved_market_regime"] = regime
                resolved.loc[mask, "resolution_status"] = "resolved_from_observed_market_regime"
                resolved.loc[mask, "is_trainable"] = True
                resolved_count += int(mask.sum())

    summary = {
        "input_labels": len(labels),
        "matured_windows": len(matured),
        "resolved_labels": resolved_count,
        "trainable_labels": int(resolved["is_trainable"].apply(as_bool).sum()),
        "status": "ready" if resolved_count > 0 else "waiting_for_mature_windows",
        "next_action": (
            "Rebuild training_dataset_v3 using resolved labels."
            if resolved_count > 0
            else "Continue collecting observations until windows mature."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    resolved.to_csv(OUT, index=False)
    pd.DataFrame([summary]).to_csv(SUMMARY, index=False)

    REPORT.write_text(
        "\n".join([
            "# True Outcome Resolver v1",
            "",
            f"Input labels: {summary['input_labels']}",
            f"Matured windows: {summary['matured_windows']}",
            f"Resolved labels: {summary['resolved_labels']}",
            f"Trainable labels: {summary['trainable_labels']}",
            f"Status: {summary['status']}",
            "",
            "## CTO Assessment",
            "",
            "This resolver turns matured forecast windows into trainable labels only when an observed future market regime is available.",
            "It prevents unresolved or immature windows from entering model training.",
            "",
        ]),
        encoding="utf-8",
    )

    print("TRUE OUTCOME RESOLVER V1")
    print("========================")
    print(pd.DataFrame([summary]))


if __name__ == "__main__":
    main()
