from intelligence.signals.new_gpu_detector import detect_new_gpu_entries
from intelligence.events.provider_expansion_detector import detect_provider_expansion

def build_market_event_feed():

    events = []

    for gpu in detect_new_gpu_entries():
        events.append({
            "type": "new_gpu_detected",
            "gpu": gpu
        })

    events.extend(
        detect_provider_expansion()
    )

    return events
