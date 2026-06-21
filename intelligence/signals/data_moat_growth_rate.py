import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def data_moat_growth_rate():

    df = pd.read_csv(FILE)

    return {
        "historical_observations":
            int(len(df))
    }
