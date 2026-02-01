# ======================================
# 🔮 PERSPECTIVE BRIDGE
# Multi-Agent Discussion & Perspective Shifting
# ======================================

import streamlit as st
import random
from datetime import datetime
from database import SessionLocal, Profile, DiplomaticProgress, DiplomaticExercise
from auth import get_user
from styles import get_cosmic_css, get_starfield_html
from ai_agents import (
    get_age_profile,
    generate_council_discussion,
    generate_perspective_meditation,
    generate_empathy_bridge,
    COUNCIL_MEMBERS,
    PERSPECTIVE_SHIFT_PROMPTS,
    get_agent_mood_intro,
    get_surprise_wisdom,
    check_easter_egg,
    AGE_RANGES,
    AGENT_MOODS
)
import openai
import os

def get_current_user(db):
    if "username" in st.session_state:
        return get_user(db, st.session_state["username"])
    return None

def get_or_create_progress(db, user_id):
    """Get or create diplomatic progress record for user."""
    progress = db.query(DiplomaticProgress).filter(DiplomaticProgress.user_id == user_id).first()
    if not progress:
        progress = DiplomaticProgress(user_id=user_id, achievements=[])
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress

def generate_agent_debate(topic: str, age_profile: dict, rounds: int = 2) -> list:
    """Generate a multi-round debate between council members."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    # Select 3 debaters
    debaters = random.sample(list(COUNCIL_MEMBERS.keys()), 3)
    debate = []
    
    for round_num in range(rounds):
        for debater_key in debaters:
            member = COUNCIL_MEMBERS[debater_key]
            
            # Build context from previous statements
            context = ""
            if debate:
                context = "\n\nPrevious statements:\n" + "\n".join([
                    f"{d['member']['name']}: {d['statement'][:200]}..."
                    for d in debate[-3:]
                ])
            
            system_prompt = f"""You are {member['name']}, participating in a friendly cosmic debate.

Archetype: {member['archetype']}
Core Value: {member['core_value']}
Speaking Style: {member['speaking_style']}
Perspective Approach: {member['perspective_approach']}

The listener is {age_profile['label']} (age {age_profile['user_age']}).
{age_profile['content_guidelines']}

DEBATE RULES:
- Respectfully engage with other viewpoints
- Stay true to your unique perspective
- Build on or thoughtfully disagree with previous points
- Keep responses brief ({age_profile['max_response_length']} words max)
- Model healthy disagreement - be curious, not combative
- Use your signature speaking style
- End with a thought-provoking insight or question

This is round {round_num + 1} of the debate."""

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"The topic: {topic}{context}"}
                    ],
                    temperature=0.9,
                    max_tokens=age_profile['max_response_length'] + 50
                )
                
                debate.append({
                    "member": member,
                    "statement": response.choices[0].message.content,
                    "round": round_num + 1
                })
            except Exception as e:
                debate.append({
                    "member": member,
                    "statement": f"*{member['name']} pauses to gather thoughts...*",
                    "round": round_num + 1
                })
    
    return debate

def generate_debate_synthesis(topic: str, debate: list, age_profile: dict) -> str:
    """Generate a synthesis/summary of the debate that highlights key insights."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    debate_summary = "\n\n".join([
        f"{d['member']['name']}: {d['statement']}"
        for d in debate
    ])
    
    system_prompt = f"""You are the Cosmic Synthesizer, helping to integrate multiple perspectives.

The listener is {age_profile['label']} (age {age_profile['user_age']}).
{age_profile['content_guidelines']}

Your task: Create a beautiful synthesis of the debate that:
1. Highlights where different perspectives overlapped
2. Notes where they productively disagreed
3. Identifies the core insights from each viewpoint
4. Offers wisdom about how different perspectives enrich understanding
5. Asks a reflective question for the listener to consider

Be warm, insightful, and {age_profile['tone']}.
Keep your response under {age_profile['max_response_length'] + 100} words."""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {topic}\n\nDebate:\n{debate_summary}"}
            ],
            temperature=0.8,
            max_tokens=age_profile['max_response_length'] + 150
        )
        return response.choices[0].message.content
    except Exception as e:
        return "The cosmic synthesis is still forming... Please try again! ✨"

