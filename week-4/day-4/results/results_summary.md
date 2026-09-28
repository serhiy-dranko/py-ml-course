# Home Credit Default Risk: Final Results Summary

Source key: D1 B5 = Day 1, Block 5, and so on. CV = stratified 5-fold ROC-AUC, mean ± std across folds.

## 1. Final result (locked test set, evaluated once)

| Model | Test ROC-AUC | Test PR-AUC | Test accuracy |
|---|---|---|---|
| Dummy (class prior) | 0.5000 | about 0.081 (equals class prevalence) | 0.9193 |
| Simple logistic regression (default settings, raw features) | 0.7509 | not computed | not computed |
| **Final model** (HistGradientBoosting, engineered features, re-tuned) | **0.7618** | **0.2526** | 0.9195 |

Test log-loss of the final model: 0.2451. Source: D4 B4.

- The final model beats the dummy by 0.262 ROC-AUC and the simple baseline by 0.011. Accuracy is almost identical for dummy and final model (0.9193 vs 0.9195), which is why accuracy was rejected as the headline metric.
- The test AUC is a single estimate on 61,503 rows (4,965 defaulters). We did not compute a confidence interval for it, so differences of a few thousandths should not be over-read.

## 2. Progress across the week

| Stage | CV ROC-AUC (dev subsample, 50k rows) | Source |
|---|---|---|
| Dummy | 0.5000 | D1 B4 |
| Simple logistic regression | 0.7399 ± 0.0098 | D1 B4 |
| HGB, untuned, raw features | 0.7387 ± 0.0112 | D2 B1 |
| HGB, tuned, raw features | 0.7458 ± 0.0108 | D2 B4 |
| HGB, tuned (Day 2 settings) + engineered features | 0.7516 ± 0.0096 | D3 B6 |
| HGB, re-tuned + engineered features (frozen) | 0.7533 ± 0.0086 | D4 B3 |

Confirmation on the full working set (246,008 rows), where fold noise is much lower:

| Model | CV ROC-AUC | Source |
|---|---|---|
| Logistic regression, tuned, raw features | 0.7442 ± 0.0032 | D2 B6 |
| HGB, tuned, raw features | 0.7499 ± 0.0025 | D2 B6 |
| HGB, tuned (Day 2 settings) + engineered features | 0.7555 ± 0.0016 | D3 B6 |

The Day 4 re-tuned configuration was scored only on the dev subsample, so the full-working-set number that is comparable to the test score is 0.7555, not 0.7533.

### What contributed how much

On the dev subsample the steps added +0.0071 (tuning), +0.0058 (features) and +0.0017 (re-tune). The order matters: engineered features added +0.0101 to the *untuned* HGB (0.7387 to 0.7488, D3 B2). The fold std on dev is about 0.009 to 0.011, so none of these single steps is clearly separated from noise on dev alone. Two things are better supported:

- On the full working set (std 0.0016 to 0.0025), moving from tuned-raw (0.7499) to tuned-plus-features (0.7555) is +0.0056, larger than that std. The feature gain is credible.
- The Day 4 re-tune (+0.0017) is not distinguishable from noise. It is also the best of 20 candidates, so it is optimistically biased. The top five candidates spanned 0.7517 to 0.7533.

We do not claim that features mattered more than tuning; the evidence shows both helped by comparable amounts.

### Test vs. CV

The test AUC (0.7618) is above the comparable CV estimate (0.7555), by 0.0063. The simple logistic regression shows a similar offset (test 0.7509 vs. full-working-set CV 0.7442, +0.0067, though the two used slightly different settings). A shift of similar size for both models points to the test split being slightly easier by chance rather than to anything model-specific, and gives no sign of leakage. This is a consistency check, not proof.

## 3. Evaluation design

A locked 20% stratified test set was created on Day 1 and loaded once, on Day 4. All experiments used the 80% working set with stratified 5-fold CV, and a 50,000-row stratified dev subsample for fast iteration. Class balance was the same in every split (about 8.07%). `SK_ID_CURR` was dropped as a pure identifier.

Ten single 80/20 splits of the dev subsample gave ROC-AUC from 0.7244 to 0.7460 (range 0.0216, standard deviation about 0.0066 across the ten scores; D1 B5). The per-fold std of 5-fold CV is 0.0098. These are different statistics, so the range should not be compared with the std directly. The practical point is that any single split can land 0.01 to 0.02 away from the average, while a CV mean averages five folds, so its standard error is smaller (roughly 0.0098 divided by the square root of 5, about 0.004; approximate because the folds share training data).

