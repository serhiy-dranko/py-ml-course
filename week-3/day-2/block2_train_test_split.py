import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("insurance.csv")
X = df.drop(columns=["charges"])
y = df["charges"]
X = pd.get_dummies(X, columns=["sex", "smoker", "region"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)


print(f"\nTrain proportion: {len(X_train) / len(X):.1%}")
print(f"Test proportion: {len(X_test) / len(X):.1%}")