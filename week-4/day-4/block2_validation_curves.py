import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, validation_curve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder

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

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

hgb_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", numeric_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(
        random_state=42, learning_rate=0.0383, min_samples_leaf=97, l2_regularization=0.0494,
    )),
])

# Validation curve for max_leaf_nodes
leaf_range = [5, 10, 15, 22, 31, 45, 63, 90, 127]
train_scores, val_scores = validation_curve(
    hgb_pipeline, X_dev, y_dev, param_name="model__max_leaf_nodes",
    param_range=leaf_range, cv=cv, scoring="roc_auc", n_jobs=-1
)

train_mean, val_mean = train_scores.mean(axis=1), val_scores.mean(axis=1)
train_std, val_std = train_scores.std(axis=1), val_scores.std(axis=1)

print("=== Validation curve: max_leaf_nodes ===")
for n, tm, vm in zip(leaf_range, train_mean, val_mean):
    marker = " <- Day 2 choice" if n == 22 else ""
    print(f"max_leaf_nodes={n:>3}: train={tm:.4f}, val={vm:.4f}, gap={tm-vm:.4f}{marker}")

best_idx = val_mean.argmax()
print(f"\nPeak validation score at max_leaf_nodes={leaf_range[best_idx]}: {val_mean[best_idx]:.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(leaf_range, train_mean, "o-", label="Train")
ax.fill_between(leaf_range, train_mean - train_std, train_mean + train_std, alpha=0.2)
ax.plot(leaf_range, val_mean, "o-", label="Validation")
ax.fill_between(leaf_range, val_mean - val_std, val_mean + val_std, alpha=0.2)
ax.axvline(22, color="gray", linestyle="--", label="Day 2 choice (22)")
ax.set_title("Validation curve — max_leaf_nodes (HistGradientBoosting)")
ax.set_xlabel("max_leaf_nodes")
ax.set_ylabel("ROC-AUC")
ax.legend()
plt.tight_layout()
plt.savefig("results/validation_curve_max_leaf_nodes.png", dpi=150)
plt.close()
print("Saved results/validation_curve_max_leaf_nodes.png")

# Validation curve for learning_rate
lr_range = [0.005, 0.01, 0.02, 0.0383, 0.05, 0.1, 0.2, 0.3]
train_scores_lr, val_scores_lr = validation_curve(
    hgb_pipeline, X_dev, y_dev, param_name="model__learning_rate",
    param_range=lr_range, cv=cv, scoring="roc_auc", n_jobs=-1
)
train_mean_lr, val_mean_lr = train_scores_lr.mean(axis=1), val_scores_lr.mean(axis=1)

print("\n=== Validation curve: learning_rate ===")
for lr, tm, vm in zip(lr_range, train_mean_lr, val_mean_lr):
    marker = " <- Day 2 choice" if abs(lr - 0.0383) < 0.001 else ""
    print(f"learning_rate={lr:.4f}: train={tm:.4f}, val={vm:.4f}, gap={tm-vm:.4f}{marker}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(lr_range, train_mean_lr, "o-", label="Train")
ax.plot(lr_range, val_mean_lr, "o-", label="Validation")
ax.axvline(0.0383, color="gray", linestyle="--", label="Day 2 choice")
ax.set_xscale("log")
ax.set_title("Validation curve — learning_rate (HistGradientBoosting)")
ax.set_xlabel("learning_rate (log scale)")
ax.set_ylabel("ROC-AUC")
ax.legend()
plt.tight_layout()
plt.savefig("results/validation_curve_learning_rate.png", dpi=150)
plt.close()
print("Saved results/validation_curve_learning_rate.png")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 4, Block 2 — Validation Curves\n\n")
    f.write(f"- max_leaf_nodes peak at {leaf_range[best_idx]}: {val_mean[best_idx]:.4f}\n")
    f.write(f"- Day 2's choice of 22 for max_leaf_nodes: {'near peak' if abs(leaf_range[best_idx]-22)<=15 else 'not at peak, consider adjusting'}\n")