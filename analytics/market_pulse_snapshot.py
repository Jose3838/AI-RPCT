import json
import os
from pathlib import Path

from api.terminal_core import MARKET_PULSE_HISTORY_FILE, save_market_pulse_snapshot


def main():
    history_file = Path(
        os.environ.get("AIRPCT_MARKET_PULSE_HISTORY_FILE", MARKET_PULSE_HISTORY_FILE)
    )
    result = save_market_pulse_snapshot(history_file=history_file)
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
