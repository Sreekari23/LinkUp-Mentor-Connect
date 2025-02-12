import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from mentors import mentor_page
from mentees import mentee_page
from activities import activities_page
from utils import create_event
from database import create_tables, add_user, get_user, get_activities, print_all_users

# Set up Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path to your OAuth 2.0 client credentials file
CLIENT_SECRET_FILE = r'mentor_connect\client_secret_17091883499-qv76lpge1u8egqijtdpb039tqevnt9tb.apps.googleusercontent.com.json'
st.set_page_config(page_title="Mentor Connect", layout="wide")

# Create tables without dropping them
create_tables()

# Initialize session state variables
if 'creds' not in st.session_state:
    st.session_state['creds'] = None

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

if 'email' not in st.session_state:
    st.session_state['email'] = None

if 'role' not in st.session_state:
    st.session_state['role'] = None

if 'activities' not in st.session_state:
    st.session_state['activities'] = []

if 'signup' not in st.session_state:
    st.session_state['signup'] = False  # Initialize signup state

if 'navigation' not in st.session_state:
    st.session_state['navigation'] = []

def authenticate_user():
    """Authenticate with Google API using OAuth 2.0 and return credentials."""
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def login():
    st.title("Mentor Connect - Login")
    user_id = st.text_input("User ID", key="login_user_id")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        user = get_user(user_id)
        if user:
            print(f"Retrieved user data: {user}")  # Debugging print
            
            # Debugging prints for password comparison
            print(f"Entered password: '{password}'")
            print(f"Stored password: '{user['password']}'")

            # Ensure passwords are stripped of spaces and are compared as strings
            if str(user['password']).strip() == str(password).strip():
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user['user_id']
                st.session_state['email'] = user['email']
                st.session_state['activities'] = get_activities(user['user_id'])

                # Authenticate with Google API after login
                st.session_state['creds'] = authenticate_user()

                # Handle multiple roles and debug role assignment
                print(f"User Roles - Mentor: {user['is_mentor']}, Mentee: {user['is_mentee']}")  # Debugging print
                st.session_state['navigation'] = []
                if user['is_mentor'] == 1:
                    st.session_state['navigation'].append("Mentor")
                if user['is_mentee'] == 1:
                    st.session_state['navigation'].append("Mentee")
                st.session_state['navigation'].append("Activities")

            else:
                st.error("Incorrect password. Please try again.")
                print("Password does not match.")  # Debugging print
        else:
            st.error("User not found. Please register first.")

    # Sign Up button to show the sign-up form
    if st.button("Sign Up", key="signup_button"):
        st.session_state['signup'] = True

# Show the sign-up form if the signup state is True
if st.session_state['signup']:
    st.title("Sign Up for Mentor Connect")
    user_id = st.text_input("User ID", key="signup_user_id")
    password = st.text_input("Password", type="password", key="signup_password")
    email = st.text_input("Email", key="signup_email")
    roles = st.multiselect("Select Roles", ["mentor", "mentee"], key="signup_roles")

    if st.button("Register", key="register_button"):
        if user_id and password and email and roles:
            is_mentor = 1 if "mentor" in roles else 0
            is_mentee = 1 if "mentee" in roles else 0
            add_user(user_id, password, email, is_mentor, is_mentee)
            st.success("User registered successfully. Please log in.")
            st.session_state['signup'] = False
            
            # Print all users for debugging
            print_all_users()  # Add this line
        else:
            st.error("Please fill in all fields.")

# Add logo to sidebar and main content
logo_path = r'mentor_connect\Screenshot 2024-08-31 020524.png'
st.sidebar.image(logo_path, use_column_width=True)
st.image(logo_path, width=200)  # Adjust width as needed

# Main application logic
if not st.session_state['logged_in']:
    login()
else:
    st.sidebar.title(f"Welcome, {st.session_state['user_id']}")
    
    # Add Sign Out button
    if st.sidebar.button("Sign Out", key="signout_button"):
        # Reset session state
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state['email'] = None
        st.session_state['role'] = None
        st.session_state['activities'] = []
        st.session_state['signup'] = False
        st.session_state['creds'] = None
        st.session_state['navigation'] = []
        st.experimental_rerun()  # Refresh the app to show the login screen

    # Dynamically update navigation based on roles
    page = st.sidebar.selectbox("Navigation", st.session_state['navigation'], key="navigation_select")

    if page == "Mentor":
        mentor_page()
    elif page == "Mentee":
        mentee_page()
    elif page == "Activities":
        activities_page()
