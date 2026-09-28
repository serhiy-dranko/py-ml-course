import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
import numpy as np

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

numeric_cols = X_working.select_dtypes(include=["int64", "float64", "int32", "float32", "int8", "int16"]).columns.tolist()
categorical_cols = X_working.select_dtypes(include="object").columns.tolist()

hgb_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", "passthrough", numeric_cols),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), categorical_cols),
    ])),
    ("model", HistGradientBoostingClassifier(
        random_state=42, learning_rate=0.0383, max_leaf_nodes=22,
        min_samples_leaf=97, l2_regularization=0.0494,
    )),
])

lr_pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OneHotEncoder(handle_unknown="ignore"))]), categorical_cols),
    ])),
    ("model", LogisticRegression(max_iter=1000, C=0.1)),
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
train_sizes = np.linspace(0.1, 1.0, 6)

def plot_learning_curve(pipeline, name, filename):
    sizes, train_scores, val_scores = learning_curve(
        pipeline, X_working, y_working, cv=cv, scoring="roc_auc",
        train_sizes=train_sizes, n_jobs=-1, random_state=42
    )
    train_mean, train_std = train_scores.mean(axis=1), train_scores.std(axis=1)
    val_mean, val_std = val_scores.mean(axis=1), val_scores.std(axis=1)

    print(f"\n=== {name} learning curve ===")
    for s, tm, vm in zip(sizes, train_mean, val_mean):
        print(f"n={int(s):>7}: train={tm:.4f}, val={vm:.4f}, gap={tm-vm:.4f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, train_mean, "o-", label="Train")
    ax.fill_between(sizes, train_mean - train_std, train_mean + train_std, alpha=0.2)
    ax.plot(sizes, val_mean, "o-", label="Validation")
    ax.fill_between(sizes, val_mean - val_std, val_mean + val_std, alpha=0.2)
    ax.set_title(f"Learning curve — {name}")
    ax.set_xlabel("Training set size")
    ax.set_ylabel("ROC-AUC")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"results/{filename}", dpi=150)
    plt.close()
    print(f"Saved results/{filename}")

    final_gap = train_mean[-1] - val_mean[-1]
    still_rising = val_mean[-1] - val_mean[-2] > 0.001
    return final_gap, still_rising

hgb_gap, hgb_rising = plot_learning_curve(hgb_pipeline, "HistGradientBoosting", "learning_curve_hgb.png")
lr_gap, lr_rising = plot_learning_curve(lr_pipeline, "LogisticRegression", "learning_curve_lr.png")

diagnosis = f"""
LEARNING CURVE DIAGNOSIS:

HistGradientBoosting: final train/val gap = {hgb_gap:.4f}. {"Still rising" if hgb_rising else "Plateaued"} at max size.
{"This gap suggests mild overfitting, consistent with Day 2's finding that top HGB candidates showed train/val gaps." if hgb_gap > 0.03 else "Gap is modest — model is reasonably balanced, not severely overfitting."}
{"More data would likely help further, since validation score is still climbing." if hgb_rising else "Validation score has plateaued — more data alone is unlikely to help much further; better features or a different model family would matter more."}

LogisticRegression: final train/val gap = {lr_gap:.4f}. {"Still rising" if lr_rising else "Plateaued"} at max size.
Small gap suggests the model is closer to underfitting (limited by its linear form)
than overfitting — a more flexible model captures more signal, as already shown
by HGB's higher scores across the week.
"""
print(diagnosis)

with open("decision_log.md", "a") as f:
    f.write("\n## Day 4, Block 1 — Learning Curves\n\n")
    f.write(diagnosis)