import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection
import numpy as np
import time

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER")
    df = cursor.fetch_pandas_all()

    # Point 1: pull a numeric column out as a raw NumPy array
    arr = df["C_ACCTBAL"].to_numpy()
    print("Array type:", type(arr))
    print("First 5 values:", arr[:5])

    # Point 2: broadcasted operation on the array vs on the Series
    arr_increased = arr * 1.1
    series_increased = df["C_ACCTBAL"] * 1.1

    print("\nArray result matches Series result?",
          np.allclose(arr_increased, series_increased.to_numpy()))

    # Point 3a: np.where() for conditional column creation
    start_where = time.perf_counter()
    df["balance_level_where"] = np.where(df["C_ACCTBAL"] > 1000, "high", "low")
    end_where = time.perf_counter()

    # Point 3b: same logic with .apply() + lambda, for comparison
    start_apply = time.perf_counter()
    df["balance_level_apply"] = df["C_ACCTBAL"].apply(lambda x: "high" if x > 1000 else "low")
    end_apply = time.perf_counter()

    print(f"\nnp.where() time: {end_where - start_where:.6f} seconds")
    print(f".apply() + lambda time: {end_apply - start_apply:.6f} seconds")
    print("Results match?", (df["balance_level_where"] == df["balance_level_apply"]).all())   

     # Point 4: NaN handling — arr.sum() vs np.nansum()
    test_arr = np.array([10.0, 20.0, np.nan, 30.0])
    print("\nTest array:", test_arr)
    print("arr.sum():", test_arr.sum())
    print("np.nansum():", np.nansum(test_arr))


finally:
    conn.close()

# np.where() (0.0086s) was nearly 2x faster than .apply() (0.0158s), confirming that vectorized NumPy operations scale better than row-by-row .apply() calls, consistent with Day 1's loop-vs-vectorization findings