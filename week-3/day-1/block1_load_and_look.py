import pandas as pd

# Load both datasets directly from public GitHub raw URLs
insurance_url = "https://raw.githubusercontent.com/krish1407/Medical-Cost-Personal-Datasets/master/insurance.csv"
titanic_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df_reg = pd.read_csv(insurance_url)
df_clf = pd.read_csv(titanic_url)

# Save local copies df_reg.to_csv("insurance.csv", index=False)
df_reg.to_csv("insurance.csv", index=False)
df_clf.to_csv("titanic.csv", index=False)

print("=== INSURANCE (regression candidate) ===")
print("Shape:", df_reg.shape)
print("\nDtypes:\n", df_reg.dtypes)
print("\nHead:\n", df_reg.head())
print("\nDescribe:\n", df_reg.describe())

print("\n\n=== TITANIC (classification candidate) ===")
print("Shape:", df_clf.shape)
print("\nDtypes:\n", df_clf.dtypes)
print("\nHead:\n", df_clf.head())
print("\nDescribe:\n", df_clf.describe())

# 3: identify target columns and their dtype
print("\n\n=== Target columns ===")
print("charges dtype:", df_reg["charges"].dtype)
print("Survived dtype:", df_clf["Survived"].dtype)
