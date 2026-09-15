from snowflake_helpers import get_connection
import snowflake.connector

conn = None
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    result = cursor.fetchone()
    print("Connected! Snowflake version:", result)

    # cursor (tuples)
    cursor.execute("SELECT * FROM CUSTOMER LIMIT 10")
    rows = cursor.fetchall()
    print("\n--- As tuples ---")
    for row in rows:
        print(row)

    # DictCursor (dictionaries)
    dict_cursor = conn.cursor(snowflake.connector.DictCursor)
    dict_cursor.execute("SELECT * FROM CUSTOMER LIMIT 10")
    dict_rows = dict_cursor.fetchall()
    print("\n--- As dictionaries ---")
    for row in dict_rows:
        print(row["C_NAME"], row["C_NATIONKEY"])

except Exception as e:
    print(f"Something went wrong: {e}")

finally:
    if conn is not None:
        conn.close()
        print("Connection closed.")