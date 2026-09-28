import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split, StratifiedKFold, RepeatedStratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]
X_working = pd.read_parquet("X_working.parquet")
y_working = pd.read_parquet("y_working.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

def build_pipeline():
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
    return Pipeline([
        ("preprocessor", preprocessor),
        ("model", LogisticRegression(max_iter=1000)),
    ])

# Point 1: 10 different single splits
single_split_scores = []
for seed in range(10):
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_dev, y_dev, test_size=0.2, random_state=seed, stratify=y_dev
    )
    pipe = build_pipeline()
    pipe.fit(X_tr, y_tr)
    proba = pipe.predict_proba(X_val)[:, 1]
    score = roc_auc_score(y_val, proba)
    single_split_scores.append(score)
    print(f"Seed {seed}: ROC-AUC = {score:.4f}")

single_split_scores = np.array(single_split_scores)
print(f"\nSingle-split scores: min={single_split_scores.min():.4f}, max={single_split_scores.max():.4f}, spread={single_split_scores.max()-single_split_scores.min():.4f}")

# Point 2: compare with 5-fold CV
cv5 = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv5_results = cross_validate(build_pipeline(), X_dev, y_dev, cv=cv5, scoring="roc_auc")
cv5_scores = cv5_results["test_score"]
print(f"\n5-fold CV: mean={cv5_scores.mean():.4f} ± {cv5_scores.std():.4f}")

print(f"""
Comparison: the 10 single-split scores span a range of {single_split_scores.max()-single_split_scores.min():.4f},
while the 5-fold CV std is only {cv5_scores.std():.4f}. A single split can land anywhere within that
wider spread purely by chance depending on which rows happened to fall into validation —
so any single-split score is not, by itself, a reliable estimate of true model performance.
""")

# Point 3: RepeatedStratifiedKFold
rcv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
rcv_results = cross_validate(build_pipeline(), X_dev, y_dev, cv=rcv, scoring="roc_auc")
rcv_scores = rcv_results["test_score"]
print(f"Repeated 5-fold x3: mean={rcv_scores.mean():.4f} ± {rcv_scores.std():.4f}")
print(f"Plain 5-fold:       mean={cv5_scores.mean():.4f} ± {cv5_scores.std():.4f}")

# Point 4: timing
start = time.perf_counter()
build_pipeline().fit(X_dev, y_dev)
dev_fit_time = time.perf_counter() - start
print(f"\nOne fit on dev subsample ({len(X_dev)} rows): {dev_fit_time:.2f}s")

start = time.perf_counter()
build_pipeline().fit(X_working, y_working)
working_fit_time = time.perf_counter() - start
print(f"One fit on full working set ({len(X_working)} rows): {working_fit_time:.2f}s")

candidates = 20
folds = 5
estimated_cost = candidates * folds * working_fit_time
print(f"\nEstimated cost for a Day 2 search of {candidates} candidates x {folds} folds on full working set: {estimated_cost:.1f}s (~{estimated_cost/60:.1f} min)")

# Point 5: plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(range(10), single_split_scores, label="10 single splits", color="#888888")
ax.axhline(cv5_scores.mean(), color="#4C72B0", label=f"5-fold CV mean ({cv5_scores.mean():.4f})")
ax.fill_between(range(10), cv5_scores.mean() - cv5_scores.std(), cv5_scores.mean() + cv5_scores.std(),
                 color="#4C72B0", alpha=0.2, label="±1 std")
ax.set_title("Single-split scores scatter around the more stable CV estimate")
ax.set_xlabel("Split seed")
ax.set_ylabel("ROC-AUC")
ax.legend()
plt.tight_layout()
plt.savefig("split_noise_vs_cv.png", dpi=150)
plt.close()
print("\nSaved split_noise_vs_cv.png")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 1, Block 5 — Split Noise vs CV\n\n")
    f.write(f"- 10 single splits: min={single_split_scores.min():.4f}, max={single_split_scores.max():.4f}\n")
    f.write(f"- 5-fold CV: {cv5_scores.mean():.4f} ± {cv5_scores.std():.4f}\n")
    f.write(f"- Repeated 5-fold x3: {rcv_scores.mean():.4f} ± {rcv_scores.std():.4f}\n")
    f.write(f"- Dev fit time: {dev_fit_time:.2f}s, Working set fit time: {working_fit_time:.2f}s\n")
    f.write(f"- Estimated Day 2 search cost ({candidates} candidates x {folds} folds): ~{estimated_cost/60:.1f} min\n")