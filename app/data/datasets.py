import os
import sqlite3
import pandas as pd
from app.data.db import *

data_csv_path = DATA_DIR / "datasets_metadata.csv"

# Loading the file into the database
def load_dataset_csv(conn):
    meta_data = pd.read_csv(data_csv_path)
    meta_data.to_sql("datasets_metadata", conn)

# Get all the data
def get_all_metadata():
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata")
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    conn.close()
    return rows, cols

# Create
def create_dataset(data):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (
            dataset_id, name, rows, columns, uploaded_by, upload_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

# Update
def update_dataset(row_id, data):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata
        SET dataset_id=?, name=?, rows=?, columns=?, uploaded_by=?, upload_date=?
        WHERE index=?
    """, (*data, row_id))
    conn.commit()
    conn.close()

# Delete
def delete_dataset(row_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE index=?", (row_id,))
    conn.commit()
    conn.close()