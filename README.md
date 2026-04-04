# 🏥 Clinic Analytics AI Agent

This project is a **Natural Language to SQL (NL-to-SQL)** AI Assistant built using the **Vanna.ai** framework and **Google Gemini 1.5 Flash**. It allows users to ask questions about clinic data (patients, doctors, appointments) in plain English and retrieves the results directly from a SQLite database.

## 🚀 Features
- **Natural Language Querying:** Converts English questions into accurate SQL queries.
- **SQL Validation:** Custom security layer to prevent non-SELECT queries (DROP, DELETE, etc.).
- **Automated Summaries:** Every data output includes a summary row indicating the total records found.
- **Interactive UI:** Built-in web interface powered by Vanna's FastAPI server.
- **AI Agent Memory:** Remembers successful SQL patterns to improve accuracy over time.

---

## 🛠️ Tech Stack
- **LLM:** Google Gemini 2.5 Flash (via `google-generativeai`)
- **Framework:** [Vanna.ai](https://vanna.ai/) (v2.0)
- **Database:** SQLite (`clinic.db`)
- **Backend:** FastAPI / Uvicorn
- **Environment:** Python 3.10+

---

## 📋 Setup Instructions

### 1. Clone the Repository
git clone [<your-github-repo-link>](https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI)  
cd AI_ML_Intern_assignment

### 2. Install dependencies
pip install -r requirements.txt
`(Note: Ensure vanna[fastapi,gemini] is installed.)`

### 3. Configure Environment Variables
Create a .env file in the root directory and add your API key:  
GOOGLE_API_KEY=your_gemini_api_key_here

### 4. Run the Application  
python main.py

## 🧠 Project Architecture & Approach
- This project follows the Vanna 2.0 Registry Pattern:
- Tool Registry: Registers RunSqlTool and VisualizeDataTool with specific access groups.
- User Resolver: Implements a SimpleUserResolver to handle mock authentication.
- Custom Runner: Instead of using the default execution, a custom_run_sql wrapper was implemented in main.py to add a security validation layer and format the final output with a summary row.

## ⚠️ Challenges & Troubleshooting
1. API Rate Limits (429 Errors): Encountered "Resource Exhausted" errors due to Gemini's Free Tier limits. Solved by implementing a clean shutdown of ghost processes and switching to the stable gemini-1.5-flash model.
2. Model Path Configuration: Some "latest" model aliases were not recognized by the google-genai SDK. Resolved this by using the explicit models/gemini-2.5-flash path.
3. UI Data Rendering: Initial issues with the table not appearing in the UI were fixed by ensuring the custom wrapper always returns a consistent Pandas DataFrame instead of raw strings.
