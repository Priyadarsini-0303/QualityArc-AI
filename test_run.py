import psycopg2
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='embedding_debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_and_store_embeddings():
    try:
        logging.info("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(
            dbname="TBS_DB",
            user="TBSDev",
            password="D8tATbsP35dDa90",
            host="172.19.6.84",
            port="5432"
        )
        cursor = conn.cursor()
        logging.info("Connection successful.")

        cursor.execute("SELECT id, text_data FROM public_api_testing_test2 WHERE embedding IS NULL")
        rows = cursor.fetchall()
        logging.info(f"Fetched {len(rows)} rows without embeddings.")

        for record_id, summary in rows:
            if not summary:
                logging.warning(f"Skipping ID {record_id}: summary is empty or None.")
                continue

            logging.info(f"Generating embedding for ID {record_id}...")
            embedding = model.encode(summary).tolist()

            cursor.execute(
                "UPDATE public_api_testing_test2 SET embedding = %s WHERE id = %s",
                (json.dumps(embedding), record_id)
            )
            logging.info(f" Stored embedding for ID: {record_id}")

        conn.commit()
        logging.info("All embeddings committed to the database.")

    except Exception as e:
        logging.error(f" Error occurred: {e}")
        print(f" ERROR: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    start_time = datetime.now()
    logging.info("==== Starting Embedding Generation Process ====")
    generate_and_store_embeddings()
    logging.info(f"==== Process completed in {datetime.now() - start_time} ====")
