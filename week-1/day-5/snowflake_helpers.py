import snowflake.connector
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization

load_dotenv()

def get_connection():
    key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")

    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        private_key=private_key_bytes,
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

def run_query(query):
    conn = get_connection()
    try:
        cursor = conn.cursor(snowflake.connector.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def run_query_to_summary(query, numeric_column):
    results = run_query(query)
    values = [row[numeric_column] for row in results]

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "average": sum(values) / len(values),
    }