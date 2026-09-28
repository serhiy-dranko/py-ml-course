# Week 4, Day 1 — Write-Up: Cross-Validation and Project Kickoff

## 1. Business Problem and Metrics

A credit analyst at Home Credit uses this model's output to rank loan applications
by predicted default risk, prioritizing which applications get closer manual
review and at what price. Approving a defaulting client costs far more than
declining a repaying one, so the model must rank risky applicants highly, not
just be "usually right." With TARGET at 8.07% default / 91.93% repay, **ROC-AUC**
is the primary metric (ranking quality independent of class balance) and
**PR-AUC** (average_precision) is the secondary check, since it's more sensitive
to minority-class performance specifically. Accuracy is explicitly rejected as a
headline metric: a model predicting "repays" for everyone scores 91.93% accuracy
while catching zero risky clients.

## 2. Split Design and Leakage Findings

Two-layer split: a locked 20% test set (61,503 rows, stratified, untouched until
Day 4) plus an 80% working set for all experimentation. A 50,000-row stratified
development subsample was carved from the working set for fast iteration. Class
balance held consistent across all four sets (~8.07% everywhere). Leakage audit:
`SK_ID_CURR` was dropped as a pure identifier with no predictive signal; no other
column was found to leak the outcome or post-date the application.

## 3. Top Data Quality Issues Found

1. **DAYS_EMPLOYED placeholder anomaly** — 55,374 rows (18% of the dataset) carry
   the value 365243 instead of a real negative day-count, almost certainly a
   sentinel for "not currently employed" rather than genuine data. Planned
   treatment: convert to NaN inside the pipeline (not permanently now), so
   imputation handles it per-fold.
2. **Housing-detail columns ~66-70% missing** (`COMMONAREA_*`, `NONLIVINGAPARTMENTS_*`,
   `LIVINGAPARTMENTS_*`, `YEARS_BUILD_*`) — likely optional fields most applicants
   didn't provide. Planned treatment: median/mode imputation inside the pipeline
   as a first pass; consider dropping the sparsest if they add no signal in Day 3.
3. **ORGANIZATION_TYPE high cardinality** (58 categories) — one-hot encoding
   inflates dimensionality; worth revisiting with target encoding or grouping
   rare categories in Day 3.
4. Memory reduced 31.1% (505MB → 348MB) via safe integer/float downcasting —
   no data quality issue, but material for keeping full-dataset iteration fast.
5. No fully duplicate rows and no duplicate `SK_ID_CURR` values — the identifier
   is confirmed genuinely unique.

## 4. Baseline Results and Noise Floor

| | ROC-AUC | Accuracy |
|---|---|---|
| Dummy baseline | 0.5000 ± 0.0000 | 0.9193 |
| Simple pipeline (val) | 0.7399 ± 0.0098 | 0.9188 |
| Simple pipeline (train) | 0.7573 ± 0.0020 | 0.9192 |

The accuracy trap is directly visible here: dummy and simple-pipeline accuracy are
nearly identical (0.9193 vs 0.9188), which would wrongly suggest the model adds no
value — but ROC-AUC shows the real story (0.50 vs 0.74), a genuine, substantial
ranking improvement accuracy alone completely hides.

**Noise floor:** 10 single splits ranged from 0.7244 to 0.7460 (spread 0.0216),
nearly double the 5-fold CV standard deviation (0.0098). Any single-split score
sits somewhere in that wider range purely by chance — a future change to the
model must move the CV mean by more than ~0.01 to be distinguishable from noise,
not just from a lucky/unlucky split.

## 5. Timings and Day 2 Compute Plan

One fit takes 2.71s on the 50k dev subsample vs. 12.47s on the full 246k working
set. A Day 2 search of 20 hyperparameter candidates × 5 folds on the full working
set is estimated at ~20.8 minutes — the plan is to iterate quickly on the dev
subsample first, then confirm only the most promising candidates on the full
working set to keep total search time manageable.

## 6. Hypotheses for Later Days

- **Hyperparameters to tune (Day 2):** regularization strength (`C`) for logistic
  regression, and comparing against a tree-based model (e.g., gradient boosting)
  which may handle the DAYS_EMPLOYED anomaly and missing data more gracefully
  without explicit preprocessing.
- **Feature ideas (Day 3):** a cleaned `DAYS_EMPLOYED` with the 365243 sentinel
  converted to NaN plus an `is_currently_employed` flag; a debt-to-income style
  ratio from `AMT_CREDIT`/`AMT_INCOME_TOTAL`; grouping `ORGANIZATION_TYPE`'s 58
  categories into a smaller number of broader sectors before encoding.