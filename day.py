# employee_portal.py

import streamlit as st
import requests

# Replace with your actual n8n webhook URL
N8N_WEBHOOK_URL = "https://your-n8n-webhook-url.com/webhook-path"

# Dummy user database
USER_CREDENTIALS = {
    "john": "password123",
    "jane": "securepass"
}

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Logout Function ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out.")

# --- Login Form ---
def login_form():
    st.title("🔐 Employee Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# --- Action Item Form ---
def action_item_form():
    st.title("📋 Submit Meeting Action Items")
    st.write(f"Welcome, **{st.session_state.username}**")
    
    with st.form("action_form"):
        meeting_date = st.date_input("Meeting Date")
        ag
