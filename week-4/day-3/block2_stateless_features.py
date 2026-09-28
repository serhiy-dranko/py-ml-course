import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

def engineer_features(df):
    """Stateless, row-wise feature engineering — safe to apply before or after split."""
    df = df.copy()

    # Sentinel fix
    df["DAYS_EMPLOYED_ANOM"] = (df["DAYS_EMPLOYED"] == 365243).astype(int)
    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, np.nan)

    # Unit conversions
    df["AGE_YEARS"] = -df["DAYS_BIRTH"] / 365.25
    df["EMPLOYED_YEARS"] = -df["DAYS_EMPLOYED"] / 365.25

    # Ratios
    df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df["ANNUITY_INCOME_RATIO"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    df["CREDIT_GOODS_RATIO"] = df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"]
    df["ANNUITY_CREDIT_RATIO"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]

    # EXT_SOURCE aggregates
    ext_cols = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
    df["EXT_SOURCE_MEAN"] = df[ext_cols].mean(axis=1)
    df["EXT_SOURCE_MIN"] = df[ext_cols].min(axis=1)

    # Document flag count
    doc_cols = [c for c in df.columns if c.startswith("FLAG_DOCUMENT_")]
    df["DOCUMENT_COUNT"] = df[doc_cols].sum(axis=1)

    return df

X_dev_engineered = engineer_features(X_dev)
print("New shape after engineering:", X_dev_engineered.shape)
print("New columns:", [c for c in X_dev_engineered.columns if c not in X_dev.columns])

numeric_cols = X_dev_engineered.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev_engineered.select_dtypes(include="object").columns.tolist()

def build_lr_pipeline(num_cols, cat_cols):
    preprocessor = ColumnTransformer(transformers=[
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
    ])
    return Pipeline([("preprocessor", preprocessor), ("model", LogisticRegression(max_iter=1000, C=0.1))])

def build_hgb_pipeline(num_cols, cat_cols):
    preprocessor = ColumnTransformer(transformers=[
        ("num", "passthrough", num_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cat_cols),
    ])
    return Pipeline([("preprocessor", preprocessor), ("model", HistGradientBoostingClassifier(random_state=42))])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Baseline (Day 1 features only) for comparison
lr_baseline = cross_validate(build_lr_pipeline(
    X_dev.select_dtypes(include=["int64","float64","int32","float32","int8","int16"]).columns.tolist(),
    X_dev.select_dtypes(include="object").columns.tolist()
), X_dev, y_dev, cv=cv, scoring="roc_auc")

lr_engineered = cross_validate(build_lr_pipeline(numeric_cols, categorical_cols), X_dev_engineered, y_dev, cv=cv, scoring="roc_auc")
hgb_engineered = cross_validate(build_hgb_pipeline(numeric_cols, categorical_cols), X_dev_engineered, y_dev, cv=cv, scoring="roc_auc")

print(f"\nLR baseline (no new features):  {lr_baseline['test_score'].mean():.4f} ± {lr_baseline['test_score'].std():.4f}")
print(f"LR with engineered features:    {lr_engineered['test_score'].mean():.4f} ± {lr_engineered['test_score'].std():.4f}")
print(f"HGB with engineered features:   {hgb_engineered['test_score'].mean():.4f} ± {hgb_engineered['test_score'].std():.4f}")
print("(Day 2 tuned HGB reference: 0.7458 ± ~0.0108 on dev subsample)")

X_dev_engineered.to_parquet("X_dev_engineered.parquet")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 3, Block 2 — Stateless Feature Engineering\n\n")
    f.write(f"- LR baseline: {lr_baseline['test_score'].mean():.4f} ± {lr_baseline['test_score'].std():.4f}\n")
    f.write(f"- LR + engineered features: {lr_engineered['test_score'].mean():.4f} ± {lr_engineered['test_score'].std():.4f}\n")
    f.write(f"- HGB + engineered features: {hgb_engineered['test_score'].mean():.4f} ± {hgb_engineered['test_score'].std():.4f}\n")