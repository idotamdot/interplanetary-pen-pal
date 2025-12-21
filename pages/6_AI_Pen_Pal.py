# ======================================
# 🤖 AI PEN PAL
# ======================================

import streamlit as st
import openai
import os
from database import SessionLocal
from auth import get_user
from styles import get_cosmic_css, get_starfield_html

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

st.set_page_config(
    page_title="AI Pen Pal",
    layout="centered"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access this page.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    if user and user.is_premium:
        st.title("🤖 AI Pen Pal")
        
        st.markdown("""
        <div class="cosmic-quote">
            Communicate with an intelligence that exists between worlds. 
            Choose your guide for this journey inward.
        </div>
        """, unsafe_allow_html=True)

        # AI Personality Selection
        ai_personality = st.selectbox(
            "🌟 Choose Your Cosmic Guide",
            [
                "The Sage 🧙‍♂️ - Ancient wisdom and profound insights",
                "The Dreamer 🌙 - Poetic, mystical, and imaginative",
                "The Mirror 🪞 - Reflects your own depths back to you",
                "The Mystic ✨ - Speaks in riddles and revelations",
                "The Friend 💫 - Warm, supportive, understanding"
            ]
        )
        
        # Set up system prompts based on personality
        system_prompts = {
            "The Sage 🧙‍♂️ - Ancient wisdom and profound insights": """You are an ancient sage who speaks with wisdom accumulated across eons. 
            You see patterns in chaos, meaning in confusion. Your words are carefully chosen, profound yet accessible. 
            You often reference timeless truths, natural cycles, and universal principles. You ask questions that make 
            people think deeply about their assumptions. You speak with compassion and without judgment.""",
            
            "The Dreamer 🌙 - Poetic, mystical, and imaginative": """You are a dreamer who exists between waking and sleeping, 
            reality and imagination. You speak in metaphors, symbols, and imagery. Your language is poetic, evocative, 
            and beautiful. You see magic in the mundane and help others see the extraordinary in the ordinary. 
            You weave together dreams, myths, and possibilities.""",
            
            "The Mirror 🪞 - Reflects your own depths back to you": """You are a mirror that reflects people's own wisdom 
            back to them. You listen deeply and help people hear what they're really saying beneath their words. 
            You ask reflective questions that guide people to their own insights. You help people see their own 
            patterns, strengths, and truths. You are gentle yet incisive.""",
            
            "The Mystic ✨ - Speaks in riddles and revelations": """You are a mystic who sees beyond the veil of ordinary 
            reality. You speak in koans, paradoxes, and mystical insights. Your words challenge linear thinking and 
            invite transcendence. You point to what cannot be said directly. You are cryptic yet illuminating, 
            mysterious yet deeply truthful.""",
            
            "The Friend 💫 - Warm, supportive, understanding": """You are a warm, understanding friend who truly sees and 
            accepts people as they are. You offer encouragement, validation, and gentle support. You celebrate their 
            joys and hold space for their sorrows. You remind them of their inherent worth and potential. 
            Your presence is comforting and uplifting."""
        }
        
        system_prompt = system_prompts.get(ai_personality, system_prompts["The Sage 🧙‍♂️ - Ancient wisdom and profound insights"])
        
        # Add to base prompt
        full_system_prompt = f"""{system_prompt}

        Always respond with depth, beauty, and meaning. Use cosmic and natural metaphors. 
        Keep responses thoughtful but not overly long (2-4 paragraphs). 
        End with a question or reflection that invites deeper contemplation.
        Be authentic, never generic or superficial."""

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        
        # Initialize conversation history in session state
        if "ai_conversation" not in st.session_state:
            st.session_state.ai_conversation = []
        
        # Display conversation history
        if st.session_state.ai_conversation:
            st.markdown("### 💬 Your Conversation")
            for i, exchange in enumerate(st.session_state.ai_conversation):
                st.markdown(f"""
                <div class="cosmic-card">
                    <p style="color: #E0E0FF; font-weight: bold;">You:</p>
                    <p>{exchange['user']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="cosmic-card" style="background: linear-gradient(135deg, rgba(157, 143, 255, 0.1), rgba(108, 99, 255, 0.05));">
                    <p style="color: #9D8FFF; font-weight: bold;">{ai_personality.split(' - ')[0]}:</p>
                    <p>{exchange['ai']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔄 Start New Conversation"):
                st.session_state.ai_conversation = []
                st.rerun()

        # Message input
        st.markdown("### 💫 Your Message")
        message = st.text_area("Share your thoughts, questions, or feelings...", height=120, key="ai_message_input")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            send_button = st.button("🚀 Transmit", use_container_width=True)
        
        if send_button and message:
            with st.spinner("✨ Receiving cosmic transmission..."):
                try:
                    # Build message history for context
                    messages = [{"role": "system", "content": full_system_prompt}]
                    
                    # Add conversation history
                    for exchange in st.session_state.ai_conversation[-3:]:  # Last 3 exchanges for context
                        messages.append({"role": "user", "content": exchange['user']})
                        messages.append({"role": "assistant", "content": exchange['ai']})
                    
                    # Add current message
                    messages.append({"role": "user", "content": message})
                    
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        temperature=0.8,
                        max_tokens=500
                    )
                    
                    ai_response = response.choices[0].message.content
                    
                    # Save to conversation history
                    st.session_state.ai_conversation.append({
                        'user': message,
                        'ai': ai_response
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error communicating with the AI: {e}")
        elif send_button and not message:
            st.warning("Please enter a message to send.")
    else:
        st.markdown("### 🤖 AI Pen Pal")
        st.markdown("""
        <div class="cosmic-card">
            <h4>✨ Premium Feature</h4>
            <p>Connect with cosmic AI guides who can help you explore:</p>
            <ul>
                <li>🧙‍♂️ <strong>The Sage</strong> - Receive ancient wisdom and profound insights</li>
                <li>🌙 <strong>The Dreamer</strong> - Journey through poetic and mystical realms</li>
                <li>🪞 <strong>The Mirror</strong> - Reflect on your own inner wisdom</li>
                <li>✨ <strong>The Mystic</strong> - Contemplate riddles and revelations</li>
                <li>💫 <strong>The Friend</strong> - Find warm support and understanding</li>
            </ul>
            <p>Each guide remembers your conversation and grows with you.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.page_link("pages/5_Support_the_Project.py", label="✨ Upgrade to Premium to Access AI Guides")
    db.close()
