import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# BLOCK 1
# Rebuild Day 2 pipeline end-to-end
df = pd.read_csv("insurance.csv")
X = df.drop(columns=["charges"])
y = df["charges"]
X = pd.get_dummies(X, columns=["sex", "smoker", "region"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# BLOCK 2
# Real metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print("RMSE:", round(rmse, 2))
print("R²:", round(r2, 3))

# Trivial baseline: always predict the mean
baseline_pred = np.full_like(y_test, fill_value=y_train.mean(), dtype=float)
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
print("\nBaseline RMSE (always predict mean):", round(baseline_rmse, 2))

improvement = baseline_rmse - rmse
print(f"\nModel improves on the baseline by ${improvement:.2f} of typical error.")