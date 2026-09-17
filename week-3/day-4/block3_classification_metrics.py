import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report

# Rebuild Day 3 pipeline end-to-end
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
y_pred = model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Precision:", round(precision_score(y_test, y_pred), 3))
print("Recall:", round(recall_score(y_test, y_pred), 3))

# Trivial baseline: always predict majority class
majority_class = y_train.mode()[0]
baseline_pred = [majority_class] * len(y_test)
print("Baseline accuracy (always predict majority class):", round(accuracy_score(y_test, baseline_pred), 3))