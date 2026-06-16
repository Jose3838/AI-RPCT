import pandas as pd

value_props = [
    {
        "customer": "AI Startup",
        "value": "Forecast compute cost increases and GPU shortages"
    },
    {
        "customer": "Hedge Fund",
        "value": "Track AI infrastructure stress before markets price it in"
    },
    {
        "customer": "GPU Provider",
        "value": "Benchmark supply pressure and competitor positioning"
    },
    {
        "customer": "Crypto Fund",
        "value": "Monitor AI-token infrastructure demand and GPU scarcity"
    }
]

df = pd.DataFrame(value_props)
df.to_csv("data/customer_value.csv", index=False)

print(df)
