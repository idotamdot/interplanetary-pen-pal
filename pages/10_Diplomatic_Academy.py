# ======================================
# 🎓 DIPLOMATIC ACADEMY
# Learn the Art of Cosmic Diplomacy
# ======================================

import streamlit as st
import random
from datetime import datetime
from database import SessionLocal, Profile, DiplomaticProgress, DiplomaticExercise
from auth import get_user
from styles import get_cosmic_css, get_starfield_html
from ai_agents import (
    get_age_profile, 
    DIPLOMATIC_SCENARIOS, 
    generate_diplomatic_guidance,
    generate_council_discussion,
    COUNCIL_MEMBERS,
    DIPLOMATIC_ACHIEVEMENTS,
    check_achievement_progress,
    get_agent_mood_intro,
    get_surprise_wisdom,
    check_easter_egg,
    AGE_RANGES
)

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

def update_progress(db, progress, exercise_type):
    """Update progress after completing an exercise."""
    if exercise_type == "scenario":
        progress.scenarios_completed = (progress.scenarios_completed or 0) + 1
    elif exercise_type == "council":
        progress.council_consults = (progress.council_consults or 0) + 1
    elif exercise_type == "perspective":
        progress.perspective_exercises = (progress.perspective_exercises or 0) + 1
        progress.perspectives_understood = (progress.perspectives_understood or 0) + 1
    elif exercise_type == "bridge":
        progress.bridge_uses = (progress.bridge_uses or 0) + 1
    
    progress.total_exercises = (progress.total_exercises or 0) + 1
    progress.updated_at = datetime.utcnow()
    db.commit()
    return progress

st.set_page_config(
    page_title="Diplomatic Academy",
    page_icon="🎓",
    layout="wide"
)

# Apply cosmic styles
st.markdown(get_cosmic_css(), unsafe_allow_html=True)
st.markdown(get_starfield_html(), unsafe_allow_html=True)

