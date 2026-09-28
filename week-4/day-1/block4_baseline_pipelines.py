import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

X_dev = pd.read_parquet("X_dev.parquet")
y_dev = pd.read_parquet("y_dev.parquet").iloc[:, 0]

numeric_cols = X_dev.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_dev.select_dtypes(include="object").columns.tolist()

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = ["roc_auc", "average_precision", "accuracy"]

# Point 1: dummy baseline
dummy = DummyClassifier(strategy="prior")
dummy_results = cross_validate(dummy, X_dev, y_dev, cv=cv, scoring=scoring)

print("=== Dummy baseline ===")
for metric in scoring:
    scores = dummy_results[f"test_{metric}"]
    print(f"{metric}: {scores.mean():.4f} ± {scores.std():.4f}")

# Point 2: simple pipeline baseline
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

simple_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])
# Point 3: score with return_train_score=True
simple_results = cross_validate(
    simple_pipeline, X_dev, y_dev, cv=cv, scoring=scoring, return_train_score=True
)

print("\n=== Simple pipeline baseline ===")
for metric in scoring:
    val_scores = simple_results[f"test_{metric}"]
    train_scores = simple_results[f"train_{metric}"]
    print(f"{metric}: val {val_scores.mean():.4f} ± {val_scores.std():.4f} | train {train_scores.mean():.4f} ± {train_scores.std():.4f}")

# Point 5: dummy accuracy vs ROC-AUC comparison
dummy_acc = dummy_results["test_accuracy"].mean()
dummy_auc = dummy_results["test_roc_auc"].mean()
print(f"\nDummy accuracy ({dummy_acc:.3f}) looks deceptively high, but its ROC-AUC ({dummy_auc:.3f}) reveals it has zero real ranking ability.")

with open("decision_log.md", "a") as f:
    f.write("\n## Day 1, Block 4 — Baseline Results\n\n")
    f.write(f"- Dummy baseline: ROC-AUC {dummy_results['test_roc_auc'].mean():.4f} ± {dummy_results['test_roc_auc'].std():.4f}, accuracy {dummy_acc:.4f}\n")
    f.write(f"- Simple pipeline: ROC-AUC {simple_results['test_roc_auc'].mean():.4f} ± {simple_results['test_roc_auc'].std():.4f}\n")
