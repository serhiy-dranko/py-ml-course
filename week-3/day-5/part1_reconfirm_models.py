import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score

print("=" * 60)
print("REGRESSION MODEL (insurance.csv)")
print("=" * 60)

df_reg = pd.read_csv("insurance.csv")
X_reg = df_reg.drop(columns=["charges"])
y_reg = df_reg["charges"]
X_reg = pd.get_dummies(X_reg, columns=["sex", "smoker", "region"], drop_first=True)

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg_model = LinearRegression()
reg_model.fit(X_train_reg, y_train_reg)
y_pred_reg = reg_model.predict(X_test_reg)

rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))
r2 = r2_score(y_test_reg, y_pred_reg)
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.3f}")

coef_table = dict(zip(X_train_reg.columns, reg_model.coef_))
top_coef = max(coef_table.items(), key=lambda x: x[1])
print(f"Largest coefficient: {top_coef[0]} = {top_coef[1]:.2f}")

print("\n" + "=" * 60)
print("CLASSIFICATION MODEL (titanic.csv)")
print("=" * 60)

df_clf = pd.read_csv("titanic.csv")
df_clf = df_clf.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
df_clf["Age"] = df_clf["Age"].fillna(df_clf["Age"].median())
df_clf["Embarked"] = df_clf["Embarked"].fillna(df_clf["Embarked"].mode()[0])
X_clf = df_clf.drop(columns=["Survived"])
y_clf = df_clf["Survived"]
X_clf = pd.get_dummies(X_clf, columns=["Sex", "Embarked"], drop_first=True)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

clf_model = LogisticRegression(max_iter=1000)
clf_model.fit(X_train_clf, y_train_clf)
y_pred_clf = clf_model.predict(X_test_clf)

acc = accuracy_score(y_test_clf, y_pred_clf)
prec = precision_score(y_test_clf, y_pred_clf)
rec = recall_score(y_test_clf, y_pred_clf)
print(f"Accuracy: {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall: {rec:.3f}")

print("\nBoth models reconfirmed and running end-to-end.")