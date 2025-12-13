import streamlit as st
from app.data.schema import create_users_table
from app.data.db import *
from app.services.user_service import login_user

st.set_page_config(page_title="Multi-Domain Intelligence Platform", page_icon="🌐")

# Create database table on startup
conn = connect_database(DB_PATH)
create_users_table(conn)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None

st.title("Multi-Domain Intelligence Platform")
st.subheader("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    ok, message, user = login_user(username, password)

    if ok:
        st.session_state["logged_in"] = True
        st.session_state["user"] = user
        st.session_state["username"] = user["username"]
        st.session_state["role"] = user["role"]
        st.success(f"Welcome, {user['username']}!")
        st.info("Go to **Dashboard** from the sidebar.")

    else:
        st.error(message)

st.info("Don't have an account? Go to the **Register** page in the sidebar.")
