from intelligence.events.provider_expansion_detector import (
    detect_provider_expansion
)

def provider_expansion_forecast():

    events = detect_provider_expansion()

    providers = sorted(
        set(
            e.get("provider")
            for e in events
            if e.get("provider")
        )
    )

    return {
        "expansion_events": len(events),
        "expanding_providers": providers,
        "signal": (
            "provider_expansion_detected"
            if events
            else "no_expansion_detected"
        )
    }
