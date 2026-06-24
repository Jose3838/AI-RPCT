from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

gate = pd.read_csv(DATA_DIR / "paid_beta_gate.csv").iloc[-1].to_dict()

blockers = str(gate.get("blockers", "")).split(", ")

actions = {
    "core_not_paid_beta_ready": "Raise core signal quality above paid threshold.",
    "history_not_ready": "Collect clean daily history until 30-day threshold is met.",
    "fallback_provenance_not_paid_safe": "Remove fallback contamination from paid claim paths.",
    "provider_preflight_blocked": "Configure live provider API keys and pass provider preflight.",
    "billing_not_ready": "Enable billing readiness gate and verify usage tracking.",
    "terms_not_ready": "Finalize Terms, Privacy, Trust Center and Beta disclosure.",
    "paid_customers_disabled": "Enable paid customer flag only after live data and legal gates pass.",
}

rows = []
for blocker in blockers:
    blocker = blocker.strip()
    rows.append({
        "blocker": blocker,
        "recommended_action": actions.get(blocker, "Investigate blocker and add remediation action."),
        "status": "open",
        "claim_scope": "research_preview"
    })

df = pd.DataFrame(rows)
df.to_csv(DATA_DIR / "paid_readiness_remediation_plan.csv", index=False)

with open(REPORTS_DIR / "paid_readiness_remediation_plan.md", "w") as f:
    f.write("# AI-RPCT Paid Readiness Remediation Plan\n\n")
    f.write(f"Paid Beta Allowed: {gate.get('paid_beta_allowed')}\n\n")
    f.write("## Open Blockers\n")
    for _, row in df.iterrows():
        f.write(f"- {row['blocker']}: {row['recommended_action']}\n")

print(df)
