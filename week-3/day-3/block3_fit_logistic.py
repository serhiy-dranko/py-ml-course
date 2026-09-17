import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


df = pd.read_csv("titanic.csv")
df = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])

df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

X = df.drop(columns=["Survived"])
y = df["Survived"]
X = pd.get_dummies(X, columns=["Sex", "Embarked"], drop_first=True)

print("Class balance:")
print(y.value_counts(normalize=True))

majority_class_accuracy = y.value_counts(normalize=True).max()
print(f"\n'Always predict majority class' would score {majority_class_accuracy:.1%} accuracy.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)

for i in range(5):
    print(f"Predicted: {y_pred[i]}, Probabilities: {y_proba[i]}")