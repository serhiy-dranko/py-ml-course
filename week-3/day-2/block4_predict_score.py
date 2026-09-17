import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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
r2 = model.score(X_test, y_test)
print("R² on test data:", round(r2, 3))

comparison = pd.DataFrame({"actual": y_test.values[:5], "predicted": y_pred[:5]})
print(comparison)