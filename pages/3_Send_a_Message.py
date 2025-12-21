# ======================================
# 💌 MESSAGE CAPSULE & DREAM SEEDS
# ======================================

import streamlit as st
import datetime
from database import SessionLocal, Message, DreamSeed
from auth import get_user
from styles import get_cosmic_css, get_starfield_html
from connection_features import ELEMENTAL_ENERGIES

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Send a Message",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    st.title("📡 Send a Message Capsule")
    
    st.markdown("""
    <div class="cosmic-quote">
        Your words carry energy across space and time. 
        Choose them with intention, infuse them with meaning.
    </div>
    """, unsafe_allow_html=True)
    
    # Message type selection with more meaning
    message_type = st.radio(
        "🌟 What kind of message is this?",
        [
            "💌 Letter to a Future Friend",
            "🔮 Message to Your Future Self", 
            "🌊 Release into the Universe",
            "✨ Intention Setting",
            "🙏 Prayer or Blessing"
        ],
        help="Each type of message carries different energy and intention"
    )
    
    # Show guidance based on message type
    guidance = {
        "💌 Letter to a Future Friend": "Write as if you're speaking to someone who will deeply understand you, even if you haven't met yet.",
        "🔮 Message to Your Future Self": "What do you want to remember? What wisdom are you discovering now that future-you should know?",
        "🌊 Release into the Universe": "What are you ready to let go of? Release it with love and trust.",
        "✨ Intention Setting": "State clearly what you're calling into your life. Write it as if it's already happening.",
        "🙏 Prayer or Blessing": "Offer your hopes, gratitude, or blessings - for yourself, others, or the world."
    }
    
    st.markdown(f"""
    <div style="background: rgba(108, 99, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <em>{guidance[message_type]}</em>
    </div>
    """, unsafe_allow_html=True)
    
    message = st.text_area(
        "✍️ Compose your message...", 
        height=200,
        placeholder="Let your heart speak..."
    )
    
    # Elemental tone selector with more context
    st.markdown("### 🌿 Choose Your Message's Energy")
    element_options = list(ELEMENTAL_ENERGIES.keys())
    element = st.selectbox(
        "What energy does this message carry?",
        element_options,
        format_func=lambda x: f"{x} - {ELEMENTAL_ENERGIES[x]['quality']}"
    )
    
    if element:
        element_info = ELEMENTAL_ENERGIES[element]
        st.markdown(f"""
        <div style="background: {element_info['color']}20; border-left: 4px solid {element_info['color']}; 
             padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            {element_info['message']}
        </div>
        """, unsafe_allow_html=True)
    
    # Recipient selection
    recipient_type = st.selectbox(
        "🎯 Where should this message go?",
        [
            "Human Pen Pal",
            "Mystery Pen Pal", 
            "Broadcast to the Universe",
            "Keep Private (Just for me)"
        ]
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        send = st.button("✨ Transmit", use_container_width=True)

    if send and message:
        if recipient_type == "Mystery Pen Pal":
            st.switch_page("pages/6_AI_Pen_Pal.py")
        else:
            user = get_current_user(db)
            if user:
                db_message = Message(
                    user_id=user.id, 
                    recipient_type=f"{message_type} -> {recipient_type}", 
                    elemental_tone=element, 
                    content=message
                )
                db.add(db_message)
                db.commit()
                timestamp = datetime.datetime.utcnow().isoformat()
                
                st.success(f"🚀 Message transmitted at {timestamp}")
                st.markdown("""
                <div class="cosmic-card">
                    <p style="text-align: center; font-size: 1.1em;">
                        Your message has been sent into the cosmos. 🌌<br/>
                        It carries your intention and will find its way to where it needs to go.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Could not find user. Please log in again.")
    elif send and not message:
        st.warning("Please compose a message before transmitting.")

    st.markdown("---")
    
    # Dream Seeds Section
    st.markdown("## 🌱 Plant a Dream Seed")
    st.markdown("""
    <div class="cosmic-quote">
        Dream seeds are whispers of possibility. Plant them in the collective field 
        and watch how the universe conspires to help them grow.
    </div>
    """, unsafe_allow_html=True)
    
    dream_seed = st.text_area(
        "🌠 Describe a dream, vision, or feeling you can't quite explain...",
        height=120,
        placeholder="It doesn't have to make sense. Sometimes the most important things are the ones we can't put into words."
    )
    
    if st.button("🌀 Plant in the Collective Soil"):
        user = get_current_user(db)
        if user and dream_seed:
            db_dream = DreamSeed(user_id=user.id, content=dream_seed)
            db.add(db_dream)
            db.commit()
            st.success("🌱 Your dream seed has been planted!")
            st.markdown("""
            <div class="cosmic-card">
                <p style="text-align: center;">
                    Your dream is now part of the collective garden. 🌺<br/>
                    Water it with intention, and watch what blooms.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif not dream_seed:
            st.warning("Please describe your dream seed.")
        else:
            st.error("Could not find user. Please log in again.")
    
    db.close()
