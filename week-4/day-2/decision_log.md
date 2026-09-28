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


## Day 1, Block 2 � Quality Audit

- Memory: 504.99 MB -> 348.09 MB after downcasting
- Duplicate rows: 0, duplicate SK_ID_CURR: 0
- DAYS_EMPLOYED anomaly: 55374 rows with positive values (likely a 365243 placeholder) � planned treatment: convert to NaN inside the pipeline, not permanently now.

## Day 1, Block 3 � Leakage Audit and Split Design

- Dropped SK_ID_CURR (pure identifier, no predictive signal)
- Locked test set: (61503, 120), saved to X_test.parquet/y_test.parquet, untouched until Day 4
- Development subsample: (50000, 120), saved for fast iteration
- Class balance held consistent: full=0.0807, working=0.0807, test=0.0807, dev=0.0807

## Day 1, Block 4 � Baseline Results

- Dummy baseline: ROC-AUC 0.5000 � 0.0000, accuracy 0.9193
- Simple pipeline: ROC-AUC 0.7399 � 0.0098

## Day 1, Block 4 � Baseline Results

- Dummy baseline: ROC-AUC 0.5000 � 0.0000, accuracy 0.9193
- Simple pipeline: ROC-AUC 0.7399 � 0.0098

## Day 1, Block 5 � Split Noise vs CV

- 10 single splits: min=0.7244, max=0.7460
- 5-fold CV: 0.7399 � 0.0098
- Repeated 5-fold x3: 0.7394 � 0.0068
- Dev fit time: 2.71s, Working set fit time: 12.47s
- Estimated Day 2 search cost (20 candidates x 5 folds): ~20.8 min

## Day 2, Block 1 � Reload and Reproduce

- Reproduced LogisticRegression baseline: 0.7399 � 0.0098 (Day 1 was 0.7399 � 0.0098)
- Untuned HistGradientBoostingClassifier reference: 0.7387 � 0.0112

## Day 2, Block 2 � Search Planning

- LogisticRegression: GridSearchCV, 10 candidates x 5 folds, ~2.3 min estimated
- HistGradientBoosting: RandomizedSearchCV, n_iter=30 x 5 folds, ~7.5 min estimated
- Total Day 2 budget target: under 15 minutes for primary searches

## Day 2, Block 3 � Grid Search on Logistic Regression

- Best params: {'model__C': 0.1, 'model__class_weight': None}
- Best CV ROC-AUC: 0.7416
- Time: 55.5s
- Improvement over untuned: 0.0017 (noise floor ~0.0098)

## Day 2, Block 4 � Random Search on HistGradientBoosting

- Best params: {'model__l2_regularization': np.float64(0.04938623547724718), 'model__learning_rate': np.float64(0.03830785929574813), 'model__max_leaf_nodes': 22, 'model__min_samples_leaf': 97}
- Best CV ROC-AUC: 0.7458
- Time: 238.5s

## Day 2, Block 5 � Grid vs Random at Equal Budget

- Grid search best: 0.7416
- Random search best: 0.7416

## Day 2, Block 6 � Full Working Set Confirmation


# Day 2 Summary Table

| Model | Untuned CV | Tuned CV (dev) | Tuned CV (full working) | Search type | Fits |
|---|---|---|---|---|---|
| LogisticRegression | 0.7399 � 0.0098 | see Block 3 output | 0.7442 � 0.0032 | Grid | 10x5 |
| HistGradientBoosting | see Block 1 output | see Block 4 output | 0.7499 � 0.0025 | Random | 30x5 |


