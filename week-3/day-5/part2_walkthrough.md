# Week 3 Walkthrough. Supervised Learning: Regression vs Classification

## The Two Problems

**Insurance cost prediction (regression):** predicting `charges` it's a continuous
dollar amount. I knew it was regression because the target passes the "can it be
sensibly averaged?" test: the mean charge ($13,270) is a real, interpretable
number representing a typical cost.

**Titanic survival prediction (classification):** predicting `Survived` this a
discrete 0/1 label. Averaging it only produces a survival *rate* (38%), not a
meaningful "typical passenger".Thr clear signal this is classification, not
regression, despite both starting from the exact same `fit`/`predict`/`score`
shape in scikit-learn.

## Final Metrics, Plain Language

**Regression model:** typically off by about **$5,796** per prediction (RMSE),
explaining **78.4%** of the variation in medical costs (R²). Compared to a
"always guess the average cost" baseline (which would be off by $12,466), this
model cuts the typical error by more than half. This is real, meaningful signal was
learned from age, BMI, smoking status and the rest.

**Classification model:** correct **80.4%** of the time overall. Clearly beating
the "always guess the most common outcome" baseline of 61.5%. But two more
specific numbers matter more than that single accuracy figure: when this model
says "this passenger survived," it's right **79.3%** of the time (precision); but
of everyone who actually survived, it only catches **66.7%** of them (recall)
it systematically misses about a third of real survivors.

## The Most Illustrative Moment

The threshold experiment on Day 4 was the clearest "aha" of the week: lowering the
decision cutoff from 0.5 to 0.35 flipped precision and recall in exactly opposite
directions (precision 0.793→0.692, recall 0.667→0.783). Using the *exact same
model*, with *no retraining at all*. It made concrete something that's easy to
nod along to in theory but only really lands when you see it happen to your own
numbers: `.predict()` isn't a fixed fact about a model. It's a probability plus a
threshold you get to choose based on which mistake costs more.

## The One Habit Worth Keeping

**Never trust a score without comparing it to a baseline.** An 80.4% accuracy
sounds impressive in isolation but next to a 61.5% "do-nothing" baseline, it's a
real but more modest win than the raw number suggests. This single habit wich always
asking "compared to what?". Is the one idea that ties every day of this week
together, from the train/test split (compared to training performance) to RMSE
(compared to a mean-prediction baseline) to accuracy (compared to majority-class
guessing).