st.set_page_config(
    page_title="Perspective Bridge",
    page_icon="🔮",
    layout="wide"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

# Custom CSS for the perspective bridge
st.markdown("""
<style>
.perspective-header {
    background: linear-gradient(135deg, rgba(0, 206, 209, 0.3), rgba(75, 0, 130, 0.3));
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 2px solid rgba(0, 206, 209, 0.5);
}

.debate-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    border-left: 4px solid;
    position: relative;
}

.debate-card::before {
    content: attr(data-round);
    position: absolute;
    top: -10px;
    right: 15px;
    background: rgba(100, 149, 237, 0.8);
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 0.75em;
}

.synthesis-card {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1));
    padding: 25px;
    border-radius: 15px;
    border: 2px solid rgba(255, 215, 0, 0.4);
    margin: 20px 0;
}

.meditation-card {
    background: linear-gradient(135deg, rgba(230, 230, 250, 0.2), rgba(147, 112, 219, 0.2));
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(147, 112, 219, 0.4);
    margin: 20px 0;
}

.perspective-prompt {
    background: rgba(100, 149, 237, 0.15);
    padding: 15px 20px;
    border-radius: 10px;
    font-style: italic;
    margin: 15px 0;
    border-left: 3px solid #6495ED;
}

.mood-indicator {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.85em;
    margin: 5px;
    background: rgba(255, 255, 255, 0.1);
}

.interactive-prompt {
    background: linear-gradient(135deg, rgba(144, 238, 144, 0.2), rgba(60, 179, 113, 0.2));
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid rgba(60, 179, 113, 0.4);
}

.surprise-reveal {
    animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access the Perspective Bridge.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    
    if user:
        # Get user's age from profile or session state
        user_age = None
        if user.profile and hasattr(user.profile, 'age') and user.profile.age:
            user_age = user.profile.age
        
        if "diplomatic_age" in st.session_state:
            user_age = st.session_state.diplomatic_age
        
        # If no age, redirect to set it
        if not user_age:
            st.markdown("""
            <div class="perspective-header">
                <h1>🔮 Perspective Bridge</h1>
                <p>Before we can personalize your experience, please visit the Diplomatic Academy first!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎓 Go to Diplomatic Academy"):
                st.switch_page("pages/10_Diplomatic_Academy.py")
            
            db.close()
            st.stop()
        
        # Get age profile
        age_profile = get_age_profile(user_age)
        progress = get_or_create_progress(db, user.id)
        
        # Header
        st.markdown(f"""
        <div class="perspective-header">
            <h1>🔮 Perspective Bridge</h1>
            <p style="font-size: 1.2em;">Watch AI minds explore ideas together • Learn to see from every angle</p>
            <p>{age_profile['label']} Mode Active ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show surprise wisdom occasionally
        wisdom = get_surprise_wisdom()
        if wisdom:
            st.markdown(f"""
            <div class="wisdom-bomb surprise-reveal">
                {wisdom}
            </div>
            """, unsafe_allow_html=True)
        
        # Main Activity Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎭 Watch Agents Discuss",
            "🧘 Perspective Meditation",
            "🎲 Random Perspective Shift",
            "🌟 Surprise Me!"
        ])
        
        # TAB 1: Watch Agents Discuss
        with tab1:
            st.markdown("### 🎭 Watch the Cosmic Council Debate")
            st.markdown("""
            Give any topic to the Council and watch them explore it from their unique perspectives!
            See how they respectfully disagree, build on each other's ideas, and model healthy discourse.
            """)
            
            # Topic input
            debate_topic = st.text_area(
                "What topic would you like the Council to discuss?",
                height=100,
                placeholder="Enter any topic, question, or dilemma you'd like to see from multiple angles...",
                key="debate_topic"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                num_rounds = st.slider("Number of debate rounds:", 1, 3, 2)
            with col2:
                st.info(f"Each round lets agents respond to each other!")
            
            if st.button("🎬 Start the Discussion!", type="primary", key="start_debate"):
                if debate_topic:
                    # Check easter eggs
                    easter_egg = check_easter_egg(debate_topic)
                    if easter_egg:
                        st.info(easter_egg)
                    
                    with st.spinner("The Council is gathering and preparing their thoughts..."):
                        debate = generate_agent_debate(debate_topic, age_profile, num_rounds)
                        
                        st.markdown("### 🌟 The Discussion Unfolds...")
                        
                        current_round = 0
                        for entry in debate:
                            if entry['round'] != current_round:
                                current_round = entry['round']
                                st.markdown(f"---\n**Round {current_round}**")
                            
                            member = entry['member']
                            st.markdown(f"""
                            <div class="debate-card" style="border-color: {member['color']};" data-round="Round {entry['round']}">
                                <h4 style="color: {member['color']};">
                                    {member['emoji']} {member['name']}
                                </h4>
                                <p style="font-size: 0.85em; opacity: 0.8;">{member['archetype']} • Core Value: {member['core_value']}</p>
                                <p style="margin-top: 15px;">{entry['statement']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Generate synthesis
                        st.markdown("---")
                        st.markdown("### ✨ Cosmic Synthesis")
                        
                        with st.spinner("Weaving the perspectives together..."):
                            synthesis = generate_debate_synthesis(debate_topic, debate, age_profile)
                            
                            st.markdown(f"""
                            <div class="synthesis-card">
                                <h4>🌈 The Bigger Picture</h4>
                                <p>{synthesis}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Update progress
                        progress.council_consults = (progress.council_consults or 0) + 1
                        progress.perspectives_understood = (progress.perspectives_understood or 0) + len(debate)
                        progress.total_exercises = (progress.total_exercises or 0) + 1
                        progress.updated_at = datetime.utcnow()
                        db.commit()
                        
                        st.success("✨ Discussion complete! You've witnessed the power of multiple perspectives!")
                else:
                    st.warning("Please enter a topic for discussion!")
        
        # TAB 2: Perspective Meditation
        with tab2:
            st.markdown("### 🧘 Guided Perspective Meditation")
            st.markdown("""
            Sometimes the best way to see from another's perspective is to quiet our mind and imagine.
            This guided meditation will help you step into someone else's shoes.
            """)
            
            meditation_situation = st.text_area(
                "Describe a situation where you'd like to understand another perspective:",
                height=100,
                placeholder="A disagreement with someone, a confusing situation, or any time you want to understand another viewpoint...",
                key="meditation_situation"
            )
            
            if st.button("🧘 Begin Meditation", type="primary", key="start_meditation"):
                if meditation_situation:
                    with st.spinner("Preparing your guided meditation..."):
                        meditation_result = generate_perspective_meditation(
                            meditation_situation,
                            age_profile
                        )
                        
                        st.markdown(f"""
                        <div class="meditation-card">
                            <h4>🌸 Guided Perspective Meditation</h4>
                            <p style="white-space: pre-wrap;">{meditation_result['meditation']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="perspective-prompt">
                            <strong>💭 Reflection Prompt:</strong><br/>
                            {meditation_result['reflection_prompt']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Optional journaling
                        st.markdown("### ✍️ Journal Your Insights (Optional)")
                        journal_entry = st.text_area(
                            "What did you discover during this meditation?",
                            height=100,
                            placeholder="Any insights, realizations, or new understandings...",
                            key="meditation_journal"
                        )
                        
                        if journal_entry:
                            st.success("✨ Your reflection has been noted. Growth happens one insight at a time!")
                        
                        # Update progress
                        progress.perspective_exercises = (progress.perspective_exercises or 0) + 1
                        progress.total_exercises = (progress.total_exercises or 0) + 1
                        progress.updated_at = datetime.utcnow()
                        db.commit()
                else:
                    st.warning("Please describe a situation for the meditation!")
        
        # TAB 3: Random Perspective Shift
        with tab3:
            st.markdown("### 🎲 Random Perspective Shift Challenge")
            st.markdown("""
            Get a random perspective-shifting prompt to challenge your thinking!
            These prompts help you practice seeing things differently.
            """)
            
            if "current_prompt" not in st.session_state:
                st.session_state.current_prompt = random.choice(PERSPECTIVE_SHIFT_PROMPTS)
            
            st.markdown(f"""
            <div class="perspective-prompt" style="font-size: 1.2em; padding: 25px;">
                <strong>Your Challenge:</strong><br/><br/>
                {st.session_state.current_prompt}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎲 New Prompt", key="new_prompt"):
                    st.session_state.current_prompt = random.choice(PERSPECTIVE_SHIFT_PROMPTS)
                    st.rerun()
            
            with col2:
                if st.button("💡 Get a Hint", key="prompt_hint"):
                    # Generate a hint based on age profile
                    hints = {
                        "young_explorer": "Think about a time when someone surprised you by being nice! What did they see that you didn't? 🌈",
                        "teen_navigator": "Consider: what would your best friend say if they were watching this situation from outside? 🤔",
                        "adult_voyager": "Sometimes our 'opponents' are just people trying to protect something they value. What might that be? 💭",
                        "elder_sage": "Over a lifetime, you've probably been on both sides of many conflicts. What patterns do you see? 🌟"
                    }
                    st.info(hints.get(age_profile['key'], hints['adult_voyager']))
            
            # Journal response
            prompt_response = st.text_area(
                "Your thoughts on this prompt:",
                height=120,
                placeholder="Take your time to really consider the prompt...",
                key="prompt_response"
            )
            
            if prompt_response and st.button("💫 Submit Reflection", key="submit_reflection"):
                st.success("✨ Beautiful reflection! Every time you consider a new perspective, you grow a little wiser.")
                
                # Update progress
                progress.perspective_exercises = (progress.perspective_exercises or 0) + 1
                progress.total_exercises = (progress.total_exercises or 0) + 1
                progress.updated_at = datetime.utcnow()
                db.commit()
                
                # Get a new prompt for next time
                st.session_state.current_prompt = random.choice(PERSPECTIVE_SHIFT_PROMPTS)
        
        # TAB 4: Surprise Me!
        with tab4:
            st.markdown("### 🌟 Surprise Features!")
            st.markdown("""
            Here are some fun, unexpected ways to explore perspectives and see what AI can do!
            """)
            
            st.markdown("---")
            
            # Feature 1: Mood of the Day
            st.markdown("#### 🎭 What Mood Are the Agents In Today?")
            
            if st.button("🔮 Check Agent Moods", key="check_moods"):
                st.markdown("**Today's Cosmic Mood Report:**")
                
                mood_cols = st.columns(5)
                for i, (member_key, member) in enumerate(COUNCIL_MEMBERS.items()):
                    mood_key = random.choice(list(AGENT_MOODS.keys()))
                    mood = AGENT_MOODS[mood_key]
                    
                    with mood_cols[i]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px;">
                            <div style="font-size: 2em;">{member['emoji']}</div>
                            <p style="font-weight: bold; color: {member['color']};">{member['name']}</p>
                            <div class="mood-indicator">{mood['emoji']} {mood_key.title()}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Feature 2: Perspective Roulette
            st.markdown("#### 🎰 Perspective Roulette")
            st.markdown("Get a random situation AND a random council member to analyze it!")
            
            random_situations = [
                "Someone cut in line at the store",
                "A friend hasn't responded to your messages for days",
                "Your neighbor plays loud music",
                "Someone gave you unsolicited advice",
                "A colleague got credit for a team effort",
                "Someone disagrees with you online",
                "A family member keeps asking personal questions",
                "Your plans got cancelled at the last minute"
            ]
            
            if st.button("🎰 Spin the Roulette!", key="spin_roulette"):
                situation = random.choice(random_situations)
                member_key = random.choice(list(COUNCIL_MEMBERS.keys()))
                member = COUNCIL_MEMBERS[member_key]
                
                st.markdown(f"""
                <div class="interactive-prompt surprise-reveal">
                    <h4>🎲 Your Random Scenario:</h4>
                    <p style="font-size: 1.1em; margin: 15px 0;">"{situation}"</p>
                    
                    <h4>🎯 Analyzed by:</h4>
                    <p style="color: {member['color']}; font-size: 1.2em;">
                        {member['emoji']} {member['name']} - {member['archetype']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate their perspective
                with st.spinner(f"{member['name']} is considering this..."):
                    discussions = generate_council_discussion(situation, age_profile, 1)
                    if discussions:
                        response = discussions[0]['response']
                        st.markdown(f"""
                        <div class="debate-card" style="border-color: {member['color']};">
                            <h4 style="color: {member['color']};">
                                {member['emoji']} {member['name']}'s Perspective:
                            </h4>
                            <p style="margin-top: 15px;">{response}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Feature 3: Quick Council Question
            st.markdown("#### 💬 Quick Question to a Random Council Member")
            
            quick_question = st.text_input(
                "Ask anything:",
                placeholder="What's on your mind?",
                key="quick_question"
            )
            
            if quick_question and st.button("✨ Ask!", key="ask_quick"):
                member_key = random.choice(list(COUNCIL_MEMBERS.keys()))
                member = COUNCIL_MEMBERS[member_key]
                
                # Check easter egg
                easter_egg = check_easter_egg(quick_question)
                if easter_egg:
                    st.info(easter_egg)
                
                with st.spinner(f"{member['name']} is answering..."):
                    discussions = generate_council_discussion(quick_question, age_profile, 1)
                    if discussions:
                        response = discussions[0]['response']
                        mood_intro = get_agent_mood_intro()
                        
                        st.markdown(f"""
                        <div class="debate-card surprise-reveal" style="border-color: {member['color']};">
                            <h4 style="color: {member['color']};">
                                {member['emoji']} {member['name']} responds:
                            </h4>
                            <p><em>{mood_intro}</em></p>
                            <p style="margin-top: 15px;">{response}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Feature 4: Wisdom Treasure Chest
            st.markdown("#### 🎁 Open a Wisdom Treasure Chest")
            
            if st.button("🎁 Open Chest!", key="open_chest"):
                from ai_agents import COSMIC_WISDOM_BOMBS
                wisdom = random.choice(COSMIC_WISDOM_BOMBS)
                
                st.markdown(f"""
                <div class="synthesis-card surprise-reveal">
                    <h4>✨ You Found Cosmic Wisdom!</h4>
                    <p style="font-size: 1.2em; margin-top: 15px;">{wisdom}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
        
    else:
        st.error("Could not find user. Please log in again.")
    
    db.close()
