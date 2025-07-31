import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


# Load data
dataFrame = pd.read_csv("../data/product_usage.csv", parse_dates=["date"])


def preprocessData(dataFrame):
    dataFrame = dataFrame[dataFrame["quantity_used"] >= 0]
    dataFrame["quantity_used"] = dataFrame["quantity_used"].replace(0, method="ffill")

    dataFrame["dayOfWeek"] = dataFrame["date"].dt.dayofweek
    dataFrame["is_weekend"] = dataFrame["dayOfWeek"] >= 5
    dataFrame["month"] = dataFrame["date"].dt.month

    dataFrame = dataFrame.sort_values(by=["product_id", "date"])
    dataFrame["rolling_avg_7d"] = dataFrame.groupby("product_id")[
        "quantity_used"
    ].transform(lambda x: x.rolling(window=7, min_periods=1).mean())

    return dataFrame


def trainModel(dataFrame, productId):
    product_df = dataFrame[dataFrame["product_id"] == productId].copy()
    if len(product_df) < 30:
        print(f"Skipping product {productId}: Not enough data")
        return None, None, None, None

    X = product_df[["dayOfWeek", "is_weekend", "month", "rolling_avg_7d"]]
    y = product_df["quantity_used"]

    splitIndex = int(len(product_df) * 0.8)
    X_train, X_test = X[:splitIndex], X[splitIndex:]
    y_train, y_test = y[:splitIndex], y[splitIndex:]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return mse, y_test, y_pred, model


def run_all_products(df: pd.DataFrame):
    unique_products = df["product_id"].unique()
    for product_id in unique_products:
        mse, y_test, y_pred, model = trainModel(df, product_id)
        if mse is not None:
            print(f"{product_id}: MSE = {mse:.5f}")


# Run
df = preprocessData(dataFrame)

# Train and test on single product
mse, y_test, y_pred, model = trainModel(df, "rice")
print(f"Single product (rice) MSE: {mse}")

# Uncomment this to run all products
run_all_products(df)

plt.plot(actual_values, label="Actual")
plt.plot(predicted_values, label="Predicted")
plt.title("Milk usage forecast")
plt.legend()
plt.savefig("milk_forecast.png")  # or plt.show()
