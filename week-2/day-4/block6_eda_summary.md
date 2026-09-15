# EDA Summary — RAW_PAYMENTS

## 1. What this table is

The `RAW_PAYMENTS` table contains payment records associated with orders.

Each row represents a payment record with an `ID`, an `ORDER_ID`, a `PAYMENT_METHOD`, and an `AMOUNT`.

The initial assumption was that the table contains individual payment transactions. The EDA generally confirmed this understanding.

The numeric columns include `ID`, `ORDER_ID`, and `AMOUNT`, while `PAYMENT_METHOD` is a categorical column.

---

## 2. Data quality issues found

### Identifier relationship

`ID` and `ORDER_ID` have an extremely strong correlation of approximately `0.9998`.

Because both columns are identifiers, this is most likely a structural characteristic of the source data rather than a meaningful business relationship.

**Recommendation:** This does not necessarily require a data-quality fix in dbt. However, the relationship should be documented so downstream users do not interpret it as a meaningful analytical relationship.

### AMOUNT contains zero values

`AMOUNT` has a minimum value of `0`.

A zero payment amount may be valid for some payment methods, but it should be confirmed against the business definition of a payment record.

**Recommendation:** If zero amounts are valid, document them in the staging model. If payments are expected to always contain a positive amount, this should be investigated as an upstream data-quality issue.

### Small category sizes

The `PAYMENT_METHOD` groups are uneven in size:

- `credit_card`: 55 records
- `bank_transfer`: 33 records
- `coupon`: 13 records
- `gift_card`: 12 records

The smaller groups should be considered when comparing distributions because their statistics are less stable.

**Recommendation:** No automatic filtering should be applied in staging. Preserve the source values and flag the small group sizes when performing downstream analysis.

---

## 3. Notable relationships

### AMOUNT and PAYMENT_METHOD

The distribution of `AMOUNT` differs between payment methods.

`gift_card` has the highest mean amount at approximately `1708`, while `bank_transfer` has the lowest mean at approximately `1245`.

The medians are also somewhat different:

- `bank_transfer`: `1400`
- `coupon`: `1700`
- `credit_card`: `1700`
- `gift_card`: `1750`

However, the distributions overlap considerably and some groups contain only 12–13 records. Therefore, the observed differences should not be treated as strong evidence of a systematic business effect without further analysis.

### Numeric relationships

`AMOUNT` has only a very weak linear relationship with the identifier columns:

- `AMOUNT` vs `ID`: approximately `0.075`
- `AMOUNT` vs `ORDER_ID`: approximately `0.073`

The extremely high correlation between `ID` and `ORDER_ID` should not be interpreted as a business relationship because both columns are identifiers.

### Visual confirmation

The histogram of `AMOUNT` was used to inspect its distribution and identify skew or unusual concentration of values.

The boxplot of `AMOUNT` by `PAYMENT_METHOD` was used to compare the distributions and identify potential outliers within individual payment-method groups.

The scatter plot of `ORDER_ID` versus `AMOUNT` was used to validate the very low correlation observed numerically.

The scatter plot did not provide evidence of a meaningful relationship between the order identifier and payment amount. This supports the conclusion from the correlation coefficient that there is no useful linear relationship between these columns.

---

## 4. Recommendation

The raw table should generally be preserved without aggressive transformations in the staging layer.

Recommended staging actions:

1. Keep `ID` and `ORDER_ID` as identifiers and document their relationship.
2. Preserve `PAYMENT_METHOD` values as source categories.
3. Validate whether `AMOUNT = 0` is a legitimate business case.
4. Do not remove small payment-method groups simply because they contain fewer records.
5. Avoid using `ID` or `ORDER_ID` as analytical variables because they are identifiers rather than meaningful measures.
6. If zero or otherwise invalid payment amounts violate the source-system business rules, raise these records as an upstream data-quality issue rather than silently filtering them in dbt.

Overall, the table appears usable for downstream analysis, but the meaning of zero payment amounts and the relationship between the identifier columns should be documented before building further models on top of it.