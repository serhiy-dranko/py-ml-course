import pandas as pd
import time
import joblib
from sklearn.model_selection import StratifiedKFold, cross_validate

X_working = pd.read_parquet("X_working.parquet")
y_working = pd.read_parquet("y_working.parquet").iloc[:, 0]

best_lr = joblib.load("best_logistic_regression.pkl")
best_hgb = joblib.load("best_hgb.pkl")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("Confirming best LogisticRegression on full working set...")
start = time.perf_counter()
lr_full_results = cross_validate(best_lr, X_working, y_working, cv=cv, scoring="roc_auc")
lr_time = time.perf_counter() - start
print(f"ROC-AUC: {lr_full_results['test_score'].mean():.4f} ± {lr_full_results['test_score'].std():.4f} ({lr_time:.1f}s)")

print("\nConfirming best HistGradientBoosting on full working set...")
start = time.perf_counter()
hgb_full_results = cross_validate(best_hgb, X_working, y_working, cv=cv, scoring="roc_auc")
hgb_time = time.perf_counter() - start
print(f"ROC-AUC: {hgb_full_results['test_score'].mean():.4f} ± {hgb_full_results['test_score'].std():.4f} ({hgb_time:.1f}s)")

summary = f"""
# Day 2 Summary Table

| Model | Untuned CV | Tuned CV (dev) | Tuned CV (full working) | Search type | Fits |
|---|---|---|---|---|---|
| LogisticRegression | 0.7399 ± 0.0098 | see Block 3 output | {lr_full_results['test_score'].mean():.4f} ± {lr_full_results['test_score'].std():.4f} | Grid | 10x5 |
| HistGradientBoosting | see Block 1 output | see Block 4 output | {hgb_full_results['test_score'].mean():.4f} ± {hgb_full_results['test_score'].std():.4f} | Random | 30x5 |
"""
print(summary)

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 6 — Full Working Set Confirmation\n\n")
    f.write(summary)
    