from Db import fetch_all_rows_from_test2, update_text_data_in_db
from model import generate_summary_from_openai
import json
import logging
from tqdm import tqdm

# Logging setup
logging.basicConfig(
    filename='main_process.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MAX_LENGTH = 5000
def truncate(text, max_len=MAX_LENGTH):
    return text[:max_len] if text else ""

def main():
    logging.info("🚀 Starting individual summary generation")

    data = fetch_all_rows_from_test2()
    if not data:
        logging.warning("⚠️ No data found.")
        return

    for record in tqdm(data):
        record_id = record['id']
        table_data = truncate(record.get('table_data', ''))
        code_data = truncate(record.get('code_data', ''))
        rule_data = truncate(record.get('rule_data', ''))

        merged_text = f"{table_data}\n\n{code_data}\n\n{rule_data}"

        try:
            summary = generate_summary_from_openai(merged_text, table_data, code_data, rule_data)
        except Exception as e:
            logging.exception(f"Exception for ID {record_id}")
            summary = None

        if summary:
            update_text_data_in_db(record_id, summary)
            logging.info(f"Summary updated for ID: {record_id}")
        else:
            logging.error(f" Failed to generate summary for ID: {record_id}")

if __name__ == "__main__":
    main()
