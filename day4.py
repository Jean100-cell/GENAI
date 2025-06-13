# employee_portal.py

import streamlit as st
import requests

# Replace with your actual n8n webhook URL
N8N_WEBHOOK_URL = "https://jean1025.app.n8n.cloud/webhook-test/c3e8a384-2390-4e1e-8ecb-f7c2aeafb063"

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
            st.rerun()
        else:
            st.error("Invalid username or password")

# --- Action Item Form ---
def action_item_form():
    st.title("📋 Submit Meeting Action Items")
    st.write(f"Welcome, **{st.session_state.username}**")
    
    with st.form("action_form"):
        meeting_date = st.date_input("Meeting Date")
        email = st.text_input("Email")  # ✅ Email field added
        agenda = st.text_area("Meeting Agenda")
        action_items = st.text_area("Action Items")
        submit = st.form_submit_button("Submit")

        if submit:
            payload = {
                "username": st.session_state.username,
                "email": email,
                "meeting_date": meeting_date.isoformat(),
                "agenda": agenda,
                "action_items": action_items
            }
            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("✅ Action items submitted successfully!")
                else:
                    st.error(f"Failed to submit. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    st.button("Logout", on_click=logout)

# --- App Execution ---
if st.session_state.logged_in:
    action_item_form()
else:
    login_form()
