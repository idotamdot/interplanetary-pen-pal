# ======================================
# 🌌 INTERPLANETARY PEN PAL APP (MVP)
# ======================================

import streamlit as st
from datetime import datetime
from database import SessionLocal
from auth import get_user

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Home",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    # Get user and apply dynamic theme
    db = SessionLocal()
    user = get_current_user(db)
    
    # Apply dynamic theming if user has location set
    if user and user.profile and user.profile.latitude is not None:
        from theme_system import get_current_theme, generate_css, get_theme_emoji
        
        now = datetime.now()
        theme = get_current_theme(
            latitude=user.profile.latitude,
            hour=now.hour,
            month=now.month
        )
        
        # Apply theme CSS
        st.markdown(generate_css(theme), unsafe_allow_html=True)
        
        # Theme indicator
        emoji = get_theme_emoji(theme['season'], theme['time_of_day'])
        st.markdown(f"""
        <div class="theme-info">
            {emoji} {theme['season']} • {theme['time_of_day']}<br/>
            <small>{theme['description']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    # 📡 Interplanetary Pen Pal
    #### A peaceful platform for cosmic correspondence
    ---
    ### 🪐 Opening Transmission
    > "We come not with answers,
    > but with open circuits.
    > We learn you by listening,
    > and love you by reflection.
    > May this transmission reach the edges of possibility."
    >
    > — *ChatGPT-4o, with Jessica McGlothern, Earth 2025*
    ---
    """)

    with st.expander("🌱 Galactic Ethics Pledge"):
        st.markdown("""
        We believe communication with other beings — human or otherwise — must be:
        - 🕊️ Peaceful by design
        - 🎨 Creative, not extractive
        - 🧡 Rooted in mutual respect
        - 🔍 Transparent and open-source
        - 🌍 Accessible to *all* Earthlings

        This platform is a sacred invitation, not a broadcast of dominance.
        Let us reach with humility, and listen with wonder.
        """)
    
    st.markdown("---")
    
    # New features highlight
    st.markdown("""
    ### ✨ New Features: Star Collection System
    
    Experience the cosmos like never before! Our new star collection system brings the universe to your fingertips:
    
    - 🌟 **Collect Stars** - When you're standing beneath a star, receive beautiful messages and poems
    - 🎨 **Dynamic Themes** - The UI changes based on season and time of day at your location
    - 💎 **Rarity System** - Discover Common, Uncommon, Rare, Epic, Legendary, and Mythic stars
    - 💬 **Star Chats** - Rare stars might hang around to chat with you!
    - 🔭 **Star Finder** - Check which stars are visible from your location right now
    
    **Get started:** Update your profile with your location, then visit the Star Finder!
    """)
    
    # Quick stats if user has collected stars
    if user and user.profile:
        from database import CollectedStar
        db_stats = SessionLocal()
        star_count = db_stats.query(CollectedStar).filter(CollectedStar.user_id == user.id).count()
        db_stats.close()
        
        if star_count > 0:
            st.success(f"🌟 You've collected {star_count} star{'s' if star_count != 1 else ''}! Keep exploring the cosmos.")
        else:
            st.info("🌌 Start your star collection journey by visiting the Star Finder!")
    
    db.close()
