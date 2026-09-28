import pandas as pd
import time
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

preprocessor = ColumnTransformer(transformers=[
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_cols),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

param_grid = {
    "model__C": [0.001, 0.01, 0.1, 1, 10],
    "model__class_weight": [None, "balanced"],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

start = time.perf_counter()
grid_search = GridSearchCV(pipeline, param_grid, scoring="roc_auc", cv=cv, n_jobs=-1)
grid_search.fit(X_dev, y_dev)
elapsed = time.perf_counter() - start

print(f"Grid search took {elapsed:.1f}s")
print(f"\nBest params: {grid_search.best_params_}")
print(f"Best CV ROC-AUC: {grid_search.best_score_:.4f}")

# Point 2: inspect cv_results_
results_df = pd.DataFrame(grid_search.cv_results_)
results_df = results_df.sort_values("rank_test_score")
print("\nTop 10 candidates:")
print(results_df[["params", "mean_test_score", "std_test_score", "rank_test_score"]].head(10).to_string())

# Point 3: edge-of-grid check
best_C = grid_search.best_params_["model__C"]
c_values = param_grid["model__C"]
if best_C == c_values[0] or best_C == c_values[-1]:
    print(f"\nWARNING: best C ({best_C}) is at the edge of the grid {c_values} — consider extending it.")
else:
    print(f"\nBest C ({best_C}) is not at the edge of the grid — range looks adequate.")

# Point 4: improvement over untuned baseline
untuned_score = 0.7399  # from Day 1 / Block 1 reproduction
improvement = grid_search.best_score_ - untuned_score
print(f"\nImprovement over untuned baseline: {improvement:.4f}")
print("(Day 1 5-fold CV std was 0.0098 — improvement should be compared against this noise floor)")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 3 — Grid Search on Logistic Regression\n\n")
    f.write(f"- Best params: {grid_search.best_params_}\n")
    f.write(f"- Best CV ROC-AUC: {grid_search.best_score_:.4f}\n")
    f.write(f"- Time: {elapsed:.1f}s\n")
    f.write(f"- Improvement over untuned: {improvement:.4f} (noise floor ~0.0098)\n")

import joblib
joblib.dump(grid_search.best_estimator_, "best_logistic_regression.pkl")
print("\nSaved best_logistic_regression.pkl")