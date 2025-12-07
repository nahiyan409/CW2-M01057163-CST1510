import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.db import DATA_DIR

DATA_TXT = DATA_DIR / "users.txt"

# Migrate from a file
def migrate_users_from_file(conn, filepath=DATA_TXT):
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return
    
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")

def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return(user)

def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()


def get_all_users():
    """Gets Everything"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users"
    )
    users = cursor.fetchall()
    conn.close()
    return(users)

def update_user(old_name, new_name):
    """Updates the username"""
    conn = connect_database()
    curr = conn.cursor()
    sql = "UPDATE users SET username = ? WHERE username = ?"
    param = (new_name, old_name)
    curr.execute(sql, param)
    conn.commit()

def delete_user(user_name):
    """Deletes username"""
    conn = connect_database()
    curr = conn.cursor()
    sql = "DELETE FROM users WHERE username = ?"
    param = (user_name,)
    curr.execute(sql, param)
    conn.commit()