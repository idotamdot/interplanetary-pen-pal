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

        st.markdown("### ✨ Basic Information")
        if profile:
            dream = st.text_area(
                "Share a Dream, Memory, or Origin Story", 
                value=profile.dream,
                height=150,
                help="This is your space to express what makes you... you."
            )
        else:
            name = st.text_input("Your Star Name")
            symbol = st.text_input("Your Symbolic Signature (emoji, glyph, constellation)")
            dream = st.text_area("Share a Dream, Memory, or Origin Story")
        
        st.markdown("---")
        st.markdown("### 📍 Location (for Star Collection)")
        st.info("💡 Your location helps us determine which stars are visible from where you are!")
        
        col1, col2 = st.columns(2)
        with col1:
            if profile and profile.latitude:
                latitude = st.number_input("Latitude", value=float(profile.latitude), min_value=-90.0, max_value=90.0, format="%.6f")
            else:
                latitude = st.number_input("Latitude", value=40.7128, min_value=-90.0, max_value=90.0, format="%.6f", help="Example: New York is 40.7128")
        
        with col2:
            if profile and profile.longitude:
                longitude = st.number_input("Longitude", value=float(profile.longitude), min_value=-180.0, max_value=180.0, format="%.6f")
            else:
                longitude = st.number_input("Longitude", value=-74.0060, min_value=-180.0, max_value=180.0, format="%.6f", help="Example: New York is -74.0060")
        
        if profile and profile.timezone:
            timezone = st.text_input("Timezone (optional)", value=profile.timezone, help="Example: America/New_York")
        else:
            timezone = st.text_input("Timezone (optional)", value="UTC", help="Example: America/New_York")
        
        st.caption("🔍 You can find your coordinates at [latlong.net](https://www.latlong.net/)")

        if st.button("Save Profile", type="primary"):
            if profile:
                profile.star_name = name
                profile.symbol = constellation
                profile.dream = dream
                profile.latitude = latitude
                profile.longitude = longitude
                profile.timezone = timezone
            else:
                profile = Profile(
                    user_id=user.id, 
                    star_name=name, 
                    symbol=symbol, 
                    dream=dream,
                    latitude=latitude,
                    longitude=longitude,
                    timezone=timezone
                )
                db.add(profile)

            db.commit()
            db.refresh(profile)

            st.success("🛸 Profile Registered for Interplanetary Exchange")
            st.markdown(f"🌌 **{name}** — {symbol}")
            st.markdown(f"🧬 *\"{dream}\"*")
            st.markdown(f"📍 Location: {latitude:.2f}°, {longitude:.2f}°")
            
            st.markdown("---")
            st.success("✨ You're ready to collect stars! Visit the Star Finder to begin your journey.")
    else:
        st.error("Could not find user. Please log in again.")

    db.close()
