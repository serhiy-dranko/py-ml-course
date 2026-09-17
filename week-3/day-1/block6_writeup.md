# Week 3, Day 1  Write-Up: Regression vs Classification

## 1. Both Datasets, Targets and Problem Type Labels

**Insurance dataset** (1338 rows, 7 columns) our target column: `charges` (dtype `float64`).
Labeled **REGRESSION**: `charges` is a continuous dollar amount. Its mean (13,270.42)
is directly meaningful as "the average cost billed per policyholder" — the value can take any point along a continuous range, and averaging it produces a real number.

**Titanic dataset** (891 rows, 12 columns) our target column: `Survived` (dtype `int64`, values 0/1). 
Labeled **CLASSIFICATION**: `Survived` is a discrete category, not a
quantity. 
Its mean (0.38) is only meaningful as a survival *rate* (38% of passengers survived). There is no such thing as a passenger who is "38% alive," so the target itself fails the "can this be sensibly averaged into a real value" test from today's concepts.

## 2. Feature/Target Splits Built

**Insurance:**
- `X_reg` shape: (1338, 6) — age, sex, bmi, children, smoker, region
- `y_reg` shape: (1338,) — charges

**Titanic:**
- `X_clf` shape: (891, 7) — Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
- `y_clf` shape: (891,)  Survived
- Dropped `PassengerId`, `Name`, `Ticket`, `Cabin`, `Survived` from features (see below)

Confirmed the classic single-vs-double-bracket shape trap: `df['age']` returns a
1D Series `(1338,)`, while `df[['age']]` returns a 2D DataFrame `(1338, 1)` scikit-learn's `.fit()` requires the 2D shape for X even with a single feature.

## 3. Columns to Drop or Transform Before Modeling

- **`PassengerId`** (titanic) — pure row identifier, unique per row, carries zero
  predictive signal. Drop entirely.
- **`Cabin`** (titanic) — 687 of 891 values missing (~77%). Too sparse to reliably
  impute; likely drop entirely, or transform into a coarser "deck known / unknown"
  binary flag if revisited later.
- **`Name`** (titanic) — free text, not usable as-is, but could be transformed later
  into a "title" feature (Mr/Mrs/Miss/Master) that may carry real signal about age and social class.
- **`region`** (insurance) — not dropped, but worth flagging: it's a true low-cardinality
  categorical (4 values) that will need encoding (e.g., one-hot) before any model can use it because it's currently text.

## 4. Open Question Heading Into Day 2

The biggest open question: **how should the 177 missing `Age` values in titanic be handled?
** Dropping those rows would lose ~20% of the dataset a meaningful chunk.
Filling with the median is the obvious first candidate, but `Age` correlates with`Pclass` in real-world intuition (wealthier passengers skew older in some cohorts). Tat is a single global median might be less accurate than filling per-`Pclass` groupmedians. This feels like exactly the kind of domain informed missing data decision Day 2 concepts doc will likely address directly.