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

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Point 2: reproduce Day 1 simple baseline
preprocessor_lr = ColumnTransformer(transformers=[
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_cols),
])

lr_pipeline = Pipeline([
    ("preprocessor", preprocessor_lr),
    ("model", LogisticRegression(max_iter=1000)),
])

lr_results = cross_validate(lr_pipeline, X_dev, y_dev, cv=cv, scoring="roc_auc")
print("=== Reproduced Day 1 baseline (LogisticRegression) ===")
print(f"ROC-AUC: {lr_results['test_score'].mean():.4f} ± {lr_results['test_score'].std():.4f}")
print("(Day 1 was: 0.7399 ± 0.0098 — should match closely)")

# Point 3: untuned HistGradientBoosting reference
# HGB handles missing values natively and works with ordinal-encoded categoricals
preprocessor_hgb = ColumnTransformer(transformers=[
    ("num", "passthrough", numeric_cols),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
])

hgb_pipeline = Pipeline([
    ("preprocessor", preprocessor_hgb),
    ("model", HistGradientBoostingClassifier(random_state=42)),
])

hgb_results = cross_validate(hgb_pipeline, X_dev, y_dev, cv=cv, scoring="roc_auc")
print("\n=== Untuned HistGradientBoostingClassifier reference ===")
print(f"ROC-AUC: {hgb_results['test_score'].mean():.4f} ± {hgb_results['test_score'].std():.4f}")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 1 — Reload and Reproduce\n\n")
    f.write(f"- Reproduced LogisticRegression baseline: {lr_results['test_score'].mean():.4f} ± {lr_results['test_score'].std():.4f} (Day 1 was 0.7399 ± 0.0098)\n")
    f.write(f"- Untuned HistGradientBoostingClassifier reference: {hgb_results['test_score'].mean():.4f} ± {hgb_results['test_score'].std():.4f}\n")