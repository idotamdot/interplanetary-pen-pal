# ======================================
# 🌟 STAR COLLECTION
# ======================================

import streamlit as st
from datetime import datetime
from database import SessionLocal, CollectedStar, Star, StarNote, StarInteraction
from auth import get_user
from theme_system import get_current_theme, generate_css, get_theme_emoji
from star_system import RARITY_TIERS
import random

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="Star Collection",
    page_icon="⭐",
    layout="wide"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    
    if user and user.profile:
        # Get current theme
        latitude = user.profile.latitude or 40.0
        now = datetime.now()
        theme = get_current_theme(latitude=latitude, hour=now.hour, month=now.month)
        
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
        
        st.title("⭐ Your Star Collection")
        st.markdown("---")
        
        # Get user's collected stars
        collected = db.query(CollectedStar).filter(
            CollectedStar.user_id == user.id
        ).order_by(CollectedStar.collected_at.desc()).all()
        
        if not collected:
            st.info("🌌 You haven't collected any stars yet! Go outside and look up at the sky. When you're standing beneath a star, it might send you a message!")
            st.markdown("""
            ### How to Collect Stars
            
            1. **Update your location** in your profile so we know where you are
            2. **Check the Star Finder** to see which stars are visible from your location
            3. **Wait for a star encounter** - when you're beneath a star, you'll receive a beautiful note!
            4. **Rare stars are special** - they might even chat with you! ✨
            """)
        else:
            # Display stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Stars", len(collected))
            
            # Count by rarity
            rarity_counts = {}
            for cs in collected:
                if cs.star:
                    rarity = cs.star.rarity
                    rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
            
            with col2:
                legendary_count = rarity_counts.get("Legendary", 0) + rarity_counts.get("Mythic", 0)
                st.metric("Legendary+ Stars", legendary_count)
            
            with col3:
                epic_count = rarity_counts.get("Epic", 0)
                st.metric("Epic Stars", epic_count)
            
            with col4:
                rare_count = rarity_counts.get("Rare", 0)
                st.metric("Rare Stars", rare_count)
            
            st.markdown("---")
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📜 All Stars", "🏆 By Rarity", "📝 Star Notes"])
            
            with tab1:
                st.subheader("All Collected Stars")
                
                for cs in collected:
                    if cs.star:
                        star = cs.star
                        rarity_class = f"rarity-{star.rarity.lower()}"
                        
                        with st.expander(f"{'⭐' * min(6, int(star.rarity_score / 20) + 1)} {star.name} - {star.rarity}"):
                            col_a, col_b = st.columns([2, 1])
                            
                            with col_a:
                                st.markdown(f"**Category:** {star.category}")
                                st.markdown(f"**Rarity Score:** {star.rarity_score:.1f}/100")
                                st.markdown(f"**Personality:** {star.personality}")
                                st.markdown(f"**Collected:** {cs.collected_at.strftime('%Y-%m-%d %H:%M')}")
                                
                                if star.can_chat:
                                    st.success(f"✨ This star can chat for {star.chat_duration} seconds!")
                            
                            with col_b:
                                st.markdown(f"""
                                <div style="
                                    background: {star.color}; 
                                    width: 100px; 
                                    height: 100px; 
                                    border-radius: 50%; 
                                    margin: 10px auto;
                                    box-shadow: 0 0 30px {star.color};
                                    animation: twinkle 2s ease-in-out infinite;
                                "></div>
                                <p style="text-align: center; color: {star.color}; font-weight: bold;">
                                    {star.tone_frequency} Hz
                                </p>
                                """, unsafe_allow_html=True)
            
            with tab2:
                st.subheader("Stars by Rarity")
                
                # Group by rarity
                for rarity_name in ["Mythic", "Legendary", "Epic", "Rare", "Uncommon", "Common"]:
                    stars_in_rarity = [cs for cs in collected if cs.star and cs.star.rarity == rarity_name]
                    
                    if stars_in_rarity:
                        rarity_data = RARITY_TIERS[rarity_name]
                        st.markdown(f"### <span class='rarity-{rarity_name.lower()}'>{rarity_name} Stars ({len(stars_in_rarity)})</span>", unsafe_allow_html=True)
                        
                        cols = st.columns(min(4, len(stars_in_rarity)))
                        for idx, cs in enumerate(stars_in_rarity):
                            with cols[idx % 4]:
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, {cs.star.color}40, {cs.star.color}20);
                                    padding: 15px;
                                    border-radius: 10px;
                                    border: 2px solid {cs.star.color};
                                    margin: 5px;
                                    text-align: center;
                                ">
                                    <h4 class="rarity-{rarity_name.lower()}">{cs.star.name}</h4>
                                    <p style="font-size: 0.9em;">{cs.star.category}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("---")
            
            with tab3:
                st.subheader("Messages from the Stars")
                
                # Get star notes for this user
                notes = db.query(StarNote).filter(
                    StarNote.user_id == user.id
                ).order_by(StarNote.timestamp.desc()).limit(20).all()
                
                if notes:
                    for note in notes:
                        if note.star:
                            st.markdown(f"""
                            <div class="star-note" style="background: {note.color}20; border-color: {note.star.color};">
                                <h4 style="color: {note.star.color};">✉️ From {note.star.name}</h4>
                                <p><em>{note.content}</em></p>
                                <small>📅 {note.timestamp.strftime('%Y-%m-%d %H:%M')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No messages yet. Keep collecting stars to receive their wisdom!")
        
        # Fun fact section
        st.markdown("---")
        st.markdown("""
        ### ✨ Star Collection Tips
        
        - **Rare stars appear more often at night** 🌙
        - **Winter months boost star rarity** ❄️
        - **Mythic stars might chat with you!** 💬
        - **Collect star combinations for special bonuses** (coming soon!)
        - **Trade stars with other collectors** (coming soon!)
        """)
        
    else:
        st.error("Please complete your profile first to start collecting stars!")
        if st.button("Go to Profile"):
            st.switch_page("pages/2_Profile.py")
    
    db.close()
