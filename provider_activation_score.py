def calculate_provider_activation_score(
    price_score,
    capacity_score,
    health_score,
    momentum_score
):

    score = (
        price_score * 0.40
        + capacity_score * 0.30
        + health_score * 0.20
        + momentum_score * 0.10
    )

    score = round(score, 2)

    if score >= 85:
        grade = "A+"
        status = "hyper_growth"

    elif score >= 75:
        grade = "A"
        status = "high_growth"

    elif score >= 65:
        grade = "B"
        status = "stable_growth"

    elif score >= 50:
        grade = "C"
        status = "neutral"

    else:
        grade = "D"
        status = "declining"

    return {
        "activation_score": score,
        "grade": grade,
        "status": status
    }
