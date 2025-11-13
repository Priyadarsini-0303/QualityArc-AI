import psycopg2
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API setup
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Load the embedding model (high quality)
model = SentenceTransformer("all-mpnet-base-v2")


# Step 1: Fetch all summaries from the DB
def fetch_all_summaries():
    conn = psycopg2.connect(
        dbname="TBS_DB",
        user="TBSDev",
        password="D8tATbsP35dDa90",
        host="172.19.6.84",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, text_data FROM public_api_testing_test2 WHERE text_data IS NOT NULL")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Step 2: Find the best-matching summary using cosine similarity
def find_best_summary(user_query, summaries):
    query_vector = model.encode(user_query).reshape(1, -1)

    best_score = -1
    best_summary = None
    best_id = None

    for id, summary_text in summaries:
        if not summary_text:
            continue
        try:
            summary_vector = model.encode(summary_text).reshape(1, -1)
            score = cosine_similarity(query_vector, summary_vector)[0][0]

            print(f"ID: {id}, Score: {score:.4f}, Preview: {summary_text[:60]}")

            if score > best_score:
                best_score = score
                best_summary = summary_text
                best_id = id
        except Exception as e:
            print(f" Error processing ID {id}: {e}")

    return best_summary


# Step 3: Generate test scenarios using OpenAI
def generate_test_scenarios(summary_text):
    prompt = f"""
You are a test scenario generation assistant.

Given the following API summary, generate test scenarios strictly based on the summary. Do not make assumptions or add generic test cases.

Each test scenario must be presented in the following format and structure (NOT as a table):

---
Test Scenario No: TS001
Test Scenario: <Short title>
TestCase#: TC001
TestCase: <Step or condition being tested>
Expected Result: <What should happen>
Reference: <Field name or business rule from the summary>

---

Use this structure for every scenario, numbering them sequentially as TS001, TS002, etc. Cover all relevant positive, negative, edge, and boundary cases based strictly on the summary below.

### API Summary:
{summary_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f" OpenAI error: {e}"


# Step 4: Main function
def main():
    user_query = input("Enter your test scenario query (e.g., 'create 1099-LTC'): ")
    summaries = fetch_all_summaries()

    best_summary = find_best_summary(user_query, summaries)

    if not best_summary:
        print(" No matching summary found.")
        return

    print("\n Matched Summary:\n", best_summary)
    print("\n Generated Test Scenarios:\n")
    print(generate_test_scenarios(best_summary))


if __name__ == "__main__":
    main()
