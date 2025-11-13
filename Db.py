import logging
import traceback
import psycopg2
from psycopg2 import pool
import json

# Logging setup
logging.basicConfig(
    filename='db_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# DB Connection Pool
try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user="TBSDev",
        password="D8tATbsP35dDa90",
        host="35.172.229.109",
        port="5432",
        database="TBS_DB"
    )
    if postgreSQL_pool:
        logging.info("PostgreSQL connection pool created successfully.")
except Exception as e:
    logging.error(f"Error initializing DB connection: {e}\n{traceback.format_exc()}")
    raise

def fetch_all_rows_from_test2():
    try:
        conn = postgreSQL_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, table_data, code_data, rule_data
            FROM public_api_testing_test2
        """)
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "table_data": row[1],
                "code_data": row[2],
                "rule_data": row[3]
            })

        logging.info(f"Fetched {len(result)} records from test2.")
        return result

    except Exception as e:
        logging.error(f"Error fetching data: {e}\n{traceback.format_exc()}")
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            postgreSQL_pool.putconn(conn)

def update_text_data_in_db(record_id, text_data):
    try:
        conn = postgreSQL_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE public_api_testing_test2
            SET text_data = %s
            WHERE id = %s
        """, (text_data, record_id))
        conn.commit()
        logging.info(f"Updated text_data for ID: {record_id}")

    except Exception as e:
        logging.error(f"Error updating text_data for ID {record_id}: {e}\n{traceback.format_exc()}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            postgreSQL_pool.putconn(conn)
