from hashing_pwd import register_user, login_user
import bcrypt

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
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Goodbye user!!!")
            break

if __name__ == "__main__":
    main()