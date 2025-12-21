# ======================================
# 🌌 INTERPLANETARY PEN PAL APP (MVP)
# ======================================

import streamlit as st
from styles import get_cosmic_css, get_starfield_html
from connection_features import (
    get_daily_reflection, 
    get_soul_question, 
    get_cosmic_quote,
    get_current_moon_phase,
    get_element_of_day,
    ELEMENTAL_ENERGIES
)

st.set_page_config(
    page_title="Home",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
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

    # Daily Cosmic Inspiration
    col1, col2 = st.columns(2)
    
    with col1:
        moon_phase, moon_meaning = get_current_moon_phase()
        st.markdown(f"""
        <div class="cosmic-card">
            <h4>🌙 Today's Moon Phase</h4>
            <p><strong>{moon_phase}</strong></p>
            <p style="font-size: 0.9em;">{moon_meaning}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        element = get_element_of_day()
        element_info = ELEMENTAL_ENERGIES[element]
        st.markdown(f"""
        <div class="cosmic-card">
            <h4>✨ Today's Element</h4>
            <p><strong>{element}</strong></p>
            <p style="font-size: 0.9em;">{element_info['quality']}</p>
            <p style="font-size: 0.85em; font-style: italic;">{element_info['message']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Daily Reflection
    st.markdown("### 🌟 Today's Reflection")
    reflection = get_daily_reflection()
    st.markdown(f"""
    <div class="cosmic-quote">
        {reflection}
    </div>
    """, unsafe_allow_html=True)
    
    # Soul Question
    with st.expander("💫 Open a Soul Question"):
        soul_q = get_soul_question()
        st.markdown(f"**{soul_q}**")
        st.text_area("Your reflection (for your eyes only):", key="soul_reflection", height=100)
        if st.button("🌠 Keep this with me"):
            st.success("✨ Reflection saved to your inner cosmos")
    
    # Cosmic Quote
    quote, author = get_cosmic_quote()
    st.markdown(f"""
    <div class="cosmic-quote">
        "{quote}"<br/>
        <em>— {author}</em>
    </div>
    """, unsafe_allow_html=True)

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
