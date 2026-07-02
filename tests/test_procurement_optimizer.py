from copilot.procurement_optimizer import get_procurement_optimizer


def test_returns_ok_status_with_real_data():
    result = get_procurement_optimizer()
    assert result["status"] == "ok"
    assert result["gpu"] == "NVIDIA H100"


def test_purchase_price_is_a_real_registry_anchor():
    result = get_procurement_optimizer()
    assert result["on_prem_purchase_price_usd"] == 30000.0
    assert result["on_prem_price_confidence"] == "partial"


def test_cloud_comparisons_cover_all_six_providers():
    result = get_procurement_optimizer()
    assert len(result["cloud_comparisons"]) == 6

    provider_names = {c["provider_name"] for c in result["cloud_comparisons"]}
    assert provider_names == {
        "Amazon Web Services", "Google Cloud", "Microsoft Azure",
        "CoreWeave", "Lambda", "RunPod",
    }


def test_comparisons_sorted_cheapest_first():
    result = get_procurement_optimizer()
    prices = [c["cloud_price_usd_per_gpu_hour"] for c in result["cloud_comparisons"]]
    assert prices == sorted(prices)


def test_breakeven_math_is_correct():
    result = get_procurement_optimizer()
    purchase_price = result["on_prem_purchase_price_usd"]

    for comparison in result["cloud_comparisons"]:
        expected_hours = purchase_price / comparison["cloud_price_usd_per_gpu_hour"]
        assert abs(comparison["breakeven_hours"] - expected_hours) < 0.5

        expected_months_full_time = expected_hours / 730
        assert abs(
            comparison["breakeven_months_full_time_utilization"] - expected_months_full_time
        ) < 0.1


def test_cheapest_option_is_the_lowest_hourly_rate():
    result = get_procurement_optimizer()
    cheapest = min(
        result["cloud_comparisons"], key=lambda c: c["cloud_price_usd_per_gpu_hour"]
    )
    assert result["cheapest_cloud_option"]["provider_name"] == cheapest["provider_name"]


def test_caveats_disclose_known_limitations():
    # This must never look more precise/authoritative than it is: no
    # power/cooling/staffing costs modeled, purchase price is an
    # estimate, cloud rates are a single-day snapshot.
    result = get_procurement_optimizer()
    caveats_text = " ".join(result["caveats"]).lower()
    assert "power" in caveats_text or "cooling" in caveats_text
    assert "estimate" in caveats_text
    assert "snapshot" in caveats_text
