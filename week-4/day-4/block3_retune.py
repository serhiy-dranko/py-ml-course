import pandas as pd
import numpy as np
import time
from scipy.stats import loguniform, randint
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
import joblib
import json

def engineer_features(df):
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

X_dev = engineer_features(pd.read_parquet("X_dev.parquet"))
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

preprocessor = ColumnTransformer([
    ("num", "passthrough", numeric_cols),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
])
pipeline = Pipeline([("preprocessor", preprocessor), ("model", HistGradientBoostingClassifier(random_state=42))])

# Narrow ranges informed by Blocks 1-2: peak was near max_leaf_nodes=22, learning_rate=0.0383
param_distributions = {
    "model__learning_rate": loguniform(0.02, 0.06),
    "model__max_leaf_nodes": randint(15, 35),
    "model__min_samples_leaf": randint(60, 130),
    "model__l2_regularization": loguniform(1e-2, 1),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

start = time.perf_counter()
search = RandomizedSearchCV(
    pipeline, param_distributions, n_iter=20, scoring="roc_auc",
    cv=cv, random_state=42, n_jobs=-1
)
search.fit(X_dev, y_dev)
elapsed = time.perf_counter() - start

print(f"Re-tune took {elapsed:.1f}s")
print(f"Best params: {search.best_params_}")
print(f"Best CV ROC-AUC: {search.best_score_:.4f}")
print(f"(Day 2 params on this feature set scored 0.7516 ± 0.0096 on dev)")

results_df = pd.DataFrame(search.cv_results_).sort_values("rank_test_score")
print("\nTop 5 candidates:")
print(results_df[["params", "mean_test_score", "std_test_score"]].head(5).to_string())

# FREEZE: save final configuration
final_params = search.best_params_
with open("results/frozen_hyperparameters.json", "w") as f:
    json.dump({k: float(v) if isinstance(v, (np.floating, float)) else int(v) for k, v in final_params.items()}, f, indent=2)
print("\nFrozen hyperparameters saved to results/frozen_hyperparameters.json")

joblib.dump(search.best_estimator_, "results/frozen_model_dev.pkl")

progress_table = f"""
# Progress Table (through Day 4, Block 3)

| Stage | CV Mean ± Std (dev subsample) |
|---|---|
| Day 1 baseline (untuned HGB, raw features) | 0.7387 ± 0.0112 |
| Day 2 tuned HGB (raw features) | 0.7458 ± 0.0108 |
| Day 3 tuned HGB + engineered features | 0.7516 ± 0.0096 |
| Day 4 re-tuned HGB + engineered features | {search.best_score_:.4f} ± {results_df.iloc[0]['std_test_score']:.4f} |
"""
print(progress_table)

with open("decision_log.md", "a") as f:
    f.write("\n## Day 4, Block 3 — Short Re-Tune (FROZEN)\n\n")
    f.write(f"- Best params: {final_params}\n")
    f.write(f"- Best CV ROC-AUC: {search.best_score_:.4f}\n")
    f.write(progress_table)
    f.write("\n**Model configuration is now FROZEN. No further changes after this point.**\n")