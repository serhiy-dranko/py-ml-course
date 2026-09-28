import pandas as pd
import numpy as np
import json
import joblib
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, accuracy_score

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

# Step 1: refit frozen pipeline on ENTIRE working set
X_working = engineer_features(pd.read_parquet("X_working.parquet"))
y_working = pd.read_parquet("y_working.parquet").iloc[:, 0]

with open("results/frozen_hyperparameters.json") as f:
    frozen_params_raw = json.load(f)

frozen_params = {k.replace("model__", ""): v for k, v in frozen_params_raw.items()}

numeric_cols = X_working.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_working.select_dtypes(include="object").columns.tolist()

final_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", numeric_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(random_state=42, **frozen_params)),
])

print("Refitting frozen pipeline on entire working set...")
final_pipeline.fit(X_working, y_working)

# Step 2: load locked test set — FIRST TIME SINCE DAY 1
X_test = engineer_features(pd.read_parquet("X_test.parquet"))
y_test = pd.read_parquet("y_test.parquet").iloc[:, 0]
print(f"Test set loaded: {X_test.shape}")

# Step 3: evaluate ONCE
y_proba_test = final_pipeline.predict_proba(X_test)[:, 1]
y_pred_test = final_pipeline.predict(X_test)

test_roc_auc = roc_auc_score(y_test, y_proba_test)
test_pr_auc = average_precision_score(y_test, y_proba_test)
test_log_loss = log_loss(y_test, y_proba_test)
test_accuracy = accuracy_score(y_test, y_pred_test)

print("\n=== LOCKED TEST SET RESULTS (evaluated once) ===")
print(f"ROC-AUC:  {test_roc_auc:.4f}")
print(f"PR-AUC:   {test_pr_auc:.4f}")
print(f"Log-loss: {test_log_loss:.4f}")
print(f"Accuracy: {test_accuracy:.4f}")

# Step 4: baselines on the same test set
dummy = DummyClassifier(strategy="prior")
dummy.fit(X_working, y_working)
dummy_proba = dummy.predict_proba(X_test)[:, 1]
dummy_roc_auc = roc_auc_score(y_test, dummy_proba)
dummy_accuracy = accuracy_score(y_test, dummy.predict(X_test))

simple_preprocessor = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OneHotEncoder(handle_unknown="ignore"))]), categorical_cols),
])
simple_pipeline = Pipeline([("preprocessor", simple_preprocessor), ("model", LogisticRegression(max_iter=1000))])
simple_pipeline.fit(X_working, y_working)
simple_proba = simple_pipeline.predict_proba(X_test)[:, 1]
simple_roc_auc = roc_auc_score(y_test, simple_proba)

print(f"\nDummy baseline test ROC-AUC:  {dummy_roc_auc:.4f} (accuracy: {dummy_accuracy:.4f})")
print(f"Simple baseline test ROC-AUC: {simple_roc_auc:.4f}")

# Step 5: compare test vs CV estimate
cv_estimate = 0.7533
gap = test_roc_auc - cv_estimate
print(f"\nFinal CV estimate: {cv_estimate:.4f}")
print(f"Test ROC-AUC:       {test_roc_auc:.4f}")
print(f"Gap: {gap:.4f}")
if abs(gap) > 0.015:
    print("WARNING: gap larger than expected noise floor — investigate for leakage or distribution mismatch.")
else:
    print("Gap is within the expected noise floor — no leakage or mismatch signal detected.")

# Step 6: save everything
joblib.dump(final_pipeline, "results/final_model.pkl")
metrics_table = pd.DataFrame({
    "model": ["Dummy", "Simple LR baseline", "Final HGB"],
    "test_roc_auc": [dummy_roc_auc, simple_roc_auc, test_roc_auc],
})
metrics_table.to_csv("results/test_metrics.csv", index=False)
print("\nSaved results/final_model.pkl and results/test_metrics.csv")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 4, Block 4 — LOCKED TEST SET EVALUATION (one-time)\n\n")
    f.write(f"- Test ROC-AUC: {test_roc_auc:.4f}\n")
    f.write(f"- Test PR-AUC: {test_pr_auc:.4f}\n")
    f.write(f"- Test log-loss: {test_log_loss:.4f}\n")
    f.write(f"- Test accuracy: {test_accuracy:.4f}\n")
    f.write(f"- Dummy baseline test ROC-AUC: {dummy_roc_auc:.4f}\n")
    f.write(f"- Simple baseline test ROC-AUC: {simple_roc_auc:.4f}\n")
    f.write(f"- CV estimate vs test gap: {gap:.4f}\n")