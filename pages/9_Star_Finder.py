# ======================================
# 🔭 STAR FINDER - Check for Star Encounters
# ======================================

import streamlit as st
from datetime import datetime
from database import SessionLocal, Star, CollectedStar, StarNote, StarInteraction, Profile
from auth import get_user
from theme_system import get_current_theme, generate_css, get_theme_emoji
from star_system import (
    check_star_alignment, 
    get_visible_stars, 
    generate_star_message,
    calculate_rarity_score,
    get_rarity_tier,
    can_star_chat,
    STAR_DATABASE
)
import random

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

def initialize_stars(db):
    """Initialize the star database if empty."""
    existing_count = db.query(Star).count()
    if existing_count == 0:
        for star_data in STAR_DATABASE:
            # Calculate initial rarity
            rarity_score = calculate_rarity_score(
                star_data["base_rarity"],
                star_data["category"]
            )
            rarity_tier = get_rarity_tier(rarity_score)
            can_chat_flag, chat_duration = can_star_chat(rarity_tier)
            
            star = Star(
                name=star_data["name"],
                category=star_data["category"],
                rarity=rarity_tier,
                rarity_score=rarity_score,
                color=star_data["color"],
                tone_frequency=star_data["tone_frequency"],
                personality=star_data["personality"],
                can_chat=can_chat_flag,
                chat_duration=chat_duration,
                right_ascension=star_data["right_ascension"],
                declination=star_data["declination"],
                properties={}
            )
            db.add(star)
        db.commit()
        return True
    return False

