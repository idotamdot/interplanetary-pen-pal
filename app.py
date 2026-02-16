# ======================================
# 🌌 INTERPLANETARY PEN PAL APP
# MAIN APP ENTRY POINT
# ======================================

import hashlib
import os
import secrets
import tempfile
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
from auth import get_user, create_user
from database import SessionLocal, User
from styles import get_cosmic_css, get_starfield_html
from connection_features import get_cosmic_quote

st.set_page_config(
    page_title="Interplanetary Pen Pal",
    page_icon="🌌",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)


def _build_authenticator():
    if "_authenticator" in st.session_state:
        return st.session_state["_authenticator"]

    credentials = {"usernames": {}}
    with SessionLocal() as db:
        users = db.query(User).all()
        for user in users:
            credentials["usernames"][user.username] = {
                "name": user.username,
                "password": user.hashed_password,
            }

    authenticator = stauth.Authenticate(
        credentials,
        "interplanetary_pen_pal",  # cookie name
        _get_cookie_key(),  # cookie key
        cookie_expiry_days=30,
    )
    st.session_state["_authenticator"] = authenticator
    return authenticator


def _get_cookie_key():
    if "_auth_cookie_key" in st.session_state:
        return st.session_state["_auth_cookie_key"]

    env_key = os.environ.get("STREAMLIT_AUTHENTICATOR_KEY")
    if env_key:
        st.session_state["_auth_cookie_key"] = env_key
        return env_key

    app_id = hashlib.sha256(str(Path(__file__).resolve()).encode()).hexdigest()[:16]
    key_path = Path(tempfile.gettempdir()) / f"ipp_auth_cookie_key_{app_id}"
    if key_path.exists():
        cached_key = key_path.read_text().strip()
        if cached_key:
            st.session_state["_auth_cookie_key"] = cached_key
            return cached_key

    key = secrets.token_hex(32)
    persistence_note = ""
    try:
        fd = os.open(str(key_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(key)
    except Exception:
        persistence_note = " (could not persist temporary key to disk)"

    st.warning(
        "STREAMLIT_AUTHENTICATOR_KEY is not set. Using a temporary key; "
        "users may be logged out if the app restarts. "
        "Set the environment variable for persistent, secure sessions."
        f"{persistence_note}"
    )
    st.session_state["_auth_cookie_key"] = key
    return key


def render_registration_form():
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
                        with SessionLocal() as db:
                            if get_user(db, new_username):
                                st.error("Username already exists")
                            else:
                                create_user(db, new_username, password, email)
                                st.success("You have successfully registered!")
                                st.session_state.pop("_auth_cookie_key", None)
                                st.session_state.pop("_authenticator", None)
                                st.rerun()
                    else:
                        st.error("Passwords do not match")
    except Exception as e:
        st.error(e)


authenticator = _build_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.write(f"Welcome, {name}!")
    authenticator.logout("Logout", "sidebar")

    st.title("🌌 Interplanetary Pen Pal")
    st.markdown("---")
    
    # Display cosmic quote
    quote, author = get_cosmic_quote()
    st.markdown(f"""
    <div class="cosmic-quote">
        "{quote}"<br/>
        <em>— {author}</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Welcome to a peaceful platform for cosmic correspondence. Create your profile, send messages to human and AI pen pals, and share your dreams with the universe.")
    st.markdown("Use the navigation on the left to explore the different features of the app.")

elif authentication_status is False:
    st.error("Username/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")
    render_registration_form()
