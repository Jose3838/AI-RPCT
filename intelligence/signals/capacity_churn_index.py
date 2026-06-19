from intelligence.lifecycle.offer_lifecycle import (
    detect_offer_changes
)

def calculate_capacity_churn():

    lifecycle = detect_offer_changes()

    return {
        "capacity_churn":
            lifecycle["new"]
            +
            lifecycle["removed"]
    }
