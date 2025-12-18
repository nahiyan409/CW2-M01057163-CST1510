import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database 
from app.data.db import DATA_DIR



# Register users
def register_user(username, password, role="user"):
    conn = connect_database()
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists."

# Login users
def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Username not found.", None

    user_id, uname, stored_hash, role = row

    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        user_dict = {
            "id": user_id,
            "username": uname,
            "role": role
        }
        return True, "Login successful.", user_dict
    else:
        return False, "Invalid password.", None

