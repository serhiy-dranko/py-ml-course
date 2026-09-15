import sys
sys.path.append("../../week-1/day-5")

from snowflake_helpers import get_connection

conn = get_connection()

try:
    cursor = conn.cursor()
    cursor.execute("ALTER WAREHOUSE COMPUTE_WH SUSPEND;")
    print("Warehouse suspended successfully.")
finally:
    conn.close()