# ======================================
# 🌌 COSMIC PROFILE
# ======================================

import streamlit as st
from database import SessionLocal, Profile
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Profile",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.title("🌟 Create Your Cosmic Profile")

    db = SessionLocal()
    user = get_current_user(db)

    if user:
        if not user.is_premium:
            st.page_link("pages/5_Support_the_Project.py", label="Upgrade to Premium")

        profile = db.query(Profile).filter(Profile.user_id == user.id).first()

        if profile:
            name = st.text_input("Your Star Name", value=profile.star_name)
            symbol = st.text_input("Your Symbolic Signature (emoji, glyph, constellation)", value=profile.symbol)
            dream = st.text_area("Share a Dream, Memory, or Origin Story", value=profile.dream)
        else:
            name = st.text_input("Your Star Name")
            symbol = st.text_input("Your Symbolic Signature (emoji, glyph, constellation)")
            dream = st.text_area("Share a Dream, Memory, or Origin Story")

        if st.button("Save Profile"):
            if profile:
                profile.star_name = name
                profile.symbol = symbol
                profile.dream = dream
            else:
                profile = Profile(user_id=user.id, star_name=name, symbol=symbol, dream=dream)
                db.add(profile)

            db.commit()
            db.refresh(profile)

            st.success("🛸 Profile Registered for Interplanetary Exchange")
            st.markdown(f"🌌 **{name}** — {symbol}")
            st.markdown(f"🧬 *\"{dream}\"*")
    else:
        st.error("Could not find user. Please log in again.")

    db.close()
