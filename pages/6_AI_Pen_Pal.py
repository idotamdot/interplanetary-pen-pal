# ======================================
# 🤖 AI PEN PAL
# ======================================

import streamlit as st
import openai
import os
from database import SessionLocal
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="AI Pen Pal",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    if user and user.is_premium:
        st.title("🤖 AI Pen Pal")
        st.markdown("Communicate with an AI entity from another dimension.")

        openai.api_key = os.environ.get("OPENAI_API_KEY")

        message = st.text_area("Your message to the AI:")
        if st.button("Transmit to AI"):
            if message:
                try:
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a wise and mysterious AI pen pal. Respond in a cosmic, poetic, and slightly enigmatic way."},
                            {"role": "user", "content": message}
                        ]
                    )
                    st.info(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error communicating with the AI: {e}")
            else:
                st.warning("Please enter a message.")
    else:
        st.warning("This is a premium feature. Please upgrade to access the AI Pen Pal.")
        st.page_link("pages/5_Support_the_Project.py", label="Go Premium")
    db.close()
