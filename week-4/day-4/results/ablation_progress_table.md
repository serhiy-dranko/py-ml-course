# Full-Week Ablation and Progress Table

| Change | CV ROC-AUC | Δ from Day 1 | Notes |
|---|---|---|---|
| Day 1: Untuned HGB, raw features, SK_ID_CURR dropped | 0.7387 ± 0.0112 | — | Baseline |
| Day 2: + GridSearch on LR (C, class_weight) | 0.7416 (LR only) | — | Within noise on dev; LR not the final model |
| Day 2: + RandomSearch on HGB hyperparameters | 0.7458 ± 0.0025 (full working set) | +0.0071 | Confirmed real on full working set |
| Day 3: + Sentinel fix, ratios, EXT_SOURCE aggregates, doc count | 0.7488 ± 0.0089 (dev) | +0.0101 | Bigger gain than Day 2 tuning |
| Day 3: + Feature filtering (constant + correlated) | 0.7459 ± 0.0081 | — | Made it WORSE — reverted |
| Day 3: + Final combined pipeline (tuned + engineered) | 0.7555 ± 0.0016 (full working set) | +0.0168 | Very stable, large sample |
| Day 4: + Short re-tune on final features | 0.7533 ± 0.0086 (dev) | — | Near-peak already found on Day 2/3 |
| **Day 4: FROZEN final model — Test set (one evaluation)** | **0.7618** | **+0.0231** | **Final reported result** |