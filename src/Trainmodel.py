import pandas as pd

# Pass path of the file relative to the script running directory
# For me its in parent DIR
df = pd.read_csv("./data/product_usage.csv")

print("Data loaded successfully.")

print(df.head())
