import pandas as pd

df_reg = pd.read_csv("insurance.csv")
df_clf = pd.read_csv("titanic.csv")

# 1: split columns by type in Insurance dataset
print("\n=== INSURANCE feature types ===")
print("Numeric features:", ["age", "bmi", "children"])
print("Categorical features:", ["sex", "smoker", "region"])
print("Target:", "charges")

# 1: split columns by type in Titanic dataset
print("\n=== TITANIC feature types ===")
print("Numeric features:", ["Age", "SibSp", "Parch", "Fare", "Pclass"])
print("Categorical features:", ["Sex", "Embarked"])
print("Target:", "Survived")

#  2: cardinality check in Insurance dataset
print("\n=== Insurance cardinality ===")
print("sex:", df_reg["sex"].nunique(), df_reg["sex"].unique())
print("smoker:", df_reg["smoker"].nunique(), df_reg["smoker"].unique())
print("region:", df_reg["region"].nunique(), df_reg["region"].unique())

#  3: cardinality check in Titanic dataset
print("\n=== Titanic cardinality ===")
print("Sex:", df_clf["Sex"].nunique(), df_clf["Sex"].unique())
print("Pclass:", df_clf["Pclass"].nunique(), sorted(df_clf["Pclass"].unique()))
print("Embarked:", df_clf["Embarked"].nunique(), df_clf["Embarked"].unique())

# 4: columns not useful as features

print("\n=== Columns likely to drop/transform (titanic) ===")
print("PassengerId: pure row identifier, no predictive signal an every value is unique and arbitrary.")
print("Name: free text, not directly usable because could be transformed to extract a 'title' (Mr/Mrs/Miss) later.")
print("Ticket: inconsistent alphanumeric codes with no clear structure.")
print("Cabin: mostly missing and high cardinality. Likely dropped or turned into a 'deck' feature.")