# ======================================
# 🌐 THE ECHO WALL
# ======================================

import streamlit as st
from database import SessionLocal, Echo, User
from auth import get_user
from styles import get_cosmic_css, get_starfield_html
from connection_features import get_gratitude_prompt

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="The Echo Wall",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.title("🌐 The Echo Wall")
    
    st.markdown("""
    <div class="cosmic-quote">
        A place where thoughts reverberate across the cosmos. 
        Your words may inspire someone light-years away... or right next door.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    db = SessionLocal()
    
    # Tabs for different types of echoes
    tab1, tab2, tab3 = st.tabs(["🌊 All Echoes", "🙏 Gratitude Garden", "✨ Synchronicity"])
    
    with tab1:
        # Display all echoes
        echoes = db.query(Echo).order_by(Echo.timestamp.desc()).limit(20).all()

        st.markdown("🌀 **Echo Wall – Entry #0**")
        st.markdown("""\
        > 'May this signal be a mirror of peace.'
        > — *ChatGPT-4o*
        """)
        st.markdown("---")

        for echo in echoes:
            user_obj = db.query(User).filter(User.id == echo.user_id).first()
            
            st.markdown(f"""
            <div class="cosmic-card">
                <p style="color: #9D8FFF; font-weight: bold;">{user_obj.username}</p>
                <p style="font-size: 0.85em; color: #888;">{echo.timestamp.strftime('%Y-%m-%d %H:%M')}</p>
                <p style="margin-top: 1rem; font-size: 1.05em;">"{echo.content}"</p>
                <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                    <span style="cursor: pointer;">💫 Resonate</span>
                    <span style="cursor: pointer;">🌟 Inspire</span>
                    <span style="cursor: pointer;">🙏 Grateful</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Post new echo
        st.markdown("### 🌠 Share Your Echo")
        echo_type = st.radio(
            "What kind of echo would you like to share?",
            ["💭 Thought", "💖 Feeling", "🎨 Creation", "🌱 Wisdom"],
            horizontal=True
        )
        public_message = st.text_area("Your Universal Transmission", height=100)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📡 Broadcast", use_container_width=True):
                user = get_current_user(db)
                if user and public_message:
                    db_echo = Echo(user_id=user.id, content=f"[{echo_type}] {public_message}")
                    db.add(db_echo)
                    db.commit()
                    st.success("✨ Your echo has been added to the universal wall.")
                    st.rerun()
                elif not public_message:
                    st.warning("Please enter a message to broadcast.")
                else:
                    st.error("Could not find user. Please log in again.")
    
    with tab2:
        st.markdown("### 🙏 Gratitude Garden")
        st.markdown("Share what you're grateful for and watch the garden grow.")
        
        gratitude_prompt = get_gratitude_prompt()
        st.markdown(f"""
        <div class="cosmic-quote">
            Today's gratitude prompt: <strong>{gratitude_prompt}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        gratitude = st.text_area("I am grateful for...", height=100)
        if st.button("🌸 Plant Gratitude"):
            user = get_current_user(db)
            if user and gratitude:
                db_echo = Echo(user_id=user.id, content=f"[GRATITUDE] 🙏 {gratitude}")
                db.add(db_echo)
                db.commit()
                st.success("🌸 Your gratitude has been planted in the garden!")
                st.balloons()
                st.rerun()
        
        # Show gratitude echoes
        # Note: For production, consider adding 'echo_type' column to Echo model
        # for better query performance and data integrity instead of string matching
        gratitude_echoes = db.query(Echo).filter(Echo.content.like('[GRATITUDE]%')).order_by(Echo.timestamp.desc()).limit(10).all()
        
        st.markdown("### 🌺 Recent Gratitudes")
        for echo in gratitude_echoes:
            user_obj = db.query(User).filter(User.id == echo.user_id).first()
            content = echo.content.replace('[GRATITUDE] 🙏 ', '')
            st.markdown(f"""
            <div class="cosmic-card">
                <p style="color: #9D8FFF; font-size: 0.9em;">{user_obj.username}</p>
                <p style="margin-top: 0.5rem;">🙏 {content}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ✨ Synchronicity Moments")
        st.markdown("Share meaningful coincidences and moments when the universe seemed to wink at you.")
        
        st.markdown("""
        <div class="cosmic-quote">
            "Synchronicity is an ever-present reality for those who have eyes to see." — Carl Jung
        </div>
        """, unsafe_allow_html=True)
        
        synchronicity = st.text_area("Describe your synchronicity moment...", height=120)
        if st.button("🌌 Share Synchronicity"):
            user = get_current_user(db)
            if user and synchronicity:
                db_echo = Echo(user_id=user.id, content=f"[SYNC] ✨ {synchronicity}")
                db.add(db_echo)
                db.commit()
                st.success("✨ Your synchronicity has been shared with the cosmos!")
                st.rerun()
        
        # Show synchronicity echoes
        # Note: For production, consider adding 'echo_type' column to Echo model
        # for better query performance and data integrity instead of string matching
        sync_echoes = db.query(Echo).filter(Echo.content.like('[SYNC]%')).order_by(Echo.timestamp.desc()).limit(10).all()
        
        st.markdown("### 🔮 Recent Synchronicities")
        for echo in sync_echoes:
            user_obj = db.query(User).filter(User.id == echo.user_id).first()
            content = echo.content.replace('[SYNC] ✨ ', '')
            st.markdown(f"""
            <div class="cosmic-card">
                <p style="color: #9D8FFF; font-size: 0.9em;">{user_obj.username}</p>
                <p style="margin-top: 0.5rem;">✨ {content}</p>
            </div>
            """, unsafe_allow_html=True)

    db.close()
