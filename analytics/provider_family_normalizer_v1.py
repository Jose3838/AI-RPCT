from __future__ import annotations

from pathlib import Path

import pandas as pd

TRAINING = Path("data/training_dataset_family_v1.csv")
FEATURES = Path("data/feature_store_family_v1.csv")

OUT_TRAINING = Path("data/training_dataset_family_provider_v1.csv")
OUT_FEATURES = Path("data/feature_store_family_provider_v1.csv")
REPORT = Path("reports/provider_family_normalizer_v1.md")


def provider_family(provider: str) -> str:
    name = str(provider).strip().lower()

    if name in {"aws", "amazon", "amazon web services"}:
        return "hyperscaler_family"
    if name in {"azure", "microsoft azure"}:
        return "hyperscaler_family"
    if name in {"gcp", "google cloud", "google"}:
        return "hyperscaler_family"

    if "runpod" in name:
        return "gpu_marketplace_family"
    if "vast" in name:
        return "gpu_marketplace_family"

    if name in {"coreweave", "lambda", "lambda labs", "crusoe", "nebius"}:
        return "specialized_gpu_cloud_family"

    if name in {"unknown", "", "nan"}:
        return "unknown_provider_family"

    return "other_provider_family"


def enrich(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()

    df = pd.read_csv(path)

    if "provider" not in df.columns:
        df["provider"] = "unknown"

    df["provider_family"] = df["provider"].apply(provider_family)
    return df


def main() -> None:
    training = enrich(TRAINING)
    features = enrich(FEATURES)

    OUT_TRAINING.parent.mkdir(parents=True, exist_ok=True)
    OUT_FEATURES.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    training.to_csv(OUT_TRAINING, index=False)
    features.to_csv(OUT_FEATURES, index=False)

    training_provider_count = training["provider"].nunique() if not training.empty else 0
    training_family_count = training["provider_family"].nunique() if not training.empty else 0

    REPORT.write_text(
        "\n".join(
            [
                "# Provider Family Normalizer v1",
                "",
                f"Training rows: {len(training)}",
                f"Feature rows: {len(features)}",
                f"Providers: {training_provider_count}",
                f"Provider families: {training_family_count}",
                "",
                "## Families",
                "",
                "- hyperscaler_family",
                "- gpu_marketplace_family",
                "- specialized_gpu_cloud_family",
                "- other_provider_family",
                "- unknown_provider_family",
                "",
                "## CTO Assessment",
                "",
                "Provider family normalization allows models to transfer learnings between structurally similar infrastructure providers.",
                "This is required before building stronger ML models on sparse provider/GPU observations.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("PROVIDER FAMILY NORMALIZER V1")
    print("=============================")
    print(f"Training rows: {len(training)}")
    print(f"Feature rows : {len(features)}")
    print(f"Provider families: {training_family_count}")
    print(f"CSV training : {OUT_TRAINING}")
    print(f"CSV features : {OUT_FEATURES}")


if __name__ == "__main__":
    main()
