import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("ALTER WAREHOUSE COMPUTE_WH RESUME;")
    print("Warehouse resumed successfully.")
finally:
    conn.close()