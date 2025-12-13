import os
import sqlite3
import pandas as pd
from app.data.db import *

ticket_csv_path = DATA_DIR / "it_tickets.csv"

# Load the file into the database
def load_ticket_csv(conn):
    ticket_data = pd.read_csv(ticket_csv_path)
    ticket_data.to_sql("it_tickets", conn)

# Create
def create_ticket(ticket_id, priority, description, status, assigned_to, created_at, resolution_hours):
    conn = connect_database()
    conn.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_hours))
    conn.commit()
    conn.close()
    return True

# Read
import sqlite3
from app.data.db import connect_database

def get_all_tickets():
    conn = connect_database()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM it_tickets").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_ticket_by_id(ticket_id):
    conn = connect_database()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM it_tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# Update
def update_ticket(ticket_id, priority, description, status, assigned_to, resolution_hours):
    conn = connect_database()
    conn.execute("""
        UPDATE it_tickets
        SET priority=?, description=?, status=?, assigned_to=?, resolution_time_hours=?
        WHERE ticket_id=?
    """, (priority, description, status, assigned_to, resolution_hours, ticket_id))
    conn.commit()
    conn.close()
    return True

# Delete
def delete_ticket(ticket_id):
    conn = connect_database()
    conn.execute("DELETE FROM it_tickets WHERE ticket_id=?", (ticket_id,))
    conn.commit()
    conn.close()
    return True