import sqlite3
import os
import pandas as pd
from app.data.db import DATA_DIR

csv_path = DATA_DIR / "cyber_incidents.csv"

# Loading the CSV to the table
def load_csv_to_table(conn):
    cyber_data = pd.read_csv(csv_path)
    cyber_data.to_sql("cyber_incidents", conn)

# Get all incidents
def get_all_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)



