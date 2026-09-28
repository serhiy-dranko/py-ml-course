import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
import joblib

X_dev = pd.read_parquet("X_dev_engineered.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]
X_working = pd.read_parquet("X_working.parquet")
y_working = pd.read_parquet("y_working.parquet").iloc[:, 0]

def engineer_features(df):
    """Final stateless feature engineering — kept from Block 2, validated by permutation importance."""
    df = df.copy()
    df["DAYS_EMPLOYED_ANOM"] = (df["DAYS_EMPLOYED"] == 365243).astype(int)
    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, np.nan)
    df["AGE_YEARS"] = -df["DAYS_BIRTH"] / 365.25
    df["EMPLOYED_YEARS"] = -df["DAYS_EMPLOYED"] / 365.25
    df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df["ANNUITY_INCOME_RATIO"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    df["CREDIT_GOODS_RATIO"] = df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"]
    df["ANNUITY_CREDIT_RATIO"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]
    ext_cols = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
    df["EXT_SOURCE_MEAN"] = df[ext_cols].mean(axis=1)
    df["EXT_SOURCE_MIN"] = df[ext_cols].min(axis=1)
    doc_cols = [c for c in df.columns if c.startswith("FLAG_DOCUMENT_")]
    df["DOCUMENT_COUNT"] = df[doc_cols].sum(axis=1)
    return df

X_working_engineered = engineer_features(X_working)

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

# Final decision: keep all engineered features, ordinal encoding for HGB,
# no filtering (Block 5 showed it hurt), best Day 2 hyperparameters
final_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", numeric_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(
        random_state=42,
        learning_rate=0.0383,
        max_leaf_nodes=22,
        min_samples_leaf=97,
        l2_regularization=0.0494,
    )),
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("Scoring final pipeline on dev subsample...")
results_dev = cross_validate(final_pipeline, X_dev, y_dev, cv=cv, scoring="roc_auc")
print(f"Dev subsample: {results_dev['test_score'].mean():.4f} ± {results_dev['test_score'].std():.4f}")

print("\nScoring final pipeline on full working set...")
results_full = cross_validate(final_pipeline, X_working_engineered, y_working, cv=cv, scoring="roc_auc")
print(f"Full working set: {results_full['test_score'].mean():.4f} ± {results_full['test_score'].std():.4f}")

# Ablation table
ablation_table = """
# Day 3 Ablation Table

| Change | CV Mean ± Std (dev) | Effect vs. Day 1 baseline (0.7387) |
|---|---|---|
| Day 1 baseline (HGB, untuned, raw features) | 0.7387 ± 0.0112 | — |
| Day 2 tuned HGB | 0.7458 ± 0.0108 | +0.0071 |
| + Stateless feature engineering | 0.7488 ± 0.0089 | +0.0101 |
| + Filtering (constant + correlated) | 0.7459 ± 0.0081 | +0.0072 (worse than no filtering) |
| Final pipeline (engineered, no filtering) | see above | see above |
"""
print(ablation_table)

final_pipeline.fit(X_working_engineered, y_working)
joblib.dump(final_pipeline, "final_feature_pipeline.pkl")
print("\nSaved final_feature_pipeline.pkl for Day 4")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 3, Block 6 — Final Pipeline\n\n")
    f.write(f"- Dev subsample: {results_dev['test_score'].mean():.4f} ± {results_dev['test_score'].std():.4f}\n")
    f.write(f"- Full working set: {results_full['test_score'].mean():.4f} ± {results_full['test_score'].std():.4f}\n")
    f.write(ablation_table)