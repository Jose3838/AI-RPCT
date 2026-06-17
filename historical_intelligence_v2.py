from historical_windows import (
    get_7_day_window,
    get_30_day_window,
    get_90_day_window
)


def summarize_window(window):
    if window["status"] != "ok":
        return window

    data = window["data"]

    if len(data) < 2:
        return {
            "status": "insufficient_history"
        }

    first = data[0]
    last = data[-1]

    return {
        "records": len(data),
        "coverage_change":
            round(
                float(last["coverage"])
                -
                float(first["coverage"]),
                2
            ),
        "market_strength_change":
            round(
                float(last["market_strength"])
                -
                float(first["market_strength"]),
                2
            ),
        "activation_change":
            round(
                float(last["avg_activation_score"])
                -
                float(first["avg_activation_score"]),
                2
            )
    }


def build_historical_intelligence_v2():

    return {
        "status": "ok",
        "version": "v2",
        "seven_day":
            summarize_window(
                get_7_day_window()
            ),
        "thirty_day":
            summarize_window(
                get_30_day_window()
            ),
        "ninety_day":
            summarize_window(
                get_90_day_window()
            )
    }
