import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from scipy.stats import loguniform

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

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Equal budget: 10 candidates each
grid = {"model__C": [0.001, 0.01, 0.1, 1, 10], "model__class_weight": [None, "balanced"]}  # 10 combos
grid_search = GridSearchCV(pipeline, grid, scoring="roc_auc", cv=cv, n_jobs=-1)
grid_search.fit(X_dev, y_dev)

random_dist = {"model__C": loguniform(0.0001, 100), "model__class_weight": [None, "balanced"]}
random_search = RandomizedSearchCV(pipeline, random_dist, n_iter=10, scoring="roc_auc", cv=cv, random_state=42, n_jobs=-1)
random_search.fit(X_dev, y_dev)

print(f"Grid search best: {grid_search.best_score_:.4f} with {grid_search.best_params_}")
print(f"Random search best: {random_search.best_score_:.4f} with {random_search.best_params_}")

# Best-score-so-far plot
grid_scores = pd.DataFrame(grid_search.cv_results_)["mean_test_score"].values
random_scores = pd.DataFrame(random_search.cv_results_)["mean_test_score"].values

grid_running_best = np.maximum.accumulate(grid_scores)
random_running_best = np.maximum.accumulate(random_scores)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(range(1, len(grid_running_best) + 1), grid_running_best, label="Grid search", marker="o")
ax.plot(range(1, len(random_running_best) + 1), random_running_best, label="Random search", marker="s")
ax.set_title("Best-score-so-far: grid vs. random search at equal budget (10 candidates)")
ax.set_xlabel("Candidates evaluated")
ax.set_ylabel("Best ROC-AUC so far")
ax.legend()
plt.tight_layout()
plt.savefig("grid_vs_random.png", dpi=150)
plt.close()
print("\nSaved grid_vs_random.png")

# One-standard-error rule
results_df = pd.DataFrame(grid_search.cv_results_).sort_values("rank_test_score")
best_score = results_df.iloc[0]["mean_test_score"]
best_std = results_df.iloc[0]["std_test_score"]
threshold = best_score - best_std
near_ties = results_df[results_df["mean_test_score"] >= threshold]
print(f"\nCandidates within one std of the best ({threshold:.4f}):")
print(near_ties[["params", "mean_test_score", "std_test_score"]].to_string())
print("\nAmong these near-ties, prefer the simplest/cheapest — for logistic regression,")
print("that typically means the smallest C (strongest regularization, simplest model).")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 2, Block 5 — Grid vs Random at Equal Budget\n\n")
    f.write(f"- Grid search best: {grid_search.best_score_:.4f}\n")
    f.write(f"- Random search best: {random_search.best_score_:.4f}\n")