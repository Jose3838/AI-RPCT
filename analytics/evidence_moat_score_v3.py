from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
REPORT_DIR = Path("reports")

OUT_CSV = DATA_DIR / "evidence_moat_score_v3.csv"
OUT_REPORT = REPORT_DIR / "evidence_moat_score_v3.md"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def score_provider_readiness() -> tuple[float, str]:
    df = read_csv(DATA_DIR / "provider_preflight.csv")
    if df.empty:
        return 0.0, "no_provider_preflight"

    ready_count = int((df["readiness"] == "ready").sum())
    total = len(df)
    score = round((ready_count / total) * 100, 2) if total else 0.0
    return score, f"{ready_count}/{total} providers ready"


def score_history_depth() -> tuple[float, str]:
    df = read_csv(DATA_DIR / "historical_moat_audit.csv")
    if df.empty:
        return 0.0, "no_historical_moat_audit"

    score = round(float(df["history_depth_score"].mean()), 2)
    return score, f"avg history depth score={score}"


def score_free_source_coverage() -> tuple[float, str]:
    df = read_csv(DATA_DIR / "free_source_audit.csv")
    if df.empty:
        return 0.0, "no_free_source_audit"

    if "evidence_ready" not in df.columns:
        return 50.0, "free sources present but evidence_ready missing"

    ready = df["evidence_ready"].astype(str).str.lower().isin(["true", "1", "yes"]).sum()
    total = len(df)
    score = round((ready / total) * 100, 2) if total else 0.0
    return score, f"{ready}/{total} free sources evidence-ready"


def score_coverage_gap_pressure() -> tuple[float, str]:
    path = DATA_DIR / "coverage_gap_priority.csv"
    df = read_csv(path)

    if df.empty:
        return 50.0, "coverage_gap_priority missing; neutral score"

    open_gaps = len(df)
    if open_gaps == 0:
        return 100.0, "no open coverage gaps"

    score = max(0.0, 100.0 - min(open_gaps * 5.0, 100.0))
    return round(score, 2), f"{open_gaps} open coverage gaps"


def classify(score: float) -> str:
    if score >= 85:
        return "strong_evidence_moat"
    if score >= 70:
        return "emerging_strong_moat"
    if score >= 50:
        return "developing_evidence_moat"
    if score >= 30:
        return "thin_evidence_moat"
    return "weak_evidence_moat"


def main() -> None:
    provider_score, provider_note = score_provider_readiness()
    history_score, history_note = score_history_depth()
    free_source_score, free_source_note = score_free_source_coverage()
    coverage_gap_score, coverage_gap_note = score_coverage_gap_pressure()

    weights = {
        "provider_readiness": 0.30,
        "history_depth": 0.30,
        "free_source_coverage": 0.25,
        "coverage_gap_pressure": 0.15,
    }

    total_score = round(
        provider_score * weights["provider_readiness"]
        + history_score * weights["history_depth"]
        + free_source_score * weights["free_source_coverage"]
        + coverage_gap_score * weights["coverage_gap_pressure"],
        2,
    )

    status = classify(total_score)

    rows = [
        {
            "metric": "provider_readiness",
            "score": provider_score,
            "weight": weights["provider_readiness"],
            "note": provider_note,
        },
        {
            "metric": "history_depth",
            "score": history_score,
            "weight": weights["history_depth"],
            "note": history_note,
        },
        {
            "metric": "free_source_coverage",
            "score": free_source_score,
            "weight": weights["free_source_coverage"],
            "note": free_source_note,
        },
        {
            "metric": "coverage_gap_pressure",
            "score": coverage_gap_score,
            "weight": weights["coverage_gap_pressure"],
            "note": coverage_gap_note,
        },
        {
            "metric": "total",
            "score": total_score,
            "weight": 1.0,
            "note": status,
        },
    ]

    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)

    OUT_REPORT.write_text(
        "\n".join(
            [
                "# Evidence Moat Score v3",
                "",
                f"Total score: {total_score}",
                f"Status: {status}",
                "",
                "## Inputs",
                "",
                f"- Provider readiness: {provider_score} — {provider_note}",
                f"- History depth: {history_score} — {history_note}",
                f"- Free source coverage: {free_source_score} — {free_source_note}",
                f"- Coverage gap pressure: {coverage_gap_score} — {coverage_gap_note}",
                "",
                "## CTO Assessment",
                "",
                "Evidence Moat v3 now includes live provider readiness, historical depth, free-source evidence readiness, and coverage gap pressure.",
                "The next moat unlock is sustained 30-day live history continuity.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("EVIDENCE MOAT SCORE V3")
    print("======================")
    print(f"Score: {total_score}")
    print(f"Status: {status}")
    print(f"CSV: {OUT_CSV}")
    print(f"Report: {OUT_REPORT}")


if __name__ == "__main__":
    main()
