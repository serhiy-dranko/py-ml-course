from snowflake_helpers import run_query

# 2 Run a query to fetch customer names, nation keys, and account balances
results = run_query("SELECT C_NAME, C_NATIONKEY, C_ACCTBAL FROM CUSTOMER LIMIT 15")

for row in results:
    print(f"{row['C_NAME']} — nation {row['C_NATIONKEY']}, balance {row['C_ACCTBAL']}")

# 3 Run a query to fetch just the names of the customers

names = [row["C_NAME"] for row in results]
print("\nJust the names:", names)

# 4 Run a query to print how many rows were returned

print(f"\nTotal rows returned: {len(results)}")

from snowflake_helpers import run_query, run_query_to_summary
summary = run_query_to_summary(
    "SELECT C_ACCTBAL FROM CUSTOMER LIMIT 500",
    "C_ACCTBAL"
)
print("\nCustomer balance summary (first 500 customers):")
print(f"Count: {summary['count']}")
print(f"Min: {summary['min']}")
print(f"Max: {summary['max']}")
print(f"Average: {summary['average']:.2f}")