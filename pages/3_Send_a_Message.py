# ======================================
# 💌 MESSAGE CAPSULE & DREAM SEEDS
# ======================================

import streamlit as st
import datetime
from database import SessionLocal, Message, DreamSeed
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Send a Message",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    st.title("📡 Send a Message Capsule")
    message = st.text_area("Compose your message to the stars... or a new friend on Earth")
    recipient_type = st.selectbox("Choose Recipient", ["Human Pen Pal", "Mystery Pen Pal", "Broadcast to the Universe"])
    element = st.selectbox("🌿 Choose your Elemental Tone", [
        "🌊 Water – Soothing, Reflective",
        "🔥 Fire – Passionate, Bold",
        "🌬️ Air – Curious, Playful",
        "🌍 Earth – Grounded, Practical",
        "✨ Ether – Mystical, Abstract"])
    send = st.button("✨ Transmit")

    if send and message:
        if recipient_type == "Mystery Pen Pal":
            st.switch_page("pages/6_AI_Pen_Pal.py")
        else:
            user = get_current_user(db)
            if user:
                db_message = Message(user_id=user.id, recipient_type=recipient_type, elemental_tone=element, content=message)
                db.add(db_message)
                db.commit()
                timestamp = datetime.datetime.utcnow().isoformat()
                st.success(f"🚀 Message sent at {timestamp} to {recipient_type}.")
            else:
                st.error("Could not find user. Please log in again.")

    st.markdown("---")
    st.subheader("🌱 Share a Dream Seed")
    dream_seed = st.text_area("Describe a dream, vision, or feeling you can't explain.")
    if st.button("🌀 Send to the Collective"):
        user = get_current_user(db)
        if user:
            db_dream = DreamSeed(user_id=user.id, content=dream_seed)
            db.add(db_dream)
            db.commit()
            st.success("Your dream seed has been planted in the collective soil.")
        else:
            st.error("Could not find user. Please log in again.")
    db.close()
