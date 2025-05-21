import pandas as pd
import mysql.connector
import random

# Step 1: Load hospital data
hospital_df = pd.read_csv("hospital data analysis.csv")

# Step 2: Load external name list
names_df = pd.read_csv("americans_by_descent.csv")
name_list = names_df['name'].dropna().tolist()

# Step 3: Add a new column 'Name' with random names
assigned_names = []

for _ in range(len(hospital_df)):
    random_name = random.choice(name_list)
    assigned_names.append(random_name)

hospital_df['Name'] = assigned_names

# Step 4: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",                      # your MySQL username
    password="Mamba@2408",        # your MySQL password
    database="medical_dataset"               # your database name
)
cursor = conn.cursor()

# Step 5: Create table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS hospital_data (
    Patient_ID VARCHAR(50),
    Age INT,
    Gender VARCHAR(10),
    `Condition` VARCHAR(100),
    `Procedure` VARCHAR(100),
    Cost FLOAT,
    Length_of_Stay INT,
    Readmission VARCHAR(10),
    Outcome VARCHAR(50),
    Satisfaction VARCHAR(50),
    Name VARCHAR(50)
);
""")

# Step 6: Insert each row into the table
for _, row in hospital_df.iterrows():
    cursor.execute("""
        INSERT INTO hospital_data 
        (Patient_ID, Age, Gender, `Condition`, `Procedure`, Cost, Length_of_Stay, Readmission, Outcome, Satisfaction, Name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Step 7: Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("✅ All rows inserted successfully into MySQL!")