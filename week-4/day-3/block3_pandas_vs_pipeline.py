import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

X_dev = pd.read_parquet("X_dev_engineered.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# === APPROACH 1: Ad-hoc pandas (LEAKY) ===
# Fit imputation, scaling, and target-mean encoding on the WHOLE dataset first
X_leaky = X_dev.copy()

# Target-mean encoding for ORGANIZATION_TYPE, computed on ALL rows (including future validation rows)
org_target_means = y_dev.groupby(X_leaky["ORGANIZATION_TYPE"]).mean()
X_leaky["ORGANIZATION_TYPE_ENCODED"] = X_leaky["ORGANIZATION_TYPE"].map(org_target_means)

# Median imputation and scaling fit on the WHOLE dataset
num_cols_leaky = numeric_cols + ["ORGANIZATION_TYPE_ENCODED"]
imputer = SimpleImputer(strategy="median")
scaler = StandardScaler()
X_leaky_num = pd.DataFrame(
    scaler.fit_transform(imputer.fit_transform(X_leaky[num_cols_leaky])),
    columns=num_cols_leaky
)

leaky_model = LogisticRegression(max_iter=1000, C=0.1)
leaky_results = cross_validate(leaky_model, X_leaky_num, y_dev, cv=cv, scoring="roc_auc")
print(f"Ad-hoc pandas (leaky): {leaky_results['test_score'].mean():.4f} ± {leaky_results['test_score'].std():.4f}")

# === APPROACH 2: Pipeline (safe) ===
# Same steps, but inside a Pipeline — refit per fold
from sklearn.preprocessing import TargetEncoder

preprocessor_safe = ColumnTransformer(transformers=[
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_cols),
    ("org", Pipeline([("encoder", TargetEncoder(random_state=42))]), ["ORGANIZATION_TYPE"]),
])

safe_pipeline = Pipeline([
    ("preprocessor", preprocessor_safe),
    ("model", LogisticRegression(max_iter=1000, C=0.1)),
])

safe_results = cross_validate(safe_pipeline, X_dev, y_dev, cv=cv, scoring="roc_auc")
print(f"Pipeline (safe):       {safe_results['test_score'].mean():.4f} ± {safe_results['test_score'].std():.4f}")

gap = leaky_results['test_score'].mean() - safe_results['test_score'].mean()
print(f"\nLeakage gap: {gap:.4f} (the ad-hoc version is optimistic by this much)")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 3, Block 3 — Pandas vs Pipeline (Leakage Demonstration)\n\n")
    f.write(f"- Ad-hoc pandas (leaky): {leaky_results['test_score'].mean():.4f} ± {leaky_results['test_score'].std():.4f}\n")
    f.write(f"- Pipeline (safe): {safe_results['test_score'].mean():.4f} ± {safe_results['test_score'].std():.4f}\n")
    f.write(f"- Leakage gap: {gap:.4f}\n")