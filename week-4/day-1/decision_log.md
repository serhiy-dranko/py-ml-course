# Week 4 Decision Log

## Day 1

- Loaded application_train.csv: shape (307511, 122)
- Class balance: {0: 91.92711805431351, 1: 8.072881945686495}

PROBLEM STATEMENT:
A credit analyst at Home Credit uses this model's output to rank loan applications
by predicted default risk before a human makes the final approve/decline/price
decision. The decision this model drives is not "approve everyone the model likes"
but "prioritize which applications get closer manual review and at what price."
Approving a client who later defaults is far costlier than declining a client who
would have repaid (a lost interest-bearing loan vs a lost customer who could
reapply or go elsewhere). So a useful model must rank risky applicants highly
enough to catch most defaults, not just be "usually right" overall.

METRIC JUSTIFICATION:
TARGET is heavily imbalanced (8.1% default, 91.9% repay).
Accuracy is misleading: a model predicting "repays" for every applicant would score
91.9% accuracy while providing zero decision value. ROC-AUC
measures ranking quality across all thresholds regardless of class balance, making
it the primary metric; PR-AUC is tracked as a secondary check since it's more
sensitive to performance on the minority (default) class specifically.


## Day 1, Block 2 — Quality Audit

- Memory: 504.99 MB -> 348.09 MB after downcasting
- Duplicate rows: 0, duplicate SK_ID_CURR: 0
- DAYS_EMPLOYED anomaly: 55374 rows with positive values (likely a 365243 placeholder) — planned treatment: convert to NaN inside the pipeline, not permanently now.

## Day 1, Block 3 — Leakage Audit and Split Design

- Dropped SK_ID_CURR (pure identifier, no predictive signal)
- Locked test set: (61503, 120), saved to X_test.parquet/y_test.parquet, untouched until Day 4
- Development subsample: (50000, 120), saved for fast iteration
- Class balance held consistent: full=0.0807, working=0.0807, test=0.0807, dev=0.0807

## Day 1, Block 4 — Baseline Results

- Dummy baseline: ROC-AUC 0.5000 ± 0.0000, accuracy 0.9193
- Simple pipeline: ROC-AUC 0.7399 ± 0.0098

## Day 1, Block 4 — Baseline Results

- Dummy baseline: ROC-AUC 0.5000 ± 0.0000, accuracy 0.9193
- Simple pipeline: ROC-AUC 0.7399 ± 0.0098

## Day 1, Block 5 — Split Noise vs CV

- 10 single splits: min=0.7244, max=0.7460
- 5-fold CV: 0.7399 ± 0.0098
- Repeated 5-fold x3: 0.7394 ± 0.0068
- Dev fit time: 2.71s, Working set fit time: 12.47s
- Estimated Day 2 search cost (20 candidates x 5 folds): ~20.8 min
