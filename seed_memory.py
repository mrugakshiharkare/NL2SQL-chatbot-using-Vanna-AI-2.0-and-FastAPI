import asyncio
import uuid
from vanna_setup import get_agent
from vanna.tools.agent_memory import ToolContext
from vanna.core.user.models import User

async def seed():
    agent = get_agent()
    
    training_data = [
            {"question": "How many patients do we have?","sql":"SELECT COUNT(*) AS total_patients FROM patients"},
            {"question": "Show revenue by doctor","sql":"SELECT d.name, SUM(i.total_amount) AS total_revenue FROM invoices i JOIN appointments a ON a.patient_id = i.patient_id JOIN doctors d ON d.id = a.doctor_id GROUP BY d.name ORDER BY total_revenue DESC"},
            {"question": "Which city has the most patients?","sql":"SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1"},
            {"question":"What is the total revenue?","sql":"SELECT SUM(total_amount) AS total_revenue FROM invoices"},
            {"question":"How many appointments are there?","sql":"SELECT COUNT(*) AS total_appointments FROM appointments"},
            {"question":"What is the average appointment duration?","sql":"SELECT AVG(duration) AS average_duration FROM appointments"},
            {"question":"Which doctor has the most appointments?","sql":"SELECT d.name, COUNT(a.id) AS appointment_count FROM appointments a JOIN doctors d ON d.id = a.doctor_id GROUP BY d.name ORDER BY appointment_count DESC LIMIT 1"},
            {"question":"What is the total number of invoices?","sql":"SELECT COUNT(*) AS total_invoices FROM invoices"},
            {"question":"Show the top 5 patients by revenue","sql":"SELECT p.name, SUM(i.total_amount) AS total_revenue FROM invoices i JOIN patients p ON p.id = i.patient_id GROUP BY p.name ORDER BY total_revenue DESC LIMIT 5"},
            {"question":"How many doctors are there?","sql":"SELECT COUNT(*) AS total_doctors FROM doctors"},
            {"question":"What is the total number of patient visits?","sql":"SELECT COUNT(*) AS total_visits FROM appointments"},
            {"question":"Show the least profitable doctor","sql":"SELECT d.name, SUM(i.total_amount) AS total_revenue FROM invoices i JOIN appointments a ON a.patient_id = i.patient_id JOIN doctors d ON d.id = a.doctor_id GROUP BY d.name ORDER BY total_revenue ASC LIMIT 1"},
            {"question":"Which patient has the highest total invoice amount?","sql":"SELECT p.name, SUM(i.total_amount) AS total_invoice_amount FROM invoices i JOIN patients p ON p.id = i.patient_id GROUP BY p.name ORDER BY total_invoice_amount DESC LIMIT 1"},
            {"question":"What is the average revenue per patient?","sql":"SELECT AVG(total_amount) AS average_revenue_per_patient FROM (SELECT SUM(total_amount) AS total_amount FROM invoices GROUP BY patient_id)"},
            {"question":"How many appointments were completed?","sql":"SELECT COUNT(*) AS completed_appointments FROM appointments WHERE status = 'Completed'"},
            {"question": "Show me patients from Pune", "sql": "SELECT * FROM patients WHERE city = 'Pune'"},
            {"question": "What is the total revenue from paid invoices?", "sql": "SELECT SUM(total_amount) FROM invoices WHERE status = 'Paid'"},
            {"question": "Who is the busiest doctor?", "sql": "SELECT d.name, COUNT(a.id) as appt_count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.name ORDER BY appt_count DESC LIMIT 1"},
            {"question": "Show appointments scheduled for today", "sql": "SELECT * FROM appointments WHERE status = 'Scheduled' AND date(appointment_date) = date('now')"},
            {"question": "How many male and female patients do we have?", "sql": "SELECT gender, COUNT(*) FROM patients GROUP BY gender"},
            {"question": "List treatments that cost more than 2000", "sql": "SELECT * FROM treatments WHERE cost > 2000"},
            {"question": "Average cost of treatments", "sql": "SELECT AVG(cost) FROM treatments"},
            {"question": "Show top 3 cities with most patients", "sql": "SELECT city, COUNT(*) as count FROM patients GROUP BY city ORDER BY count DESC LIMIT 3"},
            {"question": "List unpaid invoices for Patient_1", "sql": "SELECT * FROM invoices WHERE status != 'Paid' AND patient_id = 1"},
            {"question": "How many appointments were cancelled?", "sql": "SELECT COUNT(*) FROM appointments WHERE status = 'Cancelled'"},
            {"question": "Show doctors in Cardiology department", "sql": "SELECT name FROM doctors WHERE department LIKE '%Cardiology%'"},
            {"question": "What is the total amount pending in invoices?", "sql": "SELECT SUM(total_amount - paid_amount) FROM invoices WHERE status = 'Pending'"},
            {"question": "Show latest 5 registered patients", "sql": "SELECT * FROM patients ORDER BY registered_date DESC LIMIT 5"}
        ]
    print("Seeding Vanna Memory...\n")
    
    # Correct User
    user = User(id="admin",email="admin@example.com",group_memberships=["admin"])
    
    # Loop
    for item in training_data:
        context = ToolContext(
            user = user,
            conversation_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            agent_memory=agent.agent_memory
        )
        
        await agent.agent_memory.save_tool_usage(
            question=item['question'],
            tool_name="RunSqlTool",
            args={"sql": item['sql']},
            context = context,
            success=True
        )
        print(f"Saved: {item['question']}")
    
    print(f"Memory seeding completed with {len(training_data)} entries.")
    
if __name__ == '__main__':
    asyncio.run(seed())