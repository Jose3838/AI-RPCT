import pandas as pd
from pathlib import Path

path = Path("data/user_feedback.csv")

if path.exists():
    df = pd.read_csv(path)
    feedback_count = len(df)
else:
    feedback_count = 0

out = pd.DataFrame([{
    "feedback_count": feedback_count,
    "status": "collecting" if feedback_count > 0 else "no_feedback_yet"
}])

out.to_csv("data/feedback_summary.csv", index=False)

print(out)
