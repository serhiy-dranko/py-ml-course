import pandas as pd

df = pd.read_csv("insurance.csv")

X = df.drop(columns=["charges"])
y = df["charges"]

print("Before encoding:")
print(X.dtypes)
print("Column count:", X.shape[1])

X = pd.get_dummies(X, columns=["sex", "smoker", "region"], drop_first=True)

print("\nAfter one-hot encoding:")
print(X.dtypes)
print("Column count:", X.shape[1])
print("\nFirst few rows:")
print(X.head())