import pandas as pd
import numpy as np
from datetime import datetime

products = pd.read_json("products.json").to_dict(orient="records")
startDate = datetime(2024, 8, 1)
endDate = datetime(2025, 7, 31)
dateRange = pd.date_range(start=startDate, end=endDate, freq="D")


def seasonalMultiplier(month, seasonality):
    if seasonality == "flat":
        return 1.0 + np.random.normal(0, 0.05)
    if seasonality == "spikeWinter":
        return 1.6 if month in [11, 12, 1, 2] else 1.0 + np.random.normal(0, 0.1)
    if seasonality == "spikeSummer":
        return 1.6 if month in [4, 5, 6, 7] else 1.0 + np.random.normal(0, 0.1)
    if seasonality == "random":
        return 1.0 + np.random.normal(0, 0.3)
    return 1.0


rows = []


def generateUsageData():
    for product in products:
        for date in dateRange:
            base = product["base_usage"]
            min_usage = product["min_usage"]
            rounding = product["rounding"]

            multiplier = seasonalMultiplier(date.month, product["seasonality"])
            usage = base * multiplier * np.random.normal(1.0, 0.1)

            if date.weekday() in [5, 6]:  # weekend
                usage *= 0.8

            if product.get("allow_zero_days", False) and np.random.rand() < 0.05:
                usage = 0.0

            usage = round(max(min_usage, usage), rounding)

            rows.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "quantity_used": usage,
                }
            )

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv("product_usage.csv", index=False)
    print("✅ Product usage data generated and saved to 'product_usage.csv'.")

generateUsageData()
