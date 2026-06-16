import pandas as pd
from pathlib import Path
from datetime import datetime

current = pd.read_csv(
    "data/ai_infrastructure_index.csv"
)

current["date"] = datetime.now().strftime("%Y-%m-%d")

history_file = "data/ai_infrastructure_index_history.csv"

if Path(history_file).exists():
    history = pd.read_csv(history_file)
    out = pd.concat(
        [history, current],
        ignore_index=True
    )
else:
    out = current

out.to_csv(
    history_file,
    index=False
)

print(out.tail())
