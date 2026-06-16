import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path

symbols = {
    "NVDA": "NVDA",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "AKT": "AKT-USD",
}

Path("data").mkdir(exist_ok=True)
file_path = "data/market_data.csv"

rows = []

print("Collecting market data...\n")

for name, ticker in symbols.items():
    try:
        hist = yf.download(ticker, period="5d", interval="1d", auto_adjust=True, progress=False)

        if hist.empty:
            print(f"{name}: no data")
            continue

        close_data = hist["Close"].dropna()
        price = close_data.iloc[-1, 0] if hasattr(close_data, "columns") else close_data.iloc[-1]
        price = float(price)

        rows.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "asset": name,
            "ticker": ticker,
            "price": price
        })

        print(f"{name} | ${price:.4f}")

    except Exception as e:
        print(f"{name}: error - {e}")

new_data = pd.DataFrame(rows)

if Path(file_path).exists():
    old_data = pd.read_csv(file_path)
    final_data = pd.concat([old_data, new_data], ignore_index=True)
else:
    final_data = new_data

final_data.to_csv(file_path, index=False)

print("\nSaved to data/market_data.csv")
