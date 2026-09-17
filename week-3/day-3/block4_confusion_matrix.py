import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

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

cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:")
fig11 = px.imshow(cm, text_auto=True,
                   labels=dict(x="Predicted", y="Actual"),
                   x=['Died', 'Survived'], y=['Died', 'Survived'],
                   title='Confusion Matrix', color_continuous_scale='Blues')
fig11.show()
print(cm)
print("\nLayout: [[TN, FP], [FN, TP]]")
print(f"True Negatives (correctly predicted died): {cm[0][0]}")
print(f"False Positives (predicted survived, actually died): {cm[0][1]}")
print(f"False Negatives (predicted died, actually survived): {cm[1][0]}")
print(f"True Positives (correctly predicted survived): {cm[1][1]}")