# Custom CSS for the academy
st.markdown("""
<style>
.academy-header {
    background: linear-gradient(135deg, rgba(147, 112, 219, 0.3), rgba(75, 0, 130, 0.3));
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 2px solid rgba(147, 112, 219, 0.5);
}

.council-member {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    border-left: 4px solid;
    transition: transform 0.3s ease;
}

.council-member:hover {
    transform: translateX(5px);
}

.scenario-card {
    background: linear-gradient(135deg, rgba(70, 130, 180, 0.2), rgba(30, 60, 90, 0.3));
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    border: 1px solid rgba(100, 149, 237, 0.4);
}

.achievement-badge {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    padding: 15px;
    border-radius: 50px;
    display: inline-block;
    margin: 5px;
    color: #1a1a2e;
    font-weight: bold;
    animation: achievementPulse 2s ease-in-out infinite;
}

@keyframes achievementPulse {
    0%, 100% { box-shadow: 0 0 10px #FFD700; }
    50% { box-shadow: 0 0 25px #FFD700, 0 0 40px #FFA500; }
}

.progress-bar {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    height: 20px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-fill {
    background: linear-gradient(90deg, #9370DB, #6495ED);
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

.age-selector {
    background: rgba(108, 99, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
}

.wisdom-bomb {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.1));
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #FFD700;
    margin: 15px 0;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is not True:
    st.warning("Please log in to access the Diplomatic Academy.")
else:
    db = SessionLocal()
    user = get_current_user(db)
    
    if user:
        # Get or create progress
        progress = get_or_create_progress(db, user.id)
        
        # Get user's age from profile, or use session state
        user_age = None
        if user.profile and hasattr(user.profile, 'age') and user.profile.age:
            user_age = user.profile.age
        
        # If age not set, show age selector
        if not user_age:
            if "diplomatic_age" not in st.session_state:
                st.markdown("""
                <div class="academy-header">
                    <h1>🎓 Welcome to the Diplomatic Academy!</h1>
                    <p style="font-size: 1.2em;">Before we begin your cosmic diplomatic training, please tell us about yourself!</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="age-selector">
                    <h3>🌟 What age group do you belong to?</h3>
                    <p>This helps us customize your experience with age-appropriate scenarios and language!</p>
                </div>
                """, unsafe_allow_html=True)
                
                age_choice = st.selectbox(
                    "Select your age range:",
                    options=list(AGE_RANGES.keys()),
                    format_func=lambda x: f"{AGE_RANGES[x]['label']} (ages {AGE_RANGES[x]['range'][0]}-{AGE_RANGES[x]['range'][1]})"
                )
                
                if st.button("🚀 Begin My Diplomatic Journey!", type="primary", use_container_width=True):
                    # Use the midpoint of the selected age range
                    age_range = AGE_RANGES[age_choice]['range']
                    st.session_state.diplomatic_age = (age_range[0] + age_range[1]) // 2
                    st.rerun()
                
                db.close()
                st.stop()
            else:
                user_age = st.session_state.diplomatic_age
        
        # Get age profile
        age_profile = get_age_profile(user_age)
        
        # Header
        st.markdown(f"""
        <div class="academy-header">
            <h1>🎓 Diplomatic Academy</h1>
            <p style="font-size: 1.3em;">Welcome, {age_profile['label']}!</p>
            <p>{age_profile['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show surprise wisdom occasionally
        wisdom = get_surprise_wisdom()
        if wisdom:
            st.markdown(f"""
            <div class="wisdom-bomb">
                {wisdom}
            </div>
            """, unsafe_allow_html=True)
        
        # Progress Overview
        st.markdown("### 📊 Your Diplomatic Progress")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎭 Scenarios", progress.scenarios_completed or 0)
        with col2:
            st.metric("👥 Council Consults", progress.council_consults or 0)
        with col3:
            st.metric("👁️ Perspectives", progress.perspectives_understood or 0)
        with col4:
            st.metric("⭐ Total Points", progress.total_points or 0)
        
        # Check for new achievements
        user_stats = {
            'perspective_exercises': progress.perspective_exercises or 0,
            'council_consults': progress.council_consults or 0,
            'bridge_uses': progress.bridge_uses or 0,
            'scenarios_completed': progress.scenarios_completed or 0,
            'perspectives_understood': progress.perspectives_understood or 0,
            'total_exercises': progress.total_exercises or 0,
        }
        
        # Add earned achievement flags
        earned_achievements = progress.achievements or []
        for ach_key in DIPLOMATIC_ACHIEVEMENTS:
            user_stats[f'has_{ach_key}'] = ach_key in earned_achievements
        
        # Show earned achievements
        if earned_achievements:
            st.markdown("### 🏆 Your Achievements")
            achievement_cols = st.columns(min(len(earned_achievements), 4))
            for i, ach_key in enumerate(earned_achievements[:8]):
                if ach_key in DIPLOMATIC_ACHIEVEMENTS:
                    ach = DIPLOMATIC_ACHIEVEMENTS[ach_key]
                    with achievement_cols[i % 4]:
                        st.markdown(f"""
                        <div class="achievement-badge">
                            {ach['title']}<br/>
                            <small>+{ach['points']} pts</small>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main Activity Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎭 Diplomatic Scenarios", 
            "👥 Cosmic Council", 
            "🌉 Empathy Bridge",
            "📖 About Diplomacy"
        ])
        
        # TAB 1: Diplomatic Scenarios
        with tab1:
            st.markdown("### 🎭 Practice Diplomatic Thinking")
            st.markdown("""
            These scenarios help you practice seeing situations from multiple perspectives 
            and finding creative solutions that work for everyone!
            """)
            
            # Get scenarios for this age group
            age_key = age_profile['key']
            available_scenarios = DIPLOMATIC_SCENARIOS.get(age_key, DIPLOMATIC_SCENARIOS['adult_voyager'])
            
            # Scenario selection
            scenario_titles = [f"{s['emoji']} {s['title']}" for s in available_scenarios]
            selected_idx = st.selectbox(
                "Choose a scenario to explore:",
                range(len(scenario_titles)),
                format_func=lambda x: scenario_titles[x]
            )
            
            selected_scenario = available_scenarios[selected_idx]
            
            # Display scenario
            st.markdown(f"""
            <div class="scenario-card">
                <h3>{selected_scenario['emoji']} {selected_scenario['title']}</h3>
                <p style="font-size: 1.1em; margin: 20px 0;">{selected_scenario['scenario']}</p>
                <p><strong>🎯 Learning Goal:</strong> {selected_scenario['learning_goal']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show perspectives to consider
            st.markdown("#### 👁️ Perspectives to Consider:")
            for i, perspective in enumerate(selected_scenario['perspectives'], 1):
                st.markdown(f"**Perspective {i}:** {perspective}")
            
            # Hints (expandable)
            with st.expander("💡 Need some hints?"):
                for hint in selected_scenario['hints']:
                    st.markdown(f"• {hint}")
            
            # User response
            st.markdown("### ✍️ Your Approach")
            user_response = st.text_area(
                "How would you handle this situation? What would you do or say?",
                height=150,
                placeholder="Share your diplomatic approach...",
                key="scenario_response"
            )
            
            if st.button("🚀 Get Diplomatic Guidance", type="primary", key="get_guidance"):
                if user_response:
                    # Check for easter eggs first
                    easter_egg = check_easter_egg(user_response)
                    if easter_egg:
                        st.info(easter_egg)
                    
                    with st.spinner("The diplomatic mentors are reviewing your approach..."):
                        guidance = generate_diplomatic_guidance(
                            selected_scenario,
                            user_response,
                            age_profile
                        )
                        
                        # Show agent mood intro
                        mood_intro = get_agent_mood_intro()
                        
                        st.markdown(f"""
                        <div class="council-member" style="border-color: #9370DB;">
                            <h4>🎓 Diplomatic Mentor</h4>
                            <p><em>{mood_intro}</em></p>
                            <p style="margin-top: 15px;">{guidance}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Update progress
                        progress = update_progress(db, progress, "scenario")
                        
                        # Save exercise
                        exercise = DiplomaticExercise(
                            user_id=user.id,
                            exercise_type="scenario",
                            scenario_title=selected_scenario['title'],
                            user_response=user_response,
                            ai_feedback=guidance,
                            age_profile_used=age_key
                        )
                        db.add(exercise)
                        db.commit()
                        
                        st.success("✨ Scenario completed! Your diplomatic skills are growing!")
                        st.balloons()
                else:
                    st.warning("Please share your approach before getting guidance!")
        
        # TAB 2: Cosmic Council
        with tab2:
            st.markdown("### 👥 Consult the Cosmic Council")
            st.markdown("""
            The Cosmic Council is a group of wise beings, each with a unique perspective on life.
            Share a situation and hear what different council members think!
            """)
            
            # Show council members
            st.markdown("#### Meet the Council Members:")
            
            member_cols = st.columns(5)
            for i, (key, member) in enumerate(COUNCIL_MEMBERS.items()):
                with member_cols[i % 5]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px;">
                        <div style="font-size: 2em;">{member['emoji']}</div>
                        <p style="font-weight: bold; color: {member['color']};">{member['name']}</p>
                        <p style="font-size: 0.8em;">{member['archetype']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # User situation input
            st.markdown("#### 💭 Share Your Situation")
            council_situation = st.text_area(
                "What would you like the Council to discuss?",
                height=120,
                placeholder="Describe a situation, conflict, or question you'd like different perspectives on...",
                key="council_situation"
            )
            
            num_perspectives = st.slider(
                "How many council members should weigh in?",
                min_value=2,
                max_value=5,
                value=3
            )
            
            if st.button("🌟 Convene the Council", type="primary", key="convene_council"):
                if council_situation:
                    # Check for easter eggs
                    easter_egg = check_easter_egg(council_situation)
                    if easter_egg:
                        st.info(easter_egg)
                    
                    with st.spinner("The Council is gathering their thoughts..."):
                        discussions = generate_council_discussion(
                            council_situation,
                            age_profile,
                            num_perspectives
                        )
                        
                        st.markdown("### 🌌 The Council Speaks:")
                        
                        for discussion in discussions:
                            member = discussion['member']
                            response = discussion['response']
                            
                            st.markdown(f"""
                            <div class="council-member" style="border-color: {member['color']};">
                                <h4 style="color: {member['color']};">
                                    {member['emoji']} {member['name']} - {member['archetype']}
                                </h4>
                                <p style="margin-top: 10px;">{response}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Update progress
                        progress = update_progress(db, progress, "council")
                        progress.perspectives_understood = (progress.perspectives_understood or 0) + len(discussions)
                        db.commit()
                        
                        # Save exercise
                        exercise = DiplomaticExercise(
                            user_id=user.id,
                            exercise_type="council",
                            scenario_title="Council Consultation",
                            user_response=council_situation,
                            ai_feedback=str([d['response'] for d in discussions]),
                            council_members=[d['member']['name'] for d in discussions],
                            age_profile_used=age_profile['key']
                        )
                        db.add(exercise)
                        db.commit()
                        
                        st.success("✨ Council consultation complete! You've gained new perspectives!")
                else:
                    st.warning("Please share a situation for the Council to discuss!")
        
        # TAB 3: Empathy Bridge
        with tab3:
            st.markdown("### 🌉 Build an Empathy Bridge")
            st.markdown("""
            Sometimes two people or groups see things very differently.
            The Empathy Bridge helps translate between perspectives and find common ground!
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👤 Perspective A")
                perspective_a = st.text_area(
                    "Describe the first perspective:",
                    height=120,
                    placeholder="How does Person/Group A see the situation?",
                    key="perspective_a"
                )
            
            with col2:
                st.markdown("#### 👥 Perspective B")
                perspective_b = st.text_area(
                    "Describe the second perspective:",
                    height=120,
                    placeholder="How does Person/Group B see the situation?",
                    key="perspective_b"
                )
            
            if st.button("🌉 Build the Bridge", type="primary", key="build_bridge"):
                if perspective_a and perspective_b:
                    with st.spinner("Building the Empathy Bridge..."):
                        from ai_agents import generate_empathy_bridge
                        
                        bridge_result = generate_empathy_bridge(
                            perspective_a,
                            perspective_b,
                            age_profile
                        )
                        
                        st.markdown(f"""
                        <div class="scenario-card">
                            <h3>🌉 The Empathy Bridge</h3>
                            <p style="margin-top: 15px;">{bridge_result}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Update progress
                        progress = update_progress(db, progress, "bridge")
                        
                        # Save exercise
                        exercise = DiplomaticExercise(
                            user_id=user.id,
                            exercise_type="bridge",
                            scenario_title="Empathy Bridge",
                            user_response=f"A: {perspective_a}\n\nB: {perspective_b}",
                            ai_feedback=bridge_result,
                            age_profile_used=age_profile['key']
                        )
                        db.add(exercise)
                        db.commit()
                        
                        st.success("✨ Bridge built! Understanding flows both ways now!")
                else:
                    st.warning("Please describe both perspectives to build the bridge!")
        
        # TAB 4: About Diplomacy
        with tab4:
            st.markdown("### 📖 What is Diplomatic Thinking?")
            
            st.markdown("""
            <div class="scenario-card">
                <h4>🤝 Diplomacy is the Art of Understanding</h4>
                <p>Diplomatic thinking isn't about being weak or always agreeing with others. 
                It's about being <strong>smart and strong</strong> in how you handle disagreements!</p>
                
                <h4 style="margin-top: 20px;">🌟 The Core Skills:</h4>
                <ul>
                    <li><strong>Perspective-Taking:</strong> Seeing situations through different eyes</li>
                    <li><strong>Active Listening:</strong> Really hearing what others mean, not just what they say</li>
                    <li><strong>Finding Common Ground:</strong> Discovering what everyone actually wants</li>
                    <li><strong>Creative Problem-Solving:</strong> Finding solutions that work for everyone</li>
                    <li><strong>Emotional Intelligence:</strong> Understanding feelings (yours and others')</li>
                </ul>
                
                <h4 style="margin-top: 20px;">🌍 Why It Matters:</h4>
                <p>From playground disagreements to world peace, diplomatic thinking helps us:
                <ul>
                    <li>Solve problems without making enemies</li>
                    <li>Build stronger relationships</li>
                    <li>Create solutions nobody thought of before</li>
                    <li>Understand ourselves better by understanding others</li>
                </ul>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎓 Your Diplomatic Journey")
            
            # Show achievement roadmap
            st.markdown("#### Available Achievements:")
            
            ach_cols = st.columns(2)
            achievements_list = list(DIPLOMATIC_ACHIEVEMENTS.items())
            for i, (ach_key, ach) in enumerate(achievements_list):
                earned = ach_key in (progress.achievements or [])
                with ach_cols[i % 2]:
                    status = "✅" if earned else "🔒"
                    st.markdown(f"""
                    <div style="
                        background: {'linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.1))' if earned else 'rgba(255, 255, 255, 0.05)'};
                        padding: 15px;
                        border-radius: 10px;
                        margin: 10px 0;
                    ">
                        <p><strong>{status} {ach['title']}</strong></p>
                        <p style="font-size: 0.9em;">{ach['description']}</p>
                        <p style="color: #FFD700;">+{ach['points']} points</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Check and award new achievements
        new_achievements = check_achievement_progress(user_stats)
        if new_achievements:
            for ach in new_achievements:
                # Find the key for this achievement
                for key, val in DIPLOMATIC_ACHIEVEMENTS.items():
                    if val == ach and key not in (progress.achievements or []):
                        if not progress.achievements:
                            progress.achievements = []
                        progress.achievements.append(key)
                        progress.total_points = (progress.total_points or 0) + ach['points']
                        
                        st.balloons()
                        st.success(f"🏆 Achievement Unlocked: {ach['title']}! +{ach['points']} points!")
            
            db.commit()
    
    else:
        st.error("Could not find user. Please log in again.")
    
    db.close()
