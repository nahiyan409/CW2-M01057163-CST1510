from hashing_pwd import register_user, login_user
import bcrypt
import sqlite3
from app.data.db import *

def menu():
    print("Hello user!!!")
    print("Choose from the options below")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input(" > ")
        if choice == "1":
            conn = connect_database(DB_PATH)
            register_user(conn)
        elif choice == "2":
            conn = connect_database(DB_PATH)
            if login_user(conn):
                print("LOGIN SUCESSFULL!!")
        elif choice == "3":
            print("Goodbye user!!!")
            break
    
if __name__ == "__main__":
    main()