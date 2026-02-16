# ======================================
# 👑 ADMIN PANEL
# ======================================

import streamlit as st
from database import SessionLocal, User
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Admin Panel",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    user = get_current_user(db)

    if user and user.is_admin:
        st.title("👑 Admin Panel")
        st.markdown("---")

        st.subheader("Manage Users")
        users = db.query(User).all()

        for u in users:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Username:** {u.username}")
                st.write(f"**Email:** {u.email}")
                st.write(f"**Premium:** {'Yes' if u.is_premium else 'No'}")
            with col2:
                if not u.is_premium:
                    if st.button(f"Make Premium", key=f"premium_{u.id}"):
                        u.is_premium = True
                        db.commit()
                        st.rerun()
            st.markdown("---")
    else:
        st.error("You do not have permission to access this page.")

    db.close()
