import sqlite3
import os
import pandas as pd
from app.data.db import *

csv_path = DATA_DIR / "cyber_incidents.csv"

# Loading the CSV to the table
def load_csv_to_table(conn):
    cyber_data = pd.read_csv(csv_path)
    cyber_data.to_sql("cyber_incidents", conn)

# Get all incidents
def load_cyber_incidents():
    conn = connect_database(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    conn.close()

    return rows, column_names

# ---------- CRUD OPERATIONS FOR cyber_incidents ----------

def create_incident(data):
    conn = connect_database(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (incident_id, timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()


def update_incident(row_id, data):
    conn = connect_database(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents
        SET incident_id=?, timestamp=?, severity=?, category=?, status=?, description=?
        WHERE index=?
    """, (*data, row_id))
    conn.commit()
    conn.close()


def delete_incident(row_id):
    conn = connect_database(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE index=?", (row_id,))
    conn.commit()
    conn.close()




