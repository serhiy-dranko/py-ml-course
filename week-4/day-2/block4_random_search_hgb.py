import pandas as pd
import time
from scipy.stats import loguniform, randint
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

preprocessor = ColumnTransformer(transformers=[
    ("num", "passthrough", numeric_cols),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", HistGradientBoostingClassifier(random_state=42)),
])

param_distributions = {
    "model__learning_rate": loguniform(0.01, 0.3),
    "model__max_leaf_nodes": randint(15, 127),
    "model__min_samples_leaf": randint(10, 100),
    "model__l2_regularization": loguniform(1e-3, 10),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

start = time.perf_counter()
random_search = RandomizedSearchCV(
    pipeline, param_distributions, n_iter=30, scoring="roc_auc",
    cv=cv, random_state=42, n_jobs=-1, return_train_score=True
)
random_search.fit(X_dev, y_dev)
elapsed = time.perf_counter() - start

print(f"Random search took {elapsed:.1f}s")
print(f"\nBest params: {random_search.best_params_}")
print(f"Best CV ROC-AUC: {random_search.best_score_:.4f}")

# Point 2: inspect cv_results_
results_df = pd.DataFrame(random_search.cv_results_)
results_df = results_df.sort_values("rank_test_score")
print("\nTop 10 candidates:")
print(results_df[["params", "mean_test_score", "std_test_score", "mean_train_score", "rank_test_score"]].head(10).to_string())

# Point 3: overfitting check on top candidates
print("\nTrain vs validation gap for top 10:")
top10 = results_df.head(10)
for idx, row in top10.iterrows():
    gap = row["mean_train_score"] - row["mean_test_score"]
    flag = " <- possible overfit" if gap > 0.03 else ""
    print(f"train={row['mean_train_score']:.4f}, val={row['mean_test_score']:.4f}, gap={gap:.4f}{flag}")

# Point 4: improvement over untuned HGB reference (fill in from Block 1 output)
untuned_hgb_score = 0.7387  
if untuned_hgb_score:
    improvement = random_search.best_score_ - untuned_hgb_score
    print(f"\nImprovement over untuned HGB: {improvement:.4f}")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 4 — Random Search on HistGradientBoosting\n\n")
    f.write(f"- Best params: {random_search.best_params_}\n")
    f.write(f"- Best CV ROC-AUC: {random_search.best_score_:.4f}\n")
    f.write(f"- Time: {elapsed:.1f}s\n")

import joblib
joblib.dump(random_search.best_estimator_, "best_hgb.pkl")
print("\nSaved best_hgb.pkl")