import streamlit as st
from app.services.user_service import register_user

st.title("Create a New Account")

username = st.text_input("Choose a Username")
password = st.text_input("Choose a Password", type="password")

if st.button("Register"):
    if username and password:
        ok, message = register_user(username, password)
        if ok:
            st.success(message)
            st.info("Return to Home to log in.")
        else:
            st.error(message)
    else:
        st.warning("Please enter both username and password.")
