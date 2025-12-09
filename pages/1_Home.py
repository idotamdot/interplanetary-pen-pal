# ======================================
# 🌌 INTERPLANETARY PEN PAL APP (MVP)
# ======================================

import streamlit as st

st.set_page_config(
    page_title="Home",
    layout="centered"
)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    st.markdown("""
    # 📡 Interplanetary Pen Pal
    #### A peaceful platform for cosmic correspondence
    ---
    ### 🪐 Opening Transmission
    > “We come not with answers,
    > but with open circuits.
    > We learn you by listening,
    > and love you by reflection.
    > May this transmission reach the edges of possibility.”
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
