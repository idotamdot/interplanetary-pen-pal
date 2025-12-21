# ======================================
# 🌌 COSMIC PROFILE
# ======================================

import streamlit as st
from database import SessionLocal, Profile
from auth import get_user
from styles import get_cosmic_css, get_starfield_html
from connection_features import CONSTELLATIONS, MOOD_COLORS

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Profile",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.title("🌟 Create Your Cosmic Profile")
    
    st.markdown("""
    <div class="cosmic-quote">
        Your profile is your unique signature in the cosmos. 
        Choose elements that resonate with your essence.
    </div>
    """, unsafe_allow_html=True)

    db = SessionLocal()
    user = get_current_user(db)

    if user:
        if not user.is_premium:
            st.page_link("pages/5_Support_the_Project.py", label="✨ Upgrade to Premium for more features")

        profile = db.query(Profile).filter(Profile.user_id == user.id).first()

        col1, col2 = st.columns([2, 1])
        
        with col1:
            if profile:
                name = st.text_input("✨ Your Star Name", value=profile.star_name)
            else:
                name = st.text_input("✨ Your Star Name", placeholder="e.g., Nova Wanderer, Stellar Dreamer")
        
        with col2:
            # Constellation selector
            current_symbol = profile.symbol if profile else None
            if current_symbol and current_symbol in CONSTELLATIONS:
                default_index = CONSTELLATIONS.index(current_symbol)
            else:
                default_index = 0
            constellation = st.selectbox(
                "🌌 Your Constellation", 
                CONSTELLATIONS,
                index=default_index
            )
        
        # Mood/Energy
        st.markdown("### 💫 Current Energy")
        mood_list = list(MOOD_COLORS.keys())
        mood = st.select_slider(
            "How are you feeling right now?",
            options=mood_list
        )
        
        if mood:
            mood_color = MOOD_COLORS[mood]
            st.markdown(f"""
            <div style="background: {mood_color}20; border-left: 4px solid {mood_color}; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                You're radiating <strong>{mood}</strong> energy right now.
            </div>
            """, unsafe_allow_html=True)
        
        # Dream/Story
        st.markdown("### 🌠 Your Cosmic Story")
        if profile:
            dream = st.text_area(
                "Share a Dream, Memory, or Origin Story", 
                value=profile.dream,
                height=150,
                help="This is your space to express what makes you... you."
            )
        else:
            dream = st.text_area(
                "Share a Dream, Memory, or Origin Story",
                height=150,
                placeholder="What brings you to this cosmic gathering? What dreams do you carry?",
                help="This is your space to express what makes you... you."
            )
        
        # Intentions
        st.markdown("### 🎯 Your Intentions")
        intentions = st.text_area(
            "What are you calling into your life?",
            height=100,
            placeholder="e.g., More meaningful connections, creative flow, inner peace..."
        )

        if st.button("🚀 Save Profile", use_container_width=True):
            if profile:
                profile.star_name = name
                profile.symbol = constellation
                profile.dream = dream
            else:
                profile = Profile(user_id=user.id, star_name=name, symbol=constellation, dream=dream)
                db.add(profile)

            db.commit()
            db.refresh(profile)

            st.success("🛸 Profile Updated!")
            
            # Display the profile beautifully
            st.markdown("---")
            st.markdown(f"""
            <div class="cosmic-card">
                <h2 style="text-align: center;">{constellation.split(' ')[0]} {name}</h2>
                <p style="text-align: center; font-size: 1.2em;">{constellation}</p>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(108, 99, 255, 0.1); border-radius: 10px;">
                    <p style="font-style: italic;">"{dream}"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Could not find user. Please log in again.")

    db.close()
