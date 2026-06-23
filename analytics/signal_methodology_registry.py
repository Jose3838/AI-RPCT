from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
OUTPUT_FILE = DATA_DIR / "signal_methodology_registry.csv"


SIGNALS = [
    {
        "signal_id": "gpu_scarcity_index",
        "signal_name": "GPU Scarcity Index",
        "product_role": "Measures current supply pressure across price, availability, frontier GPU stress and provider depth.",
        "input_files": "data/gpu_data.csv",
        "formula_summary": "0.35 availability pressure + 0.30 price pressure + 0.25 frontier pressure + 0.10 provider depth pressure",
        "output_file": "data/gpu_scarcity_index.csv",
        "primary_output": "gpu_scarcity_index",
        "trust_gate": "Requires fresh provider data and source-labeled manual snapshots before paid market claims.",
        "moat_value": "Daily scarcity history becomes harder to copy as source-backed observations accumulate.",
        "current_claim_scope": "research_preview",
        "paid_safe_requirement": "30+ clean daily history records, no fallback contamination and enough source-labeled region/provider snapshots.",
    },
    {
        "signal_id": "capacity_shock_forecast",
        "signal_name": "Capacity Shock Forecast",
        "product_role": "Estimates forward-looking infrastructure pressure using RPCT trend, shortage probability, scarcity and shock delta.",
        "input_files": "data/rpct_scores.csv|data/shortage_probability.csv|data/gpu_scarcity_index.csv",
        "formula_summary": "0.40 latest RPCT + 0.25 shortage probability + 0.25 scarcity + 0.10 shock pressure",
        "output_file": "data/forecast_signal.csv",
        "primary_output": "forecast_score",
        "trust_gate": "Requires forecast validation history before customer-facing predictive claims.",
        "moat_value": "Forecast usefulness compounds when predictions can be compared against future observed pressure.",
        "current_claim_scope": "research_preview",
        "paid_safe_requirement": "Measured forecast accuracy, 30+ history days and no unsupported prediction language.",
    },
    {
        "signal_id": "provider_reliability_score",
        "signal_name": "Provider Reliability Score",
        "product_role": "Ranks providers by health, freshness, data depth, availability, price stability, history and rank score.",
        "input_files": "data/provider_health.csv|data/provider_daily_metrics.csv",
        "formula_summary": "0.25 health + 0.20 freshness + 0.10 depth + 0.10 availability + 0.10 price stability + 0.15 history + 0.10 rank",
        "output_file": "data/provider_reliability_ranking.csv",
        "primary_output": "reliability_score",
        "trust_gate": "Requires live provider ingestion or explicit fallback disclosure.",
        "moat_value": "Provider behavior history and fallback/provenance labels create trust that a cloned table lacks.",
        "current_claim_scope": "research_preview",
        "paid_safe_requirement": "Live provider ingestion green, 30+ provider history days and no missing critical credentials.",
    },
    {
        "signal_id": "price_dislocation_signal",
        "signal_name": "Price Dislocation Signal",
        "product_role": "Detects unusually wide cross-provider price spreads for the same GPU.",
        "input_files": "data/gpu_data.csv",
        "formula_summary": "For GPUs with 2+ provider prices, max spread pct = (max price - min price) / median price; score is capped at 100.",
        "output_file": "data/price_dislocation_signal.csv",
        "primary_output": "price_dislocation_score",
        "trust_gate": "Requires source-labeled price observations and persistence checks before paid claims.",
        "moat_value": "Daily spread history can reveal recurring provider mispricing that static price tables miss.",
        "current_claim_scope": "research_preview",
        "paid_safe_requirement": "Source-backed cross-provider observations, 30+ days of spread history and validated recurrence.",
    },
]


def build_signal_methodology_registry():
    return pd.DataFrame(SIGNALS)


def build_signal_methodology_markdown(registry=None):
    registry = registry if registry is not None else build_signal_methodology_registry()
    sections = [
        "# AI-RPCT Signal Methodology Registry",
        "",
        "Every core signal must be explainable, source-aware and gated before paid claims.",
    ]
    for _, row in registry.iterrows():
        sections.extend([
            "",
            f"## {row['signal_name']}",
            f"- Signal ID: {row['signal_id']}",
            f"- Role: {row['product_role']}",
            f"- Inputs: {row['input_files']}",
            f"- Formula: {row['formula_summary']}",
            f"- Output: {row['output_file']} -> {row['primary_output']}",
            f"- Trust Gate: {row['trust_gate']}",
            f"- Moat Value: {row['moat_value']}",
            f"- Claim Scope: {row['current_claim_scope']}",
            f"- Paid-Safe Requirement: {row['paid_safe_requirement']}",
        ])
    return "\n".join(sections)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    registry = build_signal_methodology_registry()
    registry.to_csv(OUTPUT_FILE, index=False)
    (REPORTS_DIR / "signal_methodology_registry.md").write_text(
        build_signal_methodology_markdown(registry)
    )
    print(registry)


if __name__ == "__main__":
    main()
