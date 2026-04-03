import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def setup_database():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    
    # Tables creation
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT,first_name TEXT,last_name TEXT,email TEXT, phone TEXT, date_of_birth DATE, gender TEXT,city TEXT, registered_date DATE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,specialization TEXT,department TEXT,phone TEXT)''')    
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER,appointment_date DATETIME, status TEXT, notes TEXT, FOREIGN KEY(patient_id) REFERENCES patients(id),FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS treatments(id INTEGER PRIMARY KEY AUTOINCREMENT, appointment_id INTEGER, treatment_name TEXT,cost REAL, duration_minutes INTEGER, FOREIGN KEY(appointment_id) REFERENCES appointments(id))''')    
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices(id INTEGER PRIMARY KEY AUTOINCREMENT,patient_id INTEGER,invoice_date DATE, total_amount REAL, paid_amount REAL,status TEXT,FOREIGN KEY(patient_id) REFERENCES patients(id))''')
    
    # Dummy Data
    cities = ['Pune','Mumbai','Nagpur','Nashik','Thane','Solapur','Amravati','Aurangabad']
    spec_list = [('Dermatology','Skin Care'),('Cardiology','Heart'),('Orthopedics','Bones'),('General','OPD'),('Pediatrics','Kids')]
    
    # Doctors
    for i in range(15):
        selected_spec = random.choice(spec_list)
        cursor.execute("INSERT INTO doctors (name,specialization,department,phone) VALUES(?,?,?,?)",
                       (f"Dr. Doctor_{i}",selected_spec[0],selected_spec[1],f"98765432{i}"))
        
    # Patients
    for i in range(200):
        reg_date = datetime.now() - timedelta(days=random.randint(0,365))
        cursor.execute("INSERT INTO patients (first_name,last_name,city,registered_date,gender) VALUES(?,?,?,?,?)",(f"Patient_{i}","Surname",random.choice(cities),reg_date.date(),random.choice(['M','F'])))
        
    # Appointments and Invoices
    for i in range(500):
        p_id = random.randint(1,200)
        d_id = random.randint(1,15)
        a_date = datetime.now() - timedelta(days=random.randint(0,365))
        status = random.choice(['Completed','Scheduled','Cancelled','No-Show'])
        cursor.execute("INSERT INTO appointments (patient_id,doctor_id,appointment_date,status) VALUES (?,?,?,?)",(p_id,d_id,a_date,status))
        
        if status == 'Completed':
            cost = random.uniform(500,5000)
            cursor.execute("INSERT INTO invoices (patient_id,invoice_date,total_amount,paid_amount,status) VALUES (?,?,?,?,?)",(p_id,a_date.date(),cost,cost if random.random() > 0.2 else 0, random.choice(['Paid','Pending','Overdue'])))
            
    conn.commit()
    print(f"Created 200 patients, 15 doctors, 500 appointments in clinic.db")
    conn.close()
    
if __name__ =='__main__':
    setup_database()
        