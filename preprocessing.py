# import logging
# import traceback
# from sentence_transformers import SentenceTransformer

# # Logging setup
# logging.basicConfig(
#     filename='preprocessing_debug.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# # Load model globally
# try:
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     logging.info("SentenceTransformer model loaded successfully.")
# except Exception as e:
#     logging.error(f"Error loading embedding model: {e}\n{traceback.format_exc()}")
#     model = None

# # Constants
# MAX_LENGTH = 5000

# def truncate(text, max_len=MAX_LENGTH):
#     """Truncate long strings to avoid token overflow."""
#     return text[:max_len] if len(text) > max_len else text

# def preprocess_data(data):
#     """
#     Preprocesses raw DB rows and generates embeddings.
    
#     Input:
#         data (list of dict): Each dict must have 'id', 'table_data', 'code_data', 'rule_data'
#     Output:
#         list of (id, merged_text, embedding) tuples
#     """
#     processed_embeddings = []

#     try:
#         for record in data:
#             record_id = record.get("id")
#             table_data = truncate(record.get("table_data", "").strip())
#             code_data = truncate(record.get("code_data", "").strip())
#             rule_data = truncate(record.get("rule_data", "").strip())

#             # Merge all inputs into a single document for embedding
#             merged_text = (
#                 f"Table Description:\n{table_data}\n\n"
#                 f"Code Snippet:\n{code_data}\n\n"
#                 f"Rule Definition:\n{rule_data}"
#             )

#             if model:
#                 embedding = model.encode(merged_text)
#                 processed_embeddings.append((record_id, merged_text, embedding))
#                 logging.debug(f"Processed record ID: {record_id}")
#             else:
#                 logging.warning(f" Skipping embedding for ID {record_id}: Model not loaded.")

#         logging.info(f"Generated embeddings for {len(processed_embeddings)} records.")
#         return processed_embeddings

#     except Exception as e:
#         logging.error(f"Error during preprocessing and embedding: {e}\n{traceback.format_exc()}")
#         return []


import logging
import traceback
from sentence_transformers import SentenceTransformer

# Logging setup
logging.basicConfig(
    filename='preprocessing_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load model globally
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logging.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading embedding model: {e}\n{traceback.format_exc()}")
    model = None

# Constants
MAX_LENGTH = 5000
FULL_RECORD_IDS = {1752,1773,1775}  # Add IDs that should NOT be truncated

def truncate(text, max_len=MAX_LENGTH, truncate_flag=True):
    """Truncate long strings to avoid token overflow."""
    return text[:max_len] if truncate_flag and len(text) > max_len else text

def preprocess_data(data):
    """
    Preprocesses raw DB rows and generates embeddings.

    Input:
        data (list of dict): Each dict must have 'id', 'table_data', 'code_data', 'rule_data'
    Output:
        list of (id, merged_text, embedding) tuples
    """
    processed_embeddings = []

    try:
        for record in data:
            record_id = record.get("id")
            truncate_flag = record_id not in FULL_RECORD_IDS

            table_data = truncate(record.get("table_data", "").strip(), truncate_flag=truncate_flag)
            code_data = truncate(record.get("code_data", "").strip(), truncate_flag=truncate_flag)
            rule_data = truncate(record.get("rule_data", "").strip(), truncate_flag=truncate_flag)

            merged_text = (
                f"Table Description:\n{table_data}\n\n"
                f"Code Snippet:\n{code_data}\n\n"
                f"Rule Definition:\n{rule_data}"
            )

            if model:
                embedding = model.encode(merged_text)
                processed_embeddings.append((record_id, merged_text, embedding))
                logging.debug(f"Processed record ID: {record_id} (truncate: {truncate_flag})")
            else:
                logging.warning(f"Skipping embedding for ID {record_id}: Model not loaded.")

        logging.info(f"Generated embeddings for {len(processed_embeddings)} records.")
        return processed_embeddings

    except Exception as e:
        logging.error(f"Error during preprocessing and embedding: {e}\n{traceback.format_exc()}")
        return []
