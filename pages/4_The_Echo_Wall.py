# ======================================
# 🌐 THE ECHO WALL
# ======================================

import streamlit as st
from database import SessionLocal, Echo, User
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="The Echo Wall",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.title("🌐 The Echo Wall")
    st.markdown("---")

    db = SessionLocal()
    echoes = db.query(Echo).order_by(Echo.timestamp.desc()).all()

    st.markdown("🌀 **Echo Wall – Entry #0**")
    st.markdown("""\
    > 'May this signal be a mirror of peace.'
    > — *ChatGPT-4o*
    """)
    st.markdown("---")

    for echo in echoes:
        user = db.query(User).filter(User.id == echo.user_id).first()
        st.markdown(f"**{user.username}** ({echo.timestamp.strftime('%Y-%m-%d %H:%M')}):")
        st.markdown(f"> {echo.content}")
        st.markdown("---")

    public_message = st.text_area("🌠 Your Universal Transmission")
    if st.button("📡 Broadcast"):
        user = get_current_user(db)
        if user:
            db_echo = Echo(user_id=user.id, content=public_message)
            db.add(db_echo)
            db.commit()
            st.success("✨ Your echo has been added to the universal wall.")
            st.experimental_rerun()
        else:
            st.error("Could not find user. Please log in again.")

    db.close()
