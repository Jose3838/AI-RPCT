from intelligence.history.offer_fingerprint import build_offer_fingerprint
from intelligence.schemas.provider_offer import ProviderOffer


def normalize_legacy_provider_result(result):
    provider = result.get("provider")
    gpu_model = result.get("gpu_type") or result.get("gpu_model") or "unknown"
    region = result.get("region") or "global"
    price = result.get("price_per_hour") or result.get("price_usd_per_gpu_hour")
    capacity = result.get("available_capacity")

    available = True
    if capacity is not None:
        available = capacity > 0

    offer = ProviderOffer(
        provider=provider,
        gpu_model=gpu_model,
        region=region,
        price_usd_per_gpu_hour=price,
        available=available,
        source=result.get("source", "unknown"),
        mode="live" if "live_api" in result.get("source", "") else "demo",
        raw=result,
        observed_at=ProviderOffer.now_iso(),
    ).to_dict()

    offer["fingerprint"] = build_offer_fingerprint(
        provider=provider,
        gpu_model=gpu_model,
        region=region,
        price=price,
    )

    return [offer]


def normalize_provider_result(result):
    if "offers" in result:
        offers = result.get("offers") or []
        normalized = []

        for offer in offers:
            if "fingerprint" not in offer:
                offer["fingerprint"] = build_offer_fingerprint(
                    provider=offer.get("provider"),
                    gpu_model=offer.get("gpu_model"),
                    region=offer.get("region"),
                    price=offer.get("price_usd_per_gpu_hour"),
                )

            normalized.append(offer)

        return normalized

    return normalize_legacy_provider_result(result)
