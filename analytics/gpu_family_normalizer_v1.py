from __future__ import annotations

from pathlib import Path

import pandas as pd

TRAINING = Path("data/training_dataset_v1.csv")
FEATURE_STORE = Path("data/feature_store_v1.csv")

OUT_TRAINING = Path("data/training_dataset_family_v1.csv")
OUT_FEATURES = Path("data/feature_store_family_v1.csv")
REPORT = Path("reports/gpu_family_normalizer_v1.md")


def gpu_family(gpu: str) -> str:
    name = str(gpu).upper()

    if "B300" in name:
        return "B300_family"
    if "GB200" in name:
        return "GB200_family"
    if "B200" in name:
        return "B200_family"
    if "H200" in name:
        return "H200_family"
    if "H100" in name:
        return "H100_family"
    if "A100" in name or "A800" in name:
        return "A100_family"
    if "L40" in name or "L40S" in name:
        return "L40_family"
    if "L4" in name:
        return "L4_family"
    if "RTX 5090" in name or "RTX 5080" in name or "RTX 5070" in name or "RTX 5060" in name:
        return "RTX50_family"
    if "RTX 4090" in name or "RTX 4080" in name or "RTX 4070" in name or "RTX 4060" in name:
        return "RTX40_family"
    if "RTX 3090" in name or "RTX 3080" in name or "RTX 3070" in name:
        return "RTX30_family"
    if "RTX A" in name or "A6000" in name or "A5000" in name or "A4000" in name:
        return "RTX_A_family"
    if "V100" in name or "K80" in name or "TESLA" in name:
        return "legacy_datacenter_family"
    if "MI300" in name:
        return "AMD_MI300_family"
    if name in {"UNKNOWN", "", "NAN"}:
        return "unknown_family"

    return "other_gpu_family"


def enrich(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()

    df = pd.read_csv(path)

    if "gpu" not in df.columns:
        df["gpu"] = "unknown"

    df["gpu_family"] = df["gpu"].apply(gpu_family)
    return df


def main() -> None:
    training = enrich(TRAINING)
    features = enrich(FEATURE_STORE)

    OUT_TRAINING.parent.mkdir(parents=True, exist_ok=True)
    OUT_FEATURES.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    training.to_csv(OUT_TRAINING, index=False)
    features.to_csv(OUT_FEATURES, index=False)

    family_count = training["gpu_family"].nunique() if not training.empty else 0
    gpu_count = training["gpu"].nunique() if not training.empty else 0

    REPORT.write_text(
        "\n".join(
            [
                "# GPU Family Normalizer v1",
                "",
                f"Training rows: {len(training)}",
                f"Feature rows: {len(features)}",
                f"Unique GPUs: {gpu_count}",
                f"GPU families: {family_count}",
                "",
                "## CTO Assessment",
                "",
                "GPU family normalization reduces overfitting caused by sparse individual GPU variants.",
                "Future training pipelines should use gpu_family alongside raw gpu names.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("GPU FAMILY NORMALIZER V1")
    print("========================")
    print(f"Training rows: {len(training)}")
    print(f"Feature rows : {len(features)}")
    print(f"GPU families : {family_count}")
    print(f"CSV training : {OUT_TRAINING}")
    print(f"CSV features : {OUT_FEATURES}")


if __name__ == "__main__":
    main()
