# ======================================
# 💎 GO PREMIUM
# ======================================

import streamlit as st
from database import SessionLocal
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Go Premium",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.title("💎 Go Premium")
    st.markdown("---")
    st.markdown("""
    Upgrade to a premium account to unlock exclusive features, including the AI Pen Pal.

    **Benefits of Premium:**
    - 🤖 Access to the AI Pen Pal
    - ✨ Priority support
    - 💖 Support the continued development of the Interplanetary Pen Pal project

    **Price:** $5/month
    """)

    st.link_button("Upgrade to Premium (via Stripe)", "https://your-stripe-link.com")

    st.markdown("---")
    st.markdown("After upgrading, your account will be automatically updated to premium. If you have any issues, please contact us.")
    db = SessionLocal()
    # a db session is not needed on this page, but we create it for consistency
    db.close()
