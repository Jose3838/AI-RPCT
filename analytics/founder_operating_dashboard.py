import pandas as pd

product = pd.read_csv("data/product_readiness_score.csv").iloc[-1]
sales = pd.read_csv("data/sales_readiness.csv").iloc[-1]
pipeline = pd.read_csv("data/customer_pipeline_summary.csv").iloc[-1]
quality = pd.read_csv("data/live_data_quality_score.csv").iloc[-1]

out = pd.DataFrame([{
    "product_readiness_score": product["product_readiness_score"],
    "sales_readiness_score": sales["sales_readiness_score"],
    "pipeline_contacts": pipeline["pipeline_contacts"],
    "live_data_quality_score": quality["live_data_quality_score"]
}])

out.to_csv("data/founder_operating_dashboard.csv", index=False)

print(out)
