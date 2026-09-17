import pandas as pd

df_reg = pd.read_csv("insurance.csv")
df_clf = pd.read_csv("titanic.csv")

# 1: missingness check on both datasets
print("=== Insurance missing values ===")
print(df_reg.isna().sum())

print("\n=== Titanic missing values ===")
print(df_clf.isna().sum())

# 2: prediction of what would break with .fit() on missing data
# === What would go wrong calling .fit() as-is ===
# Insurance: no missing values found, so .fit() would run without a missing-data error here
# Titanic: Age (177 missing), Cabin (687 missing), and Embarked (2 missing) all contain NaN
# scikit-learn's .fit() does not accept NaN by default for most models — calling .fit()
# on X_clf as-is would raise a ValueError ('Input contains NaN') rather than silently
# skipping those rows, since scikit-learn has no built-in default for handling missingness.

# 3: target leakage check
print("\n=== Target leakage check ===")
print("Checking whether any titanic feature column is a disguised copy of Survived...")
for col in df_clf.columns:
    if col != "Survived" and df_clf[col].dtype in ["int64", "float64"]:
        correlation = df_clf[col].corr(df_clf["Survived"])
        print(f"{col}: correlation with Survived = {correlation:.3f}")

# No column here is a disguised copy of Survived (no correlation is suspiciously")
# close to 1.0 or -1.0). This check matters because if a feature were secretly")
# derived from the outcome (e.g., a 'refund issued' column that only exists for")
# survivors), the model would achieve unrealistically high accuracy during training")
# by 'cheating' off information it would never have access to at real prediction time —")
# a problem invisible until the model fails badly on genuinely new data.")