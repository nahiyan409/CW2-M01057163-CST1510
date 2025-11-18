import bcrypt

def hash_pwd(password):
    password_byte = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_byte, salt)
    return hashed_password.decode("utf-8")

def verify_password(password, hashed_password):
    pwd = password.encode("utf-8")
    hashed_password_byte = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd, hashed_password_byte)

def register_user():
    user_name = input("Enter your name: ")
    user_password = input("Enter your password: ")
    hidden_pwd = hash_pwd(user_password)
    with open("users.txt", "a") as f:
        f.write(f"{user_name}, {hidden_pwd}\n")
    
    print("User registered successfully!!!")

def login_user():
    user_name = input("Enter your username: ")
    user_password = input("Enter your password: ")
    with open("users.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            name, hash = [item.strip() for item in line.strip().split(",")]
            if name == user_name:
                if verify_password(user_password, hash):
                    print("Login successful!")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    return False
