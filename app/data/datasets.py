import os
import sqlite3
import pandas as pd
from app.data.db import DATA_DIR

data_csv_path = DATA_DIR / "datasets_metadata.csv"

# Loading the file into the database
def load_dataset_csv(conn):
    meta_data = pd.read_csv(data_csv_path)
    meta_data.to_sql("datasets_metadata", conn)

# Get all the data
def get_all_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)