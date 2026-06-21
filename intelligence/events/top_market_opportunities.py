from intelligence.forecast.gpu_opportunity_score import (
    gpu_opportunity_score
)

def top_market_opportunities():

    return (
        gpu_opportunity_score()
    )[:10]
