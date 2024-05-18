import os
import pandas as pd
import psycopg2
from psycopg2 import sql

folder_path = './data'

csv_path = os.path.join(folder_path, 'meta.csv')
df = pd.read_csv(csv_path)

conn_params = {
    'dbname': 'aas_db',
    'user': 'postgres',
    'password': '123456789',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

def read_image_as_bytea(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

# Insert data into the table
for index, row in df.iterrows():
    student_id = row['student_id']
    full_name = row['full_name']
    class_id = row['class_id']
    st_group = row['st_group'] == "True"
    photo_filename = row['photo']
    
    photo_path = os.path.join(folder_path, photo_filename)
    photo_bytea = read_image_as_bytea(photo_path)
    
    insert_query = sql.SQL("""
        INSERT INTO Student (student_id, full_name, class_id, st_group, photo)
        VALUES (%s, %s, %s, %s, %s)
    """)
    cur.execute(insert_query, (student_id, full_name, class_id, st_group, photo_bytea))
    print(f"Inserted {full_name}.")

conn.commit()

cur.close()
conn.close()

print("Data inserted successfully.")
