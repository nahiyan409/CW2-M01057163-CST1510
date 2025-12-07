import os
import sqlite3
import pandas as pd
from app.data.db import DATA_DIR

ticket_csv_path = DATA_DIR / "it_tickets.csv"

# Load the file into the database
def load_ticket_csv(conn):
    ticket_data = pd.read_csv(ticket_csv_path)
    ticket_data.to_sql("it_tickets", conn)

def get_all_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close
    return (data)
