import bcrypt
from app.data.users import *
from app.data.db import *

def hash_pwd(password):
    password_byte = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_byte, salt)
    return hashed_password.decode("utf-8")

def verify_password(password, hashed_password):
    pwd = password.encode("utf-8")
    hashed_password_byte = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd, hashed_password_byte)

def register_user(conn):
    user_name = input("Enter your name: ")
    user_password = input("Enter your password: ")
    hidden_pwd = hash_pwd(user_password)
    insert_user(user_name, hidden_pwd, role= 'user')
    
    print("User registered successfully!!!")

def login_user(conn):
    user_name = input("Enter your username: ")
    user_password = input("Enter your password: ")
    id, fetched_name, fetched_hash, role, created_at= get_user_by_username(user_name)
    print(f"Welcome {fetched_name}")
    if user_name == fetched_name and verify_password(user_password, fetched_hash):
        return True
    return False
