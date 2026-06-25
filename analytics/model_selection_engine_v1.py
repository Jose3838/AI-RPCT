from __future__ import annotations

from pathlib import Path

import pandas as pd

REGISTRY = Path("data/model_performance_registry_v1.csv")
OUT = Path("data/model_selection_v1.csv")
REPORT = Path("reports/model_selection_v1.md")


def main() -> None:
    if not REGISTRY.exists() or REGISTRY.stat().st_size <= 1:
        raise SystemExit("model_performance_registry_v1.csv missing or empty")

    df = pd.read_csv(REGISTRY)

    df["directional_accuracy"] = pd.to_numeric(
        df["directional_accuracy"], errors="coerce"
    ).fillna(0)

    best = df.sort_values(
        by=["directional_accuracy", "forecast_rows"],
        ascending=[False, False],
    ).iloc[0]

    result = pd.DataFrame(
        [
            {
                "selected_model": best["model_name"],
                "model_version": best["model_version"],
                "directional_accuracy": best["directional_accuracy"],
                "forecast_rows": best["forecast_rows"],
                "selection_reason": "highest_directional_accuracy",
                "status": "production_candidate",
            }
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Model Selection Engine v1",
                "",
                f"Selected model: {best['model_name']}",
                f"Version: {best['model_version']}",
                f"Directional accuracy: {best['directional_accuracy']}",
                "",
                "## Selection Strategy",
                "",
                "- Highest directional accuracy",
                "- Highest forecast coverage",
                "",
                "## Future Improvements",
                "",
                "- Rolling 30-day accuracy",
                "- Provider-specific champions",
                "- GPU-family champions",
                "- Automatic champion/challenger evaluation",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("MODEL SELECTION ENGINE V1")
    print("=========================")
    print(result)


if __name__ == "__main__":
    main()
