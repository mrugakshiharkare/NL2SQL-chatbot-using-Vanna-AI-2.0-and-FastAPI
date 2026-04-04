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
- **LLM:** Google Gemini 1.5 Flash (via `google-generativeai`)
- **Framework:** [Vanna.ai](https://vanna.ai/) (v2.0)
- **Database:** SQLite (`clinic.db`)
- **Backend:** FastAPI / Uvicorn
- **Environment:** Python 3.10+

---

## 📋 Setup Instructions

### 1. Clone the Repository
git clone <your-github-repo-link>
cd <repo-folder-name>
