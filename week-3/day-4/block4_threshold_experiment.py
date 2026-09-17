import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

df = pd.read_csv("titanic.csv")
df = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
X = df.drop(columns=["Survived"])
y = df["Survived"]
X = pd.get_dummies(X, columns=["Sex", "Embarked"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred_default = model.predict(X_test)

print("At default 0.5 threshold:")
print("Precision:", round(precision_score(y_test, y_pred_default), 3))
print("Recall:", round(recall_score(y_test, y_pred_default), 3))

# Lower threshold to favor recall (catch more real survivors)
y_proba = model.predict_proba(X_test)[:, 1]
y_pred_lower_threshold = (y_proba >= 0.35).astype(int)

print("\nAt lowered 0.35 threshold:")
print("Precision:", round(precision_score(y_test, y_pred_lower_threshold), 3))
print("Recall:", round(recall_score(y_test, y_pred_lower_threshold), 3))