# ======================================
# 🌌 INTERPLANETARY PEN PAL APP
# MAIN APP ENTRY POINT
# ======================================

import streamlit as st
import streamlit_authenticator as stauth
from auth import get_user, create_user
from database import SessionLocal, User

st.set_page_config(
    page_title="Interplanetary Pen Pal",
    page_icon="🌌",
    layout="centered"
)

# --- USER AUTHENTICATION ---
db = SessionLocal()

users = db.query(User).all()
credentials = {"usernames": {}}
for user in users:
    credentials["usernames"][user.username] = {"name": user.username, "password": user.hashed_password}

import os

authenticator = stauth.Authenticate(
    credentials,
    "interplanetary_pen_pal", # cookie name
    os.environ.get("STREAMLIT_AUTHENTICATOR_KEY", "abcdef"), # cookie key
    cookie_expiry_days=30,
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.session_state["db"] = db
    st.sidebar.write(f"Welcome, {name}!")
    authenticator.logout("Logout", "sidebar")

    st.title("🌌 Interplanetary Pen Pal")
    st.markdown("---")
    st.markdown("Welcome to a peaceful platform for cosmic correspondence. Create your profile, send messages to human and AI pen pals, and share your dreams with the universe.")
    st.markdown("Use the navigation on the left to explore the different features of the app.")

elif authentication_status is False:
    st.error("Username/password is incorrect")
    db.close()

elif authentication_status is None:
    st.warning("Please enter your username and password")

    # --- REGISTRATION ---
    try:
        if st.checkbox("New user? Register here"):
            with st.form("Registration"):
                email = st.text_input("Email")
                new_username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submitted = st.form_submit_button("Register")
                if submitted:
                    if password == confirm_password:
                        if get_user(db, new_username):
                            st.error("Username already exists")
                        else:
                            create_user(db, new_username, password, email)
                            st.success("You have successfully registered!")
                    else:
                        st.error("Passwords do not match")
    except Exception as e:
        st.error(e)
    db.close()
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.button("Register"):
                if password == confirm_password:
                    if get_user(db, new_username):
                        st.error("Username already exists")
                    else:
                        create_user(db, new_username, password, email)
                        st.success("You have successfully registered!")
                else:
                    st.error("Passwords do not match")
    except Exception as e:
        st.error(e)
    db.close()
