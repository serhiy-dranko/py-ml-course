import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

X_dev = pd.read_parquet("X_dev_engineered.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Point 1: filter step — drop constant/near-constant columns
constant_cols = [c for c in X_dev.columns if X_dev[c].nunique() <= 1]
print("Constant columns to drop:", constant_cols)

# Drop one of each highly correlated numeric pair (threshold 0.95)
corr_matrix = X_dev[numeric_cols].corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
high_corr_drop = [col for col in upper.columns if any(upper[col] > 0.95)]
print(f"Highly correlated columns to drop ({len(high_corr_drop)}):", high_corr_drop[:10], "..." if len(high_corr_drop) > 10 else "")

filtered_numeric = [c for c in numeric_cols if c not in constant_cols and c not in high_corr_drop]

pipe_filtered = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", filtered_numeric),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(random_state=42)),
])
results_filtered = cross_validate(pipe_filtered, X_dev, y_dev, cv=cv, scoring="roc_auc")
print(f"\nHGB after filtering: {results_filtered['test_score'].mean():.4f} ± {results_filtered['test_score'].std():.4f}")
print("(compare to HGB ordinal from Block 4: 0.7488 ± 0.0089)")

# Point 2: L1-regularized logistic regression as embedded selector
pipe_l1 = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))]), categorical_cols),
    ])),
    ("model", LogisticRegression(max_iter=5000, C=0.1, penalty="l1", solver="liblinear")),
])
pipe_l1.fit(X_dev, y_dev)
coefs = pipe_l1.named_steps["model"].coef_[0]
n_survived = (coefs != 0).sum()
print(f"\nL1 logistic regression: {n_survived} of {len(coefs)} features survived (non-zero coefficient)")

# Point 3: permutation importance for HGB
X_train_perm, X_val_perm, y_train_perm, y_val_perm = train_test_split(
    X_dev, y_dev, test_size=0.2, random_state=42, stratify=y_dev
)
hgb_for_perm = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", numeric_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(random_state=42)),
])
hgb_for_perm.fit(X_train_perm, y_train_perm)

perm_result = permutation_importance(
    hgb_for_perm, X_val_perm, y_val_perm, scoring="roc_auc", n_repeats=5, random_state=42, n_jobs=-1
)
perm_df = pd.DataFrame({
    "feature": X_val_perm.columns,
    "importance_mean": perm_result.importances_mean,
}).sort_values("importance_mean", ascending=False)

print("\nTop 15 features by permutation importance:")
print(perm_df.head(15).to_string(index=False))

engineered_features = ["DAYS_EMPLOYED_ANOM", "AGE_YEARS", "EMPLOYED_YEARS", "CREDIT_INCOME_RATIO",
                        "ANNUITY_INCOME_RATIO", "CREDIT_GOODS_RATIO", "ANNUITY_CREDIT_RATIO",
                        "EXT_SOURCE_MEAN", "EXT_SOURCE_MIN", "DOCUMENT_COUNT"]
engineered_in_top15 = [f for f in perm_df.head(15)["feature"] if f in engineered_features]
print(f"\nEngineered features appearing in top 15: {engineered_in_top15}")

# Point 4: score vs top-N features
print("\n=== Score vs. top-N features ===")
n_values = [10, 20, 30, 50, 80, len(perm_df)]
scores_by_n = []
for n in n_values:
    top_n_features = perm_df.head(n)["feature"].tolist()
    top_n_numeric = [f for f in top_n_features if f in numeric_cols]
    top_n_categorical = [f for f in top_n_features if f in categorical_cols]

    pipe_topn = Pipeline([
        ("preprocessor", ColumnTransformer([
            ("num", "passthrough", top_n_numeric),
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), top_n_categorical) if top_n_categorical else ("cat", "drop", []),
        ])),
        ("model", HistGradientBoostingClassifier(random_state=42)),
    ])
    results_topn = cross_validate(pipe_topn, X_dev, y_dev, cv=cv, scoring="roc_auc")
    mean_score = results_topn["test_score"].mean()
    scores_by_n.append(mean_score)
    print(f"Top {n} features: {mean_score:.4f} ± {results_topn['test_score'].std():.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(n_values, scores_by_n, marker="o")
ax.set_title("ROC-AUC vs. number of top features kept (HistGradientBoosting)")
ax.set_xlabel("Number of top-N features (by permutation importance)")
ax.set_ylabel("CV ROC-AUC")
plt.tight_layout()
plt.savefig("score_vs_n_features.png", dpi=150)
plt.close()
print("\nSaved score_vs_n_features.png")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 3, Block 5 — Feature Selection\n\n")
    f.write(f"- Constant columns dropped: {constant_cols}\n")
    f.write(f"- Highly correlated columns dropped: {len(high_corr_drop)}\n")
    f.write(f"- HGB after filtering: {results_filtered['test_score'].mean():.4f} ± {results_filtered['test_score'].std():.4f}\n")
    f.write(f"- L1 logistic regression: {n_survived}/{len(coefs)} features survived\n")
    f.write(f"- Engineered features in top 15 by permutation importance: {engineered_in_top15}\n")