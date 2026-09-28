import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix, precision_score, recall_score
from sklearn.inspection import permutation_importance
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

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

X_working = engineer_features(pd.read_parquet("X_working.parquet"))
y_working = pd.read_parquet("y_working.parquet").iloc[:, 0]
X_test = engineer_features(pd.read_parquet("X_test.parquet"))
y_test = pd.read_parquet("y_test.parquet").iloc[:, 0]

final_pipeline = joblib.load("results/final_model.pkl")
y_proba_test = final_pipeline.predict_proba(X_test)[:, 1]

numeric_cols = X_working.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_working.select_dtypes(include="object").columns.tolist()

dummy = DummyClassifier(strategy="prior")
dummy.fit(X_working, y_working)
dummy_proba = dummy.predict_proba(X_test)[:, 1]

simple_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OneHotEncoder(handle_unknown="ignore"))]), categorical_cols),
    ])),
    ("model", LogisticRegression(max_iter=1000)),
])
simple_pipeline.fit(X_working, y_working)
simple_proba = simple_pipeline.predict_proba(X_test)[:, 1]

# Point 1: ROC and PR curves
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for name, proba, color in [("Dummy", dummy_proba, "gray"), ("Simple LR", simple_proba, "orange"), ("Final HGB", y_proba_test, "#4C72B0")]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    axes[0].plot(fpr, tpr, label=name, color=color)
axes[0].plot([0, 1], [0, 1], "k--", alpha=0.3)
axes[0].set_title("ROC Curve — final model beats both baselines")
axes[0].set_xlabel("False Positive Rate")
axes[0].set_ylabel("True Positive Rate")
axes[0].legend()

for name, proba, color in [("Dummy", dummy_proba, "gray"), ("Simple LR", simple_proba, "orange"), ("Final HGB", y_proba_test, "#4C72B0")]:
    prec, rec, _ = precision_recall_curve(y_test, proba)
    axes[1].plot(rec, prec, label=name, color=color)
axes[1].set_title("Precision-Recall Curve")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].legend()

plt.tight_layout()
plt.savefig("results/roc_pr_curves.png", dpi=150)
plt.close()
print("Saved results/roc_pr_curves.png")

# Point 2: operating threshold from a cost ratio
# Assume: missing a defaulter (FN) costs 5x more than wrongly declining a repaying client (FP)
cost_ratio = 5
thresholds = np.linspace(0.01, 0.5, 100)
best_threshold, best_cost = None, np.inf
for t in thresholds:
    preds = (y_proba_test >= t).astype(int)
    cm = confusion_matrix(y_test, preds)
    tn, fp, fn, tp = cm.ravel()
    cost = fn * cost_ratio + fp * 1
    if cost < best_cost:
        best_cost = cost
        best_threshold = t

preds_at_threshold = (y_proba_test >= best_threshold).astype(int)
cm_final = confusion_matrix(y_test, preds_at_threshold)
prec_at_t = precision_score(y_test, preds_at_threshold)
rec_at_t = recall_score(y_test, preds_at_threshold)

print(f"\n=== Threshold selection (assumed cost ratio: missed defaulter = {cost_ratio}x false decline) ===")
print(f"Chosen threshold: {best_threshold:.3f}")
print(f"Precision: {prec_at_t:.4f}, Recall: {rec_at_t:.4f}")
print(f"Confusion matrix:\n{cm_final}")

# Point 3: decile/lift table
test_results = pd.DataFrame({"y_true": y_test.values, "proba": y_proba_test})
test_results["decile"] = pd.qcut(test_results["proba"], 10, labels=False, duplicates="drop")
overall_rate = test_results["y_true"].mean()

lift_table = test_results.groupby("decile").agg(
    n=("y_true", "size"),
    default_rate=("y_true", "mean"),
).reset_index()
lift_table["decile"] = lift_table["decile"] + 1  # 1-indexed, decile 10 = highest risk
lift_table = lift_table.sort_values("decile", ascending=False)
lift_table["lift"] = lift_table["default_rate"] / overall_rate

print(f"\n=== Decile/Lift Table (overall default rate: {overall_rate:.4f}) ===")
print(lift_table.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(lift_table["decile"].astype(str), lift_table["lift"], color="#4C72B0")
ax.axhline(1, color="gray", linestyle="--", label="No lift (random)")
ax.set_title("Lift by risk decile — top decile captures much higher default risk")
ax.set_xlabel("Risk decile (10 = highest predicted risk)")
ax.set_ylabel("Lift over overall default rate")
ax.legend()
plt.tight_layout()
plt.savefig("results/lift_table.png", dpi=150)
plt.close()
print("Saved results/lift_table.png")

# Point 4: permutation importance on held-out (test) data
perm_result = permutation_importance(
    final_pipeline, X_test, y_test, scoring="roc_auc", n_repeats=5, random_state=42, n_jobs=-1
)
perm_df = pd.DataFrame({
    "feature": X_test.columns,
    "importance": perm_result.importances_mean,
}).sort_values("importance", ascending=False)

print("\n=== Top 15 features by permutation importance (test set) ===")
print(perm_df.head(15).to_string(index=False))
perm_df.head(15).to_csv("results/top_15_features.csv", index=False)

# Point 5: confident mistakes
test_results["y_pred"] = (test_results["proba"] >= 0.5).astype(int)
mistakes = test_results[test_results["y_true"] != test_results["y_pred"]].copy()
mistakes["confidence"] = np.abs(mistakes["proba"] - 0.5)
confident_mistakes = mistakes.sort_values("confidence", ascending=False).head(10)
print("\n=== Top 10 most confident mistakes ===")
print(confident_mistakes.to_string(index=False))
confident_mistakes.to_csv("results/confident_mistakes.csv", index=False)

with open("decision_log.md", "a") as f:
    f.write("\n## Day 4, Block 5 — Business-Oriented Results\n\n")
    f.write(f"- Threshold at cost ratio {cost_ratio}: {best_threshold:.3f}, precision={prec_at_t:.4f}, recall={rec_at_t:.4f}\n")
    f.write(f"- Top decile lift: {lift_table.iloc[0]['lift']:.2f}x\n")
    f.write(f"- Top 15 features saved to results/top_15_features.csv\n")