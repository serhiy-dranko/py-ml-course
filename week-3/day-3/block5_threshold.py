import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

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
y_proba = model.predict_proba(X_test)

proba_class1 = y_proba[:, 1]
borderline_idx = np.where((proba_class1 > 0.4) & (proba_class1 < 0.6))[0]
print("Borderline row indices:", borderline_idx[:5])

i = borderline_idx[0]
print(f"\nProbability of survival: {proba_class1[i]:.3f}")
print(f"Label at 0.5 threshold: {int(proba_class1[i] >= 0.5)}")
print(f"Label at 0.4 threshold: {int(proba_class1[i] >= 0.4)}")
print(f"Label at 0.6 threshold: {int(proba_class1[i] >= 0.6)}")