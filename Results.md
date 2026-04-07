## 📈 Summary of My Work
I tested how well the AI could write SQL for our hospital database. I picked **5 specific questions** to see where the AI was smart and where it got confused.

* **Total Questions Tested:** 5
* **Success on Easy Questions:** 2/2 (The AI guessed the structure correctly)
* **Success on Complex Questions:** 2/3 (It struggled with specific math/logic even with a database schema)

---

## 📝 Detailed Test Results

| Q# | Question | Difficulty | Status | What I Noticed |
|:---|:---|:---|:---:|:---|
| 1 | How many patients? | Easy | Pass | The AI correctly identified the `COUNT` function. |
| 2 | List doctors & specializations | Easy | Pass | Simple list; worked perfectly. |
| 6 | Revenue by doctor | **Hard** | Pass | **Initial Error:** The AI made up a table called `billing`. I fixed this by giving it the Table Schema. |
| 12 | Patients with >3 visits | **Medium** | Pass | **Initial Error:** The AI used the wrong column name (`PatientID`). I corrected it to use `id`. |
| 14 | Percentage of no-shows | **Hard** | **Fail** | **The Issue:** Even with the table names, the AI struggled with the math. it returned `0` instead of a decimal percentage. |

*\*Passed only after I gave the AI the Table Definitions of our database.*

---

## ⚠️ What I Learned
I found a very clear pattern during my testing:

1.  **Simple Questions:** If the question is basic, the AI is good at guessing what to do.
2.  **Complex Questions (Joins/Groups):** The AI fails at first because it doesn't know our specific table names. It starts making up names like `billing`. 
3.  **The Solution:** I realized that for high-quality results, I **must give the AI the table structure** before asking the query. This fixed most naming errors.

---

## 🔮 Why did Question fail?
Even with the table names,question failed. 
* **Integer Division:** In SQL, if you divide 10 by 100, the database often says `0` instead of `0.1`. 
* **The Fix:** For the next phase, I need to tell the AI to "Cast as Float" or multiply by 100.0 to get the correct decimal result.

---

## 🚀 Which of the remaining might still fail?
Based on my testing, these two are the most likely to have issues:

1.  **Day of the Week:** Every database (SQLite vs MySQL) has a different way of saying "Monday" or "Tuesday." The AI might pick the wrong "language" for our database.
2.  **Last Quarter:** "Last Quarter" is vague. The AI might struggle to calculate the exact dates (like Jan 1st to March 31st) without more help.
