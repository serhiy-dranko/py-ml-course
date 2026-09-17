# Block 5 — Matching Metrics to Real-World Questions

1. "On average, how many dollars off will a cost prediction be?"
   → **RMSE** — it's expressed directly in the target's units (dollars), unlike
     R² (a proportion) or any classification metric (which doesn't apply to a
     continuous target at all).

2. "Of the passengers this model flags as survivors, how often is it actually right?"
   → **Precision** — this question is specifically about false positives (flagged
     as survivor but wasn't), which is exactly what precision measures. Recall
     would answer a different question (how many real survivors were caught),
     and accuracy would blend in the "died" predictions too, diluting the answer.

3. "Of all the passengers who actually survived, how many did this model correctly catch?"
   → **Recall** — this is about false negatives (real survivors the model missed),
     which precision doesn't capture at all since precision only looks at what
     was predicted positive, not what was actually positive.

4. "How much of the variation in medical costs does this model explain overall?"
   → **R²** — it directly measures proportion of variance explained on a 0-1
     scale; RMSE answers a related but different question (typical error size
     in dollars), not "how much of the pattern was captured."