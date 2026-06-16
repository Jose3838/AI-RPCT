import pandas as pd

def predict_next(scores):
    if len(scores) < 2:
        return None

    trend = scores.iloc[-1] - scores.iloc[-2]

    return scores.iloc[-1] + trend

if __name__ == "__main__":
    df = pd.read_csv("data/rpct_scores.csv")

    prediction = predict_next(df["score"])

    result = pd.DataFrame(
        [{
            "prediction": prediction
        }]
    )

    result.to_csv(
        "data/predictions.csv",
        index=False
    )

    print(result)
