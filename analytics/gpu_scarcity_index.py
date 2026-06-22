from pathlib import Path

import pandas as pd


FRONTIER_GPUS = {"H100", "H200", "B200", "GB200", "A100"}


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, float(value)))


def component_band(score):
    if score >= 75:
        return "high"
    if score >= 50:
        return "elevated"
    if score >= 25:
        return "watch"
    return "stable"


def latest_snapshot(gpu):
    gpu = gpu.copy()
    if "timestamp" not in gpu.columns:
        return gpu

    gpu["timestamp"] = pd.to_datetime(gpu["timestamp"], errors="coerce")
    latest_timestamp = gpu["timestamp"].max()
    if pd.isna(latest_timestamp):
        return gpu
    return gpu[gpu["timestamp"] == latest_timestamp].copy()


def build_gpu_scarcity_index(gpu):
    snapshot = latest_snapshot(gpu)
    if snapshot.empty:
        return pd.DataFrame([{
            "gpu_scarcity_index": 0,
            "scarcity_band": "unknown",
            "avg_price_per_hour": 0,
            "avg_availability": 0,
            "price_pressure_score": 0,
            "availability_pressure_score": 0,
            "frontier_pressure_score": 0,
            "provider_depth_score": 100,
            "provider_count": 0,
            "gpu_count": 0,
        }])

    snapshot["price_per_hour"] = pd.to_numeric(snapshot["price_per_hour"], errors="coerce").fillna(0)
    snapshot["availability"] = pd.to_numeric(snapshot["availability"], errors="coerce").fillna(0)

    avg_price = snapshot["price_per_hour"].mean()
    avg_availability = snapshot["availability"].mean()
    provider_count = snapshot["provider"].nunique() if "provider" in snapshot.columns else 0
    gpu_count = snapshot["gpu"].nunique() if "gpu" in snapshot.columns else len(snapshot)

    frontier = snapshot[
        snapshot["gpu"].astype(str).str.upper().isin(FRONTIER_GPUS)
    ] if "gpu" in snapshot.columns else pd.DataFrame()

    price_pressure = clamp(((avg_price - 0.75) / 2.75) * 100)
    availability_pressure = clamp(((2500 - avg_availability) / 2500) * 100)
    provider_depth_pressure = clamp(((3 - provider_count) / 3) * 100)

    if frontier.empty:
        frontier_pressure = 50.0
    else:
        frontier_price = frontier["price_per_hour"].mean()
        frontier_availability = frontier["availability"].mean()
        frontier_price_pressure = clamp(((frontier_price - 1.0) / 3.0) * 100)
        frontier_availability_pressure = clamp(((2000 - frontier_availability) / 2000) * 100)
        frontier_pressure = (frontier_price_pressure * 0.45) + (frontier_availability_pressure * 0.55)

    scarcity_score = round(clamp(
        (availability_pressure * 0.35)
        + (price_pressure * 0.30)
        + (frontier_pressure * 0.25)
        + (provider_depth_pressure * 0.10)
    ), 2)

    return pd.DataFrame([{
        "gpu_scarcity_index": scarcity_score,
        "scarcity_band": component_band(scarcity_score),
        "avg_price_per_hour": round(avg_price, 4),
        "avg_availability": round(avg_availability, 2),
        "price_pressure_score": round(price_pressure, 2),
        "availability_pressure_score": round(availability_pressure, 2),
        "frontier_pressure_score": round(frontier_pressure, 2),
        "provider_depth_score": round(100 - provider_depth_pressure, 2),
        "provider_count": int(provider_count),
        "gpu_count": int(gpu_count),
    }])


def main():
    gpu = pd.read_csv("data/gpu_data.csv")
    result = build_gpu_scarcity_index(gpu)
    Path("data").mkdir(exist_ok=True)
    result.to_csv("data/gpu_scarcity_index.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
