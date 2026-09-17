import pandas as pd

df_reg = pd.read_csv("insurance.csv")
df_clf = pd.read_csv("titanic.csv")

# 1: X and y for insurance (regression)
X_reg = df_reg.drop(columns=["charges"])
y_reg = df_reg["charges"]

print("=== Insurance X/y shapes ===")
print("X_reg shape:", X_reg.shape, "2D  Rows, feature columns")
print("y_reg shape:", y_reg.shape, "1D  One target value per row")

# 2: X and y for titanic (classification)
non_features = ["PassengerId", "Name", "Ticket", "Cabin", "Survived"]
X_clf = df_clf.drop(columns=non_features)
y_clf = df_clf["Survived"]

print("\n=== Titanic X/y shapes ===")
print("X_clf shape:", X_clf.shape, "2D  Rows, feature columns")
print("y_clf shape:", y_clf.shape, "1D  One target value per row")
print("X_clf columns:", X_clf.columns.tolist())

#  3: deliberately trigger a shape mismatch
print("\n=== Shape mismatch demonstration ===")
single_bracket = df_reg["age"]          
double_bracket = df_reg[["age"]] 

print("df_reg['age'] type:", type(single_bracket), "shape:", single_bracket.shape)
print("df_reg[['age']] type:", type(double_bracket), "shape:", double_bracket.shape)

print("df_reg['age'] type:", type(single_bracket), "head:", single_bracket.head())
print("df_reg[['age']] type:", type(double_bracket), "head:", double_bracket.head())