## 4. Diagnosis

- **Learning curves (D4 B1).** HGB train/validation gap fell from 0.117 to 0.014 as training size grew, and the validation score plateaued at about 0.7555 (0.7554 to 0.7555 over the last step). More data alone is unlikely to help much. Logistic regression plateaued at 0.748 with a gap of only 0.003, so it is limited by its linear form rather than by data.
- **Validation curve (D4 B2).** Validation ROC-AUC was highest at `max_leaf_nodes = 22` (0.7516), but 15 to 45 leaves scored within 0.0007 of it, so this is a broad flat region rather than a sharp peak. The train/validation gap grew from 0.012 (5 leaves) to 0.198 (127 leaves), showing overfitting beyond that range. Learning rates from 0.02 to 0.1 also scored within about 0.006.

## 5. Threshold decision (with a caveat)

We assumed a missed defaulter costs 5 times a wrongly declined client. That ratio is our assumption, not Home Credit's figure. Minimizing that cost gave threshold 0.163, with precision 0.267, recall 0.382 and confusion matrix [[51,329, 5,209], [3,071, 1,894]] (D4 B5).

**Caveat:** this threshold was chosen on the test set, which breaks the rule that the test set is used once. ROC-AUC and the lift table do not depend on the threshold, but precision and recall at 0.163 are somewhat optimistic. A proper choice would use out-of-fold predictions on the working set. As a sanity check, if the probabilities are calibrated (not verified), the cost-optimal threshold for a 5:1 ratio is 1/(1+5) = 0.167, close to what we found.

## 6. Lift

On the test set, the top predicted-risk decile has a 28.0% default rate (lift 3.47 over the 8.07% overall rate) and the bottom decile 1.27% (lift 0.16). Default rate decreases at every decile, and deciles depend only on ranking, not on the chosen threshold. This is the most business-readable result.

## 7. Drivers

Permutation importance on the test set (D4 B5): `EXT_SOURCE_MEAN` (0.109) is about 9 times the next feature `ANNUITY_CREDIT_RATIO` (0.012). On the dev subsample in Day 3 it was about 15 times the next one. Six of the top 15 features are engineered ones, including `CREDIT_GOODS_RATIO`, `EXT_SOURCE_MIN` and `AGE_YEARS`.

Two cautions. `EXT_SOURCE_1/2/3`, `EXT_SOURCE_MEAN` and `EXT_SOURCE_MIN` carry overlapping information, and permutation importance spreads credit unevenly across correlated features, so the size of the `EXT_SOURCE_MEAN` gap partly reflects that it summarizes three columns. Importance also describes what the model uses, not what causes default.

## 8. Other experiments and how far to trust them

- **Leakage demo (D3 B3).** Target encoding, imputation and scaling fit on all rows before CV scored 0.7416 vs. 0.7371 inside a Pipeline (gap 0.0045). This is a single run, the gap is smaller than the fold std (about 0.009), and the two versions differ in more than leakage (for example, cross-fitted smoothing in `TargetEncoder`). It is consistent with leakage inflation but does not measure its size. Plain one-hot encoding scored higher than both (0.7458).
- **Scaling (D3 B4).** Logistic regression without scaling scored 0.6381 and hit convergence warnings at 1,000 iterations, so this mainly shows a failure to converge.
- **Feature filtering (D3 B5).** Dropping constant and highly correlated columns scored 0.7459 vs. 0.7488 without it. The difference is within noise; there is no evidence filtering helps, so all features were kept.
- **Encodings (D3 B4).** Ordinal vs. one-hot for HGB (0.7488 vs. 0.7470) and grouped vs. ungrouped rare categories for logistic regression (0.7457 vs. 0.7458) are not distinguishable.
- **Confident mistakes (D4 B5).** The ten most confident errors were all missed defaulters (predicted probability about 0.015 to 0.017). With 92% non-defaulters this is expected mechanically. Explanations such as job loss are hypotheses we did not test.

## 9. Limitations

- Only `application_train.csv` was used; bureau, previous-application and installment tables likely add signal.
- `CODE_GENDER` is the fifth most important feature. Using gender in credit decisions raises fair-lending concerns and would need legal review before any deployment.
- One data snapshot: behavior under other economic conditions is untested.
- The threshold and its precision/recall come from the test set, and the 5:1 cost ratio is assumed.
- The test AUC has no confidence interval, and probability calibration was not checked.
- The Day 4 re-tune was evaluated only on the 50k dev subsample.

