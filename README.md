# 🏥 Clinic Analytics AI Agent

This project is a **Natural Language to SQL (NL-to-SQL)** AI Assistant built using the **Vanna.ai** framework and **Google Gemini 2.5 Flash**. It allows users to ask questions about clinic data (patients, doctors, appointments) in plain English and retrieves the results directly from a SQLite database.

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
`Open your browser and go to http://localhost:8084 to start asking questions!`

### 💡 Try These Questions:
1. "List all doctors and their specializations"
2. "Show me appointments for last month"
3. "Which doctor has the most appointments?"

## 🧠 Project Architecture & Approach
- This project follows the Vanna 2.0 Registry Pattern:
- Tool Registry: Registers RunSqlTool and VisualizeDataTool with specific access groups.
- User Resolver: Implements a SimpleUserResolver to handle mock authentication.
- Custom Runner: Instead of using the default execution, a custom_run_sql wrapper was implemented in main.py to add a security validation layer and format the final output with a summary row.

## 🧪 Problems I Faced and How I Fixed Them

During this project, I ran into several challenges.Here is the story of how I built this:

### 1. Error with the AI Model Name
At first, I was just typing `gemini-2.0-flash` in my code. I read the documentation and realized it should be written as `models/gemini-2.0-flash`. Even after changing that, it still wasn't working! 
* **The Fix:** I created a special file called **`check_models.py`**. This script talked to Google and printed out a list of every single model name my API key was allowed to use. This helped me find the exact correct name that the system would accept (like `models/gemini-2.0-flash`).

### 2. API "Out of Breath" (429 Error)
Since I am using the free version of Gemini, the system would often stop working and say "Resource Exhausted." This was the most frustrating part of the project because I tried everything to fix it:
* **What I tried:** First, I waited for one minute (or the time shown in the error), but it still wouldn't work. Then, I tried switching to different models to see if they had more space, but the same issue happened. I even generated a brand-new API key, but the error didn't go away!
* **The Fix:** I eventually realized that "ghost" Python processes were still running in the background and holding onto the old, exhausted connection. I learned to "kill" these hidden tasks using the terminal. I also simplified the code to stop the AI from doing extra work, which finally saved my "daily limit" and made the connection stable.

### 3. Database Issues and `check_db.py`
Sometimes the AI would write a perfect SQL query, but the table would come back empty or show an error. I wasn't sure if the problem was the AI's logic or my actual database file (`clinic.db`).
* **The Fix:** I created **`check_db.py`**. I used this to manually look inside my database to make sure the tables (like Patients and Doctors) actually existed and had data in them. This proved my database was fine, so I knew the problem was in how the AI was connecting to it.

### 4. Table Not Showing in the Browser
In the beginning, I could see the SQL query on the screen, but the actual data table was missing. It turned out I had a small mistake in my `main.py` where I was trying to use a function before I had even created it (a `NameError`).
* **The Fix:** I rearranged my code so the functions are defined at the top. I also made sure the data is sent back as a **Pandas DataFrame**, because that is the only format the Vanna website understands to draw a proper table.

### 5. Adding the Summary Row
The assignment asked for a summary of the data. Since the Vanna website usually just shows a standard table, I had to figure out a way to "inject" a summary manually.
* **The Fix:** I wrote a custom function that takes the result table, adds one extra row at the bottom, and writes **"Summary: [Total Rows]"** in that row. This ensures the user sees the data and the total count clearly in one view.

### 6. API Quota & Global Synchronization Challenges
* **The Problem:** During the final verification phase, the system encountered persistent `429 RESOURCE_EXHAUSTED` errors. Despite the Google Cloud Console indicating that the daily quota had reset (0 requests used), the API Gateway remained locked due to a "Sync Lag" between global server regions.
* **The Strategy (Troubleshooting & Resolution):**
    1.  **Account & Identity Rotation:** To bypass the cached quota state, I transitioned the project to a fresh Google Service Account and generated a new API Key.
    2.  **Initial Retry & Burst Handling:** When the first request on the new key hit a temporary burst limit, I did not stop. I implemented a secondary retry after a 60-second cooldown.
    3.  **Model Optimization:** I pivoted the implementation from Gemini 2.0 to **Gemini 2.5 Flash**. This specific model provided the necessary stability and higher throughput required to process the SQL generation and data summarization simultaneously.
* **The Result:** This multi-step workaround successfully restored the chatbot's functionality, allowing for the final capture of system performance metrics and successful query results.

  ## 📊 Testing & Results
I tested the AI with 5 different questions to see how well it writes SQL for our database. I found that while the AI is great at simple tasks, it needs a bit of help with the hard ones.

**What I Discovered:**
* **Simple Questions:** The AI handles these perfectly on its own.
* **Hard Questions:** The AI often **guesses the wrong names** for our tables. I fixed this by **giving the AI the exact table and column names before asking a question.
* **Math Limits:** Even with a map, the AI still struggles with tricky math like percentages.

👉 **[Click here to see the full Testing Report (RESULTS.md)](https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/Results.md)**

## 📸 Project Visuals

### 1. System Configuration & Setup
This shows the successful connection to the database and the Gemini API.  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_opening_interface.png

### 2. Handling API Challenges
I documented the "Resource Exhausted" errors I faced during development to show my debugging process.  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_error_msg.png

### 3. Final Successful Results  
The AI correctly translates natural language into SQL and provides a data summary.  
Input Question to the AI:  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_question_uploded.png  
Query Result 1:  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_query_returned.png  
Data Summary Row:  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_output_response.png  
https://github.com/mrugakshiharkare/NL2SQL-chatbot-using-Vanna-AI-2.0-and-FastAPI/blob/main/vanna_2.0_responses/vanna_2.0_output_query.png  

