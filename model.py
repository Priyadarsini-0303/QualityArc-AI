import openai
import logging
import os
import time
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

# API Key Setup from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Logging setup
logging.basicConfig(
    filename='openai_debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def openai_request_with_retry(prompt, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            logging.debug(f"Sending prompt to OpenAI. Attempt {retries + 1}")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            logging.info("Prompt processed successfully.")
            return response.choices[0].message.content.strip()
        except openai.OpenAIError as e:
            logging.error(f"OpenAI error: {e}")
            if "rate_limit_exceeded" in str(e).lower():
                wait = (2 ** retries) * 5
                logging.warning(f"Rate limit hit. Retrying in {wait} seconds...")
                time.sleep(wait)
                retries += 1
            else:
                break
    return "Summary generation failed due to API error or empty response."

def generate_summary_from_openai(preprocessed_text, table_data, code_data, rule_data):
    prompt = f"""
You are an expert test scenario generation assistant with a strong understanding of API design, backend logic, database structures, and business rules.

Your task is to analyze and synthesize the following inputs to generate a **comprehensive, detailed, and fully-paragraph-based summary** that reflects the complete behavior of the API endpoint.

### Inputs:
- **Code Data (API Logic):** {code_data}
- **Table Data (Database Schema):** {table_data}
- **Rule Data (Business Requirements):** {rule_data}
- **Preprocessed Combined Info:** {preprocessed_text}

### Instructions:
Write a clear, coherent, and structured paragraph (or multiple short paragraphs) that summarizes the **complete logic and behavior of the API endpoint** based on the combined inputs.

The summary should describe:
- The overall purpose of the API and the resource it handles.
- The structure of requests and responses, including HTTP methods, endpoints, field usage, and expected data types.
- All key validations: required vs optional fields, format constraints, value restrictions, and conditional dependencies.
- Business rule enforcement, including how specific fields or conditions are governed by rule logic.
- How the API interacts with the database: what tables are queried, updated, or inserted into; what constraints apply; and any lookups or joins.
- Error handling behavior: how the system responds to invalid inputs, missing fields, or database failures.
- Any defaults or derived values handled internally (e.g., timestamps, IDs, flags).
- Important test-relevant behaviors such as input edge cases, boundary conditions, and integrity checks that must be validated.

Do **not** use bullet points, numbered lists, or section headers. Write it entirely as a **natural flowing paragraph (or two)** that includes all critical information required for test planning. The goal is to produce a full summary of the endpoint’s behavior, not just a narrow or single scenario.
"""


    return openai_request_with_retry(prompt)
