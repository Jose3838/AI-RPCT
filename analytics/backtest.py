import pandas as pd

def classify(score):
    if score >= 80:
        return "HIGH"
    if score >= 60:
        return "MEDIUM"
    return "LOW"

if __name__ == "__main__":
    scores = pd.read_csv("data/rpct_scores.csv")
    scores["risk_bucket"] = scores["score"].apply(classify)
    scores.to_csv("data/backtest_results.csv", index=False)
    print(scores.tail(10))
