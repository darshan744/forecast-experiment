import pandas as pd
import numpy as np
from datetime import datetime , timedelta


products = [
    {"id": "rice", "name": "Rice", "base": 3.0, "seasonality": "flat"},
    {"id": "paint", "name": "Paint", "base": 2.0, "seasonality": "spikeWinter"},
    {"id": "battery", "name": "Battery", "base": 1.2, "seasonality": "spikeSummer"},
    {"id": "detergent", "name": "Detergent", "base": 4.0, "seasonality": "random"},
    {"id": "sugar", "name": "Sugar", "base": 2.5, "seasonality": "flat"},
    {"id": "oil", "name": "Engine Oil", "base": 1.5, "seasonality": "spikeSummer"},
    {"id": "jacket", "name": "Jacket Cloth", "base": 0.8, "seasonality": "spikeWinter"},
    {"id": "water", "name": "Packaged Water", "base": 3.5, "seasonality": "spikeSummer"},
    {"id": "soap", "name": "Soap", "base": 2.8, "seasonality": "flat"},
    {"id": "wipes", "name": "Sanitary Wipes", "base": 2.0, "seasonality": "random"},
]

startDate = datetime(2024 , 8 , 1)
endDate = datetime(2025, 7, 31)

dateRange = pd.date_range(start=startDate, end=endDate, freq='D')

def seasonalMultiplier(month , seasonality):
    if seasonality == "flat":
        return 1.0 * np.random.normal(0 , 0.05)
    if seasonality == "spikeWinter":
        return 1.6 if month in [11, 12, 1, 2] else 1.0 + np.random.normal(0, 0.1)
    if seasonality == "spikeSummer":
        return 1.6 if month in [4, 5, 6, 7] else 1.0 + np.random.normal(0, 0.1)
    if seasonality == "random":
        return 1.0 + np.random.normal(0, 0.3)
    return 1.0

rows = []

for product in products:
    for date in dateRange:
        multiplier = seasonalMultiplier(date.month , product["seasonality"])

        usage = multiplier * product["base"]
        usage += np.random.normal(0, 0.2)  # Adding some random noise to the usage
        usage = max(0 , round(usage , 2))

        rows.append({
            "date":date.strftime("%Y-%m-%d"),
            "product_id":product["id"],
            "product_name": product["name"],
            "quantity_used":usage
        })



df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])
df.to_csv("product_usage.csv", index=False)
print("Product usage data generated and saved to 'product_usage.csv'.")
