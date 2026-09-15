# Week 2 Findings — RAW vs STG Comparison

## Finding 1: Column renaming for join safety
**What changed:** `RAW_CUSTOMERS.ID` → `STG_CUSTOMERS.CUSTOMER_ID`; `RAW_ORDERS.ID` → `STG_ORDERS.ORDER_ID`; `RAW_ORDERS.USER_ID` → `STG_ORDERS.CUSTOMER_ID`; `RAW_ORDERS.STATUS` → `STG_ORDERS.ORDER_STATUS`.
**Likely reason:** dbt gives every generic/ambiguous column an explicit, table-specific name so that joining multiple staging models together never produces naming collisions.
**Impact if not done:** Exactly what we hit ourselves in Day 2 — joining raw tables with identical column names (`ID`) forces pandas to invent `_x`/`_y` suffixes, and it's easy to reference the wrong one by mistake in downstream code.

## Finding 2: Row counts are identical — staging does not filter or dedupe
**What changed:** Nothing — `RAW_CUSTOMERS` (100) = `STG_CUSTOMERS` (100), `RAW_ORDERS` (101) = `STG_ORDERS` (101). See chart 1.
**Likely reason:** This staging layer's job is purely structural cleanup (renaming, typing) — not filtering or deduplication. Both source tables were already clean (0 nulls, 0 duplicate keys), so there was nothing to filter.
**Impact if not done:** N/A here, but this confirms staging isn't hiding row loss — a teammate can trust that `STG_ORDERS` represents literally every order in the source system, not a filtered subset.

## Finding 3: STATUS values were preserved, not standardized
**What changed:** `RAW_ORDERS.STATUS` has 5 unique values; the renamed `STG_ORDERS.ORDER_STATUS` column carries the same values through (only the column name changed, not the category values themselves).
**Likely reason:** The 5 status values (`completed`, `shipped`, `placed`, `returned`, `return_pending`) were already clean and consistently spelled at the source — there was no `'Completed'` vs `'completed'` inconsistency to collapse.
**Impact if not done:** If the raw values *had* been inconsistent (mixed casing, typos), skipping standardization here would silently split what should be one category into several in every downstream groupby — a common real-world staging responsibility this table simply didn't need.

## Finding 4: Orders-per-customer distribution is right-skewed
**What changed:** From chart 2 — of the 62 customers with at least one order, most (33) placed exactly 1 order, a smaller group (21) placed 2, and only a handful placed 3+ (one customer placed 6).
**Likely reason:** This is a `clean_and_merge()`-derived finding, not a raw-vs-staging difference — it reflects genuine underlying customer behavior (a typical "long tail" purchase pattern), not something dbt transformed.
**Impact if not done:** Worth flagging to a teammate building customer lifetime value or churn logic — averaging "orders per customer" as a single number would hide that the vast majority of active customers are single- or double-purchasers.

## Finding 5: ORDER_DATE stayed as text (object), not converted to a true date type
**What changed:** Both `RAW_ORDERS.ORDER_DATE` and `STG_ORDERS.ORDER_DATE` are dtype `object` (string), not `datetime64`.
**Likely reason:** This particular staging model focused on renaming/structure, not type casting — date parsing may happen in a later intermediate/mart model instead, or simply wasn't prioritized for this small demo project.
**Impact if not done:** Any downstream date arithmetic (days since order, monthly cohorts) run directly on `STG_ORDERS` would require an explicit `pd.to_datetime()` conversion first — a teammate assuming staging models always deliver typed dates would hit a silent bug (string comparison instead of date comparison) if they forgot this step.