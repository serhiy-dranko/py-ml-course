import pandas as pd
import numpy as np

np.random.seed(42)

n_rows = 1500

regions = ["West", "East", "North", "South"]
categories = ["Electronics", "Clothing", "Home", "Toys", "Books"]

df = pd.DataFrame({
    "order_id": range(1, n_rows + 1),
    "customer_name": [f"Customer_{i}" for i in np.random.randint(1, 400, n_rows)],
    "region": np.random.choice(regions, n_rows),
    "category": np.random.choice(categories, n_rows),
    "sales": np.round(np.random.exponential(scale=200, size=n_rows), 2),
    "quantity": np.random.randint(1, 10, n_rows),
    "order_date": pd.date_range("2025-01-01", periods=n_rows, freq="h"),
})

df.to_csv("raw_orders.csv", index=False)
print("raw_orders.csv created with shape:", df.shape)