st.set_page_config(
    page_title="Star Finder",
    page_icon="🔭",
    layout="wide"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    
    # Initialize stars if needed
    if initialize_stars(db):
        st.success("✨ Star database initialized!")
    
    if user and user.profile:
        # Get current theme
        latitude = user.profile.latitude or 40.0
        longitude = user.profile.longitude or -74.0
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
        
        st.title("🔭 Star Finder")
        st.markdown("### Discover which stars are visible from your location")
        st.markdown("---")
        
        # Location info
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📍 Your Location: {latitude:.2f}°, {longitude:.2f}°")
        with col2:
            st.info(f"🕐 Local Time: {now.strftime('%H:%M')} • {theme['time_of_day']}")
        
        st.markdown("---")
        
        # Check for star alignment
        st.subheader("🌟 Star Encounter Check")
        
        if st.button("✨ Check for Stars Above Me", type="primary", use_container_width=True):
            with st.spinner("Scanning the cosmic tapestry..."):
                # Check alignment
                aligned_star = check_star_alignment(
                    latitude, longitude, now.hour, now.month, threshold=5.0
                )
                
                if aligned_star:
                    # Get star from database
                    db_star = db.query(Star).filter(Star.name == aligned_star["name"]).first()
                    
                    if db_star:
                        # Check if already collected
                        already_collected = db.query(CollectedStar).filter(
                            CollectedStar.user_id == user.id,
                            CollectedStar.star_id == db_star.id
                        ).first()
                        
                        if not already_collected:
                            # New star encounter!
                            st.balloons()
                            
                            st.markdown(f"""
                            <div class="star-encounter">
                                <div style="text-align: center;">
                                    <h1 class="rarity-{aligned_star['rarity_tier'].lower()} chime-indicator">
                                        ✨ {aligned_star['name']} ✨
                                    </h1>
                                    <p style="font-size: 1.2em; margin: 20px 0;">
                                        A <span class="rarity-{aligned_star['rarity_tier'].lower()}">{aligned_star['rarity_tier']}</span> 
                                        {aligned_star['category']} star appears above you!
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Play chime (visual representation)
                            st.markdown(f"""
                            <div style="text-align: center; margin: 30px 0;">
                                <div class="chime-indicator" style="
                                    font-size: 3em; 
                                    color: {aligned_star['color']};
                                    text-shadow: 0 0 30px {aligned_star['color']};
                                ">
                                    🔔 {aligned_star['tone_frequency']} Hz
                                </div>
                                <p style="font-style: italic; color: {aligned_star['color']};">
                                    *A beautiful cascade of chimes resonates through the cosmos*
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Generate star message
                            message_data = generate_star_message(
                                aligned_star['name'],
                                aligned_star['category'],
                                aligned_star['personality'],
                                theme['time_of_day']
                            )
                            
                            # Display star note
                            st.markdown(f"""
                            <div class="star-note" style="background: {aligned_star['color']}30; border-color: {aligned_star['color']};">
                                <h3 style="color: {aligned_star['color']};">📜 Starshine Note</h3>
                                <p style="font-size: 1.1em; line-height: 1.6;">{message_data['content']}</p>
                                <p style="text-align: right; font-style: italic; margin-top: 20px;">
                                    {message_data['signature']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Save the collected star
                            collected_star = CollectedStar(
                                user_id=user.id,
                                star_id=db_star.id,
                                encounter_location_lat=latitude,
                                encounter_location_lon=longitude
                            )
                            db.add(collected_star)
                            
                            # Save the star note
                            star_note = StarNote(
                                user_id=user.id,
                                star_id=db_star.id,
                                content=message_data['content'],
                                note_type=message_data['note_type'],
                                color=aligned_star['color']
                            )
                            db.add(star_note)
                            
                            # Save interaction
                            interaction = StarInteraction(
                                user_id=user.id,
                                star_id=db_star.id,
                                interaction_type="encounter",
                                metadata={
                                    "location_lat": latitude,
                                    "location_lon": longitude,
                                    "time_of_day": theme['time_of_day'],
                                    "season": theme['season']
                                }
                            )
                            db.add(interaction)
                            db.commit()
                            
                            st.success(f"🎉 You collected {aligned_star['name']}! Check your Star Collection.")
                            
                            # Check if star can chat
                            if aligned_star.get('can_chat'):
                                st.markdown("---")
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, {aligned_star['color']}60, {aligned_star['color']}30);
                                    padding: 20px;
                                    border-radius: 15px;
                                    border: 2px solid {aligned_star['color']};
                                    animation: starGlow 2s ease-in-out infinite;
                                ">
                                    <h3 style="text-align: center; color: {aligned_star['color']};">
                                        💬 {aligned_star['name']} wants to chat!
                                    </h3>
                                    <p style="text-align: center; font-size: 1.1em;">
                                        This rare star will hang around for {aligned_star['chat_duration']} seconds.
                                    </p>
                                    <p style="text-align: center; font-style: italic;">
                                        {aligned_star['personality']}
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Simple chat interface
                                user_message = st.text_input(f"Send a message to {aligned_star['name']}:", key="star_chat")
                                if user_message:
                                    st.markdown(f"**You:** {user_message}")
                                    
                                    # Generate a simple response based on star personality
                                    responses = [
                                        f"✨ The cosmos hears you, dear one. {aligned_star['personality']}",
                                        f"🌟 Your words ripple through stardust. I sense your intention.",
                                        f"💫 How beautiful that our paths cross in this vast universe!",
                                        f"⭐ Your energy resonates with mine. Keep reaching for the stars!"
                                    ]
                                    st.markdown(f"**{aligned_star['name']}:** {random.choice(responses)}")
                        else:
                            st.info(f"🌟 {aligned_star['name']} is above you, but you've already collected this star! Check your collection to see it again.")
                    else:
                        st.error("Star data not found in database.")
                else:
                    st.warning("🌌 No stars are directly above you right now. The cosmos is vast - try again later or at a different location!")
                    st.info("💡 Tip: Stars are more likely to appear at night, especially rare ones!")
        
        st.markdown("---")
        
        # Show visible stars
        st.subheader("🌠 Currently Visible Stars")
        
        visible_stars = get_visible_stars(latitude, longitude, now.hour, now.month)
        
        if visible_stars:
            st.info(f"There are {len(visible_stars)} stars visible from your location right now!")
            
            # Group by rarity
            cols = st.columns(3)
            for idx, star_info in enumerate(visible_stars[:9]):  # Show first 9
                with cols[idx % 3]:
                    rarity_class = f"rarity-{star_info['rarity_tier'].lower()}"
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {star_info['color']}40, {star_info['color']}20);
                        padding: 15px;
                        border-radius: 10px;
                        border: 1px solid {star_info['color']};
                        margin: 10px 0;
                    ">
                        <h4 class="{rarity_class} star-twinkle">{star_info['name']}</h4>
                        <p><strong>Category:</strong> {star_info['category']}</p>
                        <p><strong>Rarity:</strong> <span class="{rarity_class}">{star_info['rarity_tier']}</span></p>
                        <p style="font-size: 0.85em; font-style: italic;">{star_info['personality'][:60]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No stars are currently visible from your location. The cosmic dance continues - check back soon!")
        
    else:
        st.warning("⚠️ Please update your location in your profile to use Star Finder!")
        st.markdown("""
        To find stars, we need to know where you are. Please:
        1. Go to your Profile page
        2. Add your latitude and longitude
        3. Return here to start your star collection journey!
        """)
        
        if st.button("Go to Profile"):
            st.switch_page("pages/2_Profile.py")
    
    db.close()
