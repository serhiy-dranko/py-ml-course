import sys
import time
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 5000")
    df = cursor.fetch_pandas_all()

    # 1: Vectorized operations
    
    start_vectorized = time.perf_counter()
    
    df["C_ACCTBAL_Doubled"] = df["C_ACCTBAL"] * 2
    
    end_vectorized = time.perf_counter()
    vectorized_time = end_vectorized - start_vectorized

    print("First 5 rows with doubled account balance:")
    print(df[["C_CUSTKEY", "C_ACCTBAL", "C_ACCTBAL_Doubled"]].head())
    
    # 2:Loop-based operations
    start_loop = time.perf_counter()
    doubled_values = []
    for index, row in df.iterrows():
        doubled_values.append(row["C_ACCTBAL"] * 2)
    df["balance_doubled_loop"] = doubled_values
    end_loop = time.perf_counter()
    loop_time = end_loop - start_loop

    print("\nFirst 5 rows with loop-based doubled account balance:")
    print(df[["C_CUSTKEY", "C_ACCTBAL", "balance_doubled_loop"]].head())

    # 3: Compare execution times
    print(f"\Vectorized time: {vectorized_time:.6f} seconds")
    print(f"Loop time: {loop_time:.6f} seconds")

finally:
    conn.close()