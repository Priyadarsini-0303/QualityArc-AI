# QualityArc-AI
This project helps generate **test scenarios automatically** from **API summaries** stored in a database.  
It uses **text similarity** and **AI models** to find the most relevant API description and create easy-to-understand test cases.

---
##  What It Does
- Reads API details from a database  
- Uses **sentence embeddings** to find the closest matching summary  
- Generates **test scenarios** and **descriptions** using an AI model  
- Updates the database with the generated output  

---

##  Main Files
- **main.py** – Runs the full process (fetch → generate → update DB)  
- **test_run.py** – Creates and stores embeddings in the database  
- **test_scenario_generator.py** – Finds the best match and generates test scenarios  
- **model.py** – Connects to the OpenAI model and formats prompts  
- **Db.py / vector_Db.py** – Handles database connections  

---

##  Tech Stack
- **Python**
- **Pandas**, **Sentence Transformers**, **OpenAI API**
- **PostgreSQL** for database
- **LangChain** for AI model connection

##  Demo Video

https://github.com/user-attachments/assets/41ed7cb7-ed81-4298-9626-e684784bf3f2



