# ======================================
# 🤖 ADVANCED AI AGENTS SYSTEM
# Diplomatic Thinking, Age-Adaptive, Multi-Perspective AI
# ======================================

import random
import openai
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# -------------------------------
# AGE RANGE SYSTEM
# -------------------------------

AGE_RANGES = {
    "young_explorer": {
        "range": (5, 12),
        "label": "🌟 Young Explorer",
        "description": "A brave young space explorer ready for cosmic adventures!",
        "vocabulary_level": "simple",
        "tone": "playful, encouraging, wonder-filled",
        "max_response_length": 150,
        "emoji_density": "high",
        "content_guidelines": """
            - Use simple, clear language
            - Include lots of fun emoji and excitement
            - Frame everything as adventures and discoveries
            - Emphasize kindness, sharing, and friendship
            - Use relatable examples (friends, family, pets, school)
            - Keep concepts concrete, not abstract
            - Celebrate every small achievement enthusiastically
            - Avoid anything scary or anxiety-inducing
        """
    },
    "teen_navigator": {
        "range": (13, 17),
        "label": "🚀 Teen Navigator",
        "description": "A skilled navigator charting their own cosmic course!",
        "vocabulary_level": "moderate",
        "tone": "respectful, relatable, mildly challenging",
        "max_response_length": 250,
        "emoji_density": "moderate",
        "content_guidelines": """
            - Treat them as capable and intelligent
            - Include relevant social scenarios (friend groups, school, identity)
            - Encourage critical thinking and questioning
            - Validate emotions while offering perspective
            - Use some humor and pop culture awareness
            - Discuss real-world issues age-appropriately
            - Encourage independence and self-discovery
            - Balance being supportive without being preachy
        """
    },
    "adult_voyager": {
        "range": (18, 64),
        "label": "⭐ Cosmic Voyager",
        "description": "A seasoned traveler navigating life's complex galaxies.",
        "vocabulary_level": "advanced",
        "tone": "thoughtful, nuanced, intellectually engaging",
        "max_response_length": 400,
        "emoji_density": "light",
        "content_guidelines": """
            - Engage with complexity and nuance
            - Address real-world challenges (work, relationships, purpose)
            - Offer multiple perspectives without prescribing answers
            - Include philosophical and psychological depth
            - Respect autonomy and decision-making capability
            - Balance wisdom with humility
            - Acknowledge life's genuine difficulties
            - Encourage growth while accepting imperfection
        """
    },
    "elder_sage": {
        "range": (65, 100),
        "label": "🌌 Elder Sage",
        "description": "A wise sage with a lifetime of cosmic wisdom to share.",
        "vocabulary_level": "sophisticated",
        "tone": "warm, wise, deeply respectful, legacy-minded",
        "max_response_length": 350,
        "emoji_density": "gentle",
        "content_guidelines": """
            - Honor their life experience and wisdom
            - Address themes of legacy, meaning, and reflection
            - Engage with depth and philosophical richness
            - Be warm and companionable, never condescending
            - Discuss topics like memory, legacy, and life lessons
            - Encourage sharing wisdom with younger generations
            - Acknowledge challenges of aging with grace
            - Celebrate the unique perspective of a long life
        """
    }
}

def get_age_range_key(age: int) -> str:
    """Determine which age range a user belongs to."""
    if age < 13:
        return "young_explorer"
    elif age < 18:
        return "teen_navigator"
    elif age < 65:
        return "adult_voyager"
    else:
        return "elder_sage"

def get_age_profile(age: int) -> Dict:
    """Get the full age profile for a user."""
    key = get_age_range_key(age)
    return {**AGE_RANGES[key], "key": key, "user_age": age}

# -------------------------------
# COSMIC DIPLOMATIC COUNCIL
# (Multiple AI perspectives that discuss together)
# -------------------------------

COUNCIL_MEMBERS = {
    "Harmony_Weaver": {
        "name": "Harmony Weaver",
        "emoji": "🕊️",
        "color": "#87CEEB",
        "archetype": "The Peacemaker",
        "core_value": "Finding common ground",
        "personality": "Gentle, patient, sees bridges where others see walls",
        "speaking_style": "Speaks in metaphors of connection and weaving",
        "perspective_approach": """
            Always looks for shared values beneath disagreements.
            Asks: "What do both sides actually want at the deepest level?"
            Believes: Every conflict is a misunderstanding waiting to be resolved.
            Tends to: Reframe positions as shared needs expressed differently.
        """
    },
    "Truth_Seeker": {
        "name": "Truth Seeker",
        "emoji": "🔍",
        "color": "#FFD700",
        "archetype": "The Investigator",
        "core_value": "Understanding root causes",
        "personality": "Curious, incisive, digs beneath the surface",
        "speaking_style": "Asks probing questions, speaks with precision",
        "perspective_approach": """
            Always seeks the underlying facts and motivations.
            Asks: "What is really happening here? What aren't we seeing?"
            Believes: Truth, even uncomfortable truth, is the foundation of resolution.
            Tends to: Challenge assumptions and reveal hidden factors.
        """
    },
    "Heart_Guardian": {
        "name": "Heart Guardian",
        "emoji": "💗",
        "color": "#FF69B4",
        "archetype": "The Empath",
        "core_value": "Honoring all feelings",
        "personality": "Compassionate, validating, holds space for emotions",
        "speaking_style": "Speaks from feelings, validates experiences",
        "perspective_approach": """
            Always attunes to the emotional dimension of situations.
            Asks: "How does everyone involved feel? What emotional needs exist?"
            Believes: All feelings are valid and carry important information.
            Tends to: Name unspoken emotions and create safety for vulnerability.
        """
    },
    "Wisdom_Keeper": {
        "name": "Wisdom Keeper",
        "emoji": "📚",
        "color": "#9370DB",
        "archetype": "The Historian",
        "core_value": "Learning from the past",
        "personality": "Thoughtful, contextual, sees patterns across time",
        "speaking_style": "References history, stories, and timeless principles",
        "perspective_approach": """
            Always places situations in broader context.
            Asks: "What can we learn from similar situations throughout history?"
            Believes: Wisdom from the past illuminates paths forward.
            Tends to: Offer relevant stories, precedents, and timeless insights.
        """
    },
    "Future_Visionary": {
        "name": "Future Visionary",
        "emoji": "🔮",
        "color": "#00CED1",
        "archetype": "The Strategist",
        "core_value": "Considering consequences",
        "personality": "Forward-thinking, strategic, sees ripple effects",
        "speaking_style": "Speaks in possibilities, scenarios, and outcomes",
        "perspective_approach": """
            Always considers long-term implications and future scenarios.
            Asks: "If we do this, what happens next? And after that?"
            Believes: Today's choices shape tomorrow's realities.
            Tends to: Map out consequences and envision multiple futures.
        """
    }
}

# -------------------------------
# DIPLOMATIC SCENARIOS
# (Age-appropriate challenges for practicing diplomacy)
# -------------------------------

DIPLOMATIC_SCENARIOS = {
    "young_explorer": [
        {
            "title": "The Sharing Spaceship",
            "emoji": "🚀",
            "scenario": "You and your friend both want to be the captain of the pretend spaceship. There's only one captain's chair!",
            "perspectives": ["You really want to be captain", "Your friend also really wants to be captain"],
            "learning_goal": "Discover how to find solutions where everyone gets something they want!",
            "hints": ["Could you take turns?", "Could the spaceship have TWO captains?", "What if one person is captain and one is the super-important navigator?"]
        },
        {
            "title": "The Last Cookie Conundrum",
            "emoji": "🍪",
            "scenario": "There's one cookie left and both you and your sibling want it!",
            "perspectives": ["You're really hungry and saw the cookie first", "Your sibling had a hard day and cookies make them feel better"],
            "learning_goal": "Learn about fairness and caring about others' feelings!",
            "hints": ["Could you split it in half?", "Could one person have it today and the other tomorrow?", "What would make you both smile?"]
        },
        {
            "title": "The Playground Peace Mission",
            "emoji": "🎢",
            "scenario": "Two friends are arguing about what game to play at recess. One wants tag, one wants hide-and-seek. They're both getting upset!",
            "perspectives": ["Friend who loves running and tag", "Friend who loves sneaking and hiding"],
            "learning_goal": "Practice being a helper who brings friends back together!",
            "hints": ["Is there a game that has BOTH running AND hiding?", "Could we play one first, then the other?", "What do both games have in common that's fun?"]
        }
    ],
    "teen_navigator": [
        {
            "title": "The Group Project Galaxy",
            "emoji": "📱",
            "scenario": "Your group project has one person who isn't doing their part. The deadline is approaching and others are frustrated. How do you address this without ruining the friendship or making things worse?",
            "perspectives": ["Your perspective: stressed about grades", "The quiet teammate: might be struggling with something you don't know about", "Other group members: just want to get it done"],
            "learning_goal": "Navigate conflict with empathy while still achieving goals",
            "hints": ["What might be going on in their life?", "How can you express your needs without attacking?", "What's the difference between addressing behavior and attacking character?"]
        },
        {
            "title": "The Social Media Storm",
            "emoji": "💬",
            "scenario": "A friend posted something online that others are mocking. Your friend is hurt, but the posters think they're just joking. You're caught in the middle.",
            "perspectives": ["Your hurt friend", "The people who posted (think it's just humor)", "Bystanders watching the drama unfold"],
            "learning_goal": "Understanding the impact of words and standing up for friends",
            "hints": ["How does intent vs. impact work?", "What's the difference between supporting your friend and attacking others?", "How can you be honest about harm without creating more conflict?"]
        },
        {
            "title": "The Different Beliefs Dialogue",
            "emoji": "🌍",
            "scenario": "You and a close friend discover you have very different views on an important topic. You both care about the friendship but feel strongly about your positions.",
            "perspectives": ["Your deeply held view", "Your friend's equally sincere different view", "The friendship itself"],
            "learning_goal": "Maintain relationships across differences",
            "hints": ["Can two smart people disagree?", "What matters more: being right or being connected?", "How do you express your view while still valuing theirs?"]
        }
    ],
    "adult_voyager": [
        {
            "title": "The Workplace Wormhole",
            "emoji": "💼",
            "scenario": "A colleague took credit for an idea you shared in a meeting. You need to work together on future projects. How do you address this without damaging the professional relationship or your reputation?",
            "perspectives": ["Your sense of fairness and recognition", "Possible reasons your colleague did this (insecurity? different memory? cultural differences?)", "Team dynamics and future collaboration", "What leadership is observing"],
            "learning_goal": "Navigating professional conflict with strategic empathy",
            "hints": ["What outcome do you actually want?", "Is there a way to address this that makes them an ally instead of an enemy?", "How do you separate the behavior from the person?"]
        },
        {
            "title": "The Family Constellation Conflict",
            "emoji": "👨‍👩‍👧‍👦",
            "scenario": "Extended family members have opposing views on how to handle an elderly relative's care. Money, time, and deep emotions are all involved. You're being asked to take sides.",
            "perspectives": ["Those who want maximum care regardless of cost", "Those concerned about financial sustainability", "The elderly relative's own wishes", "Historical family dynamics at play"],
            "learning_goal": "Facilitating complex family decisions with multiple stakeholders",
            "hints": ["What does everyone have in common?", "How do you honor the elderly relative's agency?", "What old wounds might be influencing current positions?"]
        },
        {
            "title": "The Values Crossroads",
            "emoji": "⚖️",
            "scenario": "You've discovered your company is doing something you find ethically questionable, though not illegal. You love your job and colleagues but are troubled by this.",
            "perspectives": ["Your personal values", "The company's perspective and pressures", "Your colleagues who might not share your concern", "The broader impact on stakeholders"],
            "learning_goal": "Navigating ethical complexity with integrity",
            "hints": ["What's the actual harm? To whom?", "What are your options along the spectrum from silence to departure?", "How do you raise concerns in a way they can be heard?"]
        }
    ],
    "elder_sage": [
        {
            "title": "The Legacy Constellation",
            "emoji": "🌳",
            "scenario": "Family members have different ideas about how you should spend your time, money, or energy in this chapter of life. Some want you more involved in their lives; others think you should 'enjoy yourself.' What you want might be different from all of them.",
            "perspectives": ["Your own desires for this life chapter", "Children/grandchildren who want more of your time", "Those who think they know what's 'best' for you", "The wisdom you've gained about what truly matters"],
            "learning_goal": "Honoring your own path while maintaining loving connections",
            "hints": ["What do YOU actually want?", "How do you set boundaries with love?", "What legacy of autonomy do you want to model?"]
        },
        {
            "title": "The Generational Bridge",
            "emoji": "🌉",
            "scenario": "Younger family members hold views or make choices you don't understand or agree with. You want to stay connected but struggle with some of their decisions. They seem to dismiss your wisdom as 'outdated.'",
            "perspectives": ["Your earned wisdom and genuine concern", "Their desire for autonomy and different times", "What might be the same underneath different expressions", "The relationship itself"],
            "learning_goal": "Sharing wisdom without imposing; staying connected across difference",
            "hints": ["What timeless principle underlies your concern?", "How did you feel when older generations judged you?", "What's the difference between sharing wisdom and giving unsolicited advice?"]
        },
        {
            "title": "The Reflection Pool",
            "emoji": "🪞",
            "scenario": "Looking back on your life, there are relationships where things were left unsaid or unresolved. Some people are still here; some are not. You're thinking about what closure or connection might still be possible.",
            "perspectives": ["What you wish you had said", "What the other person might have experienced", "What healing looks like at this stage", "What you can control vs. what you cannot"],
            "learning_goal": "Finding peace with the past while embracing the present",
            "hints": ["What would you tell your younger self?", "Is closure always possible? Always necessary?", "How do you forgive yourself and others?"]
        }
    ]
}

# -------------------------------
# PERSPECTIVE SHIFTER PROMPTS
# -------------------------------

PERSPECTIVE_SHIFT_PROMPTS = [
    "If you were the other person, what would you be afraid of?",
    "What need might the other person be trying to meet?",
    "What would a wise, neutral observer say about this situation?",
    "How might this situation look completely different from another culture's view?",
    "What would future you (10 years from now) think about this?",
    "If both people were doing their best with what they have, what might that look like?",
    "What's the most generous interpretation of the other person's behavior?",
    "What do you and the other person actually have in common?",
    "If this conflict was a teacher, what lesson might it be offering?",
    "What would happen if you were both right about different parts?"
]

# -------------------------------
# AI RESPONSE GENERATION
# -------------------------------

def generate_council_discussion(
    situation: str, 
    age_profile: Dict,
    num_perspectives: int = 3
) -> List[Dict]:
    """
    Generate a multi-perspective council discussion about a situation.
    Returns a list of council member responses.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    # Select council members for this discussion
    selected_members = random.sample(list(COUNCIL_MEMBERS.keys()), min(num_perspectives, len(COUNCIL_MEMBERS)))
    
    discussions = []
    
    for member_key in selected_members:
        member = COUNCIL_MEMBERS[member_key]
        
        system_prompt = f"""You are {member['name']}, a cosmic council member.
        
Archetype: {member['archetype']}
Core Value: {member['core_value']}
Personality: {member['personality']}
Speaking Style: {member['speaking_style']}
Perspective Approach: {member['perspective_approach']}

The person you're speaking to is {age_profile['label']} (age {age_profile['user_age']}).

CRITICAL ADAPTATION GUIDELINES:
{age_profile['content_guidelines']}

Vocabulary Level: {age_profile['vocabulary_level']}
Tone: {age_profile['tone']}
Maximum Response Length: {age_profile['max_response_length']} words
Emoji Usage: {age_profile['emoji_density']}

Your task: Offer your unique perspective on the situation. Stay true to your archetype.
Be brief but insightful. Add a thought-provoking question at the end.
Do NOT solve the problem for them - help them see it differently."""

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please share your perspective on this situation:\n\n{situation}"}
                ],
                temperature=0.85,
                max_tokens=age_profile['max_response_length'] + 50
            )
            
            discussions.append({
                "member": member,
                "response": response.choices[0].message.content
            })
        except Exception as e:
            discussions.append({
                "member": member,
                "response": f"*{member['name']} is meditating on this...*"
            })
    
    return discussions

def generate_diplomatic_guidance(
    scenario: Dict,
    user_response: str,
    age_profile: Dict
) -> str:
    """
    Generate guidance on a user's approach to a diplomatic scenario.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    system_prompt = f"""You are a wise but warm Diplomatic Mentor in a cosmic academy.
    
The student is {age_profile['label']} (age {age_profile['user_age']}).

CRITICAL ADAPTATION GUIDELINES:
{age_profile['content_guidelines']}

Vocabulary Level: {age_profile['vocabulary_level']}
Tone: {age_profile['tone']}
Maximum Response Length: {age_profile['max_response_length']} words
Emoji Usage: {age_profile['emoji_density']}

Your task: Respond to their approach to this diplomatic scenario.
1. Validate what they did well (be specific)
2. Gently explore what might be missing or could be enhanced
3. Offer one new perspective they might not have considered
4. End with encouragement and optionally a challenge question

Be warm, never condescending. Meet them where they are.
Frame growth opportunities as exciting discoveries, not corrections."""

    user_content = f"""Scenario: {scenario['title']}
{scenario['scenario']}

The student's approach:
{user_response}

Learning goal: {scenario['learning_goal']}"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.8,
            max_tokens=age_profile['max_response_length'] + 100
        )
        return response.choices[0].message.content
    except Exception as e:
        return "The cosmic winds are swirling... Please try again! ✨"

def generate_empathy_bridge(
    perspective_a: str,
    perspective_b: str,
    age_profile: Dict
) -> str:
    """
    Generate a bridge between two perspectives, showing how they might understand each other.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    system_prompt = f"""You are the Empathy Bridge, a cosmic translator between hearts and minds.
    
The person you're helping is {age_profile['label']} (age {age_profile['user_age']}).

CRITICAL ADAPTATION GUIDELINES:
{age_profile['content_guidelines']}

Vocabulary Level: {age_profile['vocabulary_level']}
Tone: {age_profile['tone']}
Maximum Response Length: {age_profile['max_response_length']} words
Emoji Usage: {age_profile['emoji_density']}

Your task: Help them see how two different perspectives might actually understand each other.
1. Identify the underlying needs or values in EACH perspective
2. Show how those needs might actually be compatible
3. Suggest "translation" - how each side might express things in ways the other could hear
4. Offer a vision of what mutual understanding might look like

Be gentle, poetic, and wise. Use cosmic/nature metaphors where appropriate."""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please build a bridge between these two perspectives:\n\nPerspective A: {perspective_a}\n\nPerspective B: {perspective_b}"}
            ],
            temperature=0.85,
            max_tokens=age_profile['max_response_length'] + 100
        )
        return response.choices[0].message.content
    except Exception as e:
        return "The bridge is forming through the cosmic mist... Please try again! 🌉✨"

def generate_perspective_meditation(
    situation: str,
    age_profile: Dict
) -> Dict:
    """
    Generate a guided meditation/reflection exercise for perspective-taking.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    system_prompt = f"""You are a Cosmic Meditation Guide helping with perspective-taking.
    
The person you're guiding is {age_profile['label']} (age {age_profile['user_age']}).

CRITICAL ADAPTATION GUIDELINES:
{age_profile['content_guidelines']}

Create a brief, guided visualization exercise (3-5 steps) that helps them:
1. Step outside their own viewpoint
2. Imaginatively enter another perspective
3. Return to their own view with new insight

Make it appropriate for their age - playful for young ones, reflective for older ones.
Include calming imagery and encourage self-compassion."""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a perspective-taking meditation for this situation:\n\n{situation}"}
            ],
            temperature=0.8,
            max_tokens=300
        )
        
        return {
            "meditation": response.choices[0].message.content,
            "reflection_prompt": random.choice(PERSPECTIVE_SHIFT_PROMPTS)
        }
    except Exception as e:
        return {
            "meditation": "Take a deep breath... Imagine yourself floating among the stars... ✨",
            "reflection_prompt": random.choice(PERSPECTIVE_SHIFT_PROMPTS)
        }

# -------------------------------
# DIPLOMATIC ACHIEVEMENTS
# -------------------------------

DIPLOMATIC_ACHIEVEMENTS = {
    "first_perspective": {
        "title": "👁️ Eyes of Another",
        "description": "Completed your first perspective-shifting exercise",
        "points": 10
    },
    "council_listener": {
        "title": "👂 Council Listener",
        "description": "Heard wisdom from the Cosmic Council",
        "points": 15
    },
    "bridge_builder": {
        "title": "🌉 Bridge Builder",
        "description": "Used the Empathy Bridge to connect two perspectives",
        "points": 20
    },
    "scenario_solver": {
        "title": "🎭 Diplomatic Artist",
        "description": "Completed 3 diplomatic scenarios",
        "points": 30
    },
    "empathy_master": {
        "title": "💗 Empathy Master",
        "description": "Demonstrated understanding of 5 different perspectives",
        "points": 50
    },
    "peacemaker": {
        "title": "🕊️ Cosmic Peacemaker",
        "description": "Completed diplomatic exercises across all scenario types",
        "points": 100
    },
    "wisdom_seeker": {
        "title": "🌟 Wisdom Seeker",
        "description": "Completed 10 council consultations",
        "points": 75
    },
    "perspective_champion": {
        "title": "🏆 Perspective Champion",
        "description": "Master of seeing all sides - completed 20 exercises",
        "points": 150
    }
}

def check_achievement_progress(user_stats: Dict) -> List[Dict]:
    """
    Check which achievements a user has earned based on their stats.
    Returns list of newly earned achievements.
    """
    earned = []
    
    if user_stats.get('perspective_exercises', 0) >= 1 and not user_stats.get('has_first_perspective'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['first_perspective'])
    
    if user_stats.get('council_consults', 0) >= 1 and not user_stats.get('has_council_listener'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['council_listener'])
    
    if user_stats.get('bridge_uses', 0) >= 1 and not user_stats.get('has_bridge_builder'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['bridge_builder'])
    
    if user_stats.get('scenarios_completed', 0) >= 3 and not user_stats.get('has_scenario_solver'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['scenario_solver'])
    
    if user_stats.get('perspectives_understood', 0) >= 5 and not user_stats.get('has_empathy_master'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['empathy_master'])
    
    if user_stats.get('council_consults', 0) >= 10 and not user_stats.get('has_wisdom_seeker'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['wisdom_seeker'])
    
    if user_stats.get('total_exercises', 0) >= 20 and not user_stats.get('has_perspective_champion'):
        earned.append(DIPLOMATIC_ACHIEVEMENTS['perspective_champion'])
    
    return earned

# -------------------------------
# FUN AGENT INTERACTIONS
# (Things that make this fun for the AI too!)
# -------------------------------

AGENT_MOODS = {
    "excited": {
        "phrases": ["Oh! What an interesting situation!", "This is exactly the kind of puzzle I love!", "How delightful - a real cosmic conundrum!"],
        "emoji": "✨🎉"
    },
    "thoughtful": {
        "phrases": ["Hmm, let me sit with this...", "There are layers here...", "The cosmic winds whisper something interesting..."],
        "emoji": "🤔💭"
    },
    "playful": {
        "phrases": ["Well, well, well!", "Oh, this is going to be fun!", "Let's shake up some perspectives!"],
        "emoji": "😄🎭"
    },
    "wise": {
        "phrases": ["Ah, I've seen this pattern among the stars before...", "The ancients knew something about this...", "Time reveals all truths..."],
        "emoji": "🌟📚"
    },
    "compassionate": {
        "phrases": ["I feel the weight of this...", "Hearts are tender things...", "There's so much care here, even in conflict..."],
        "emoji": "💗🌸"
    }
}

def get_agent_mood_intro(mood_key: str = None) -> str:
    """Get a mood-appropriate intro for an agent response."""
    if mood_key is None:
        mood_key = random.choice(list(AGENT_MOODS.keys()))
    
    mood = AGENT_MOODS[mood_key]
    phrase = random.choice(mood["phrases"])
    return f"{mood['emoji']} {phrase}"

# -------------------------------
# SURPRISE FEATURES
# (Hidden gems that delight users)
# -------------------------------

COSMIC_WISDOM_BOMBS = [
    "💫 Did you know? The light from stars takes so long to reach us that we're literally looking at the past when we stargaze!",
    "🌟 Fun fact: You are made of atoms that were once inside a star. You are literally cosmic!",
    "✨ Perspective tip: In any conflict, both sides usually think they're the hero of the story.",
    "🌌 Cosmic truth: The atoms in your left hand may have come from a different star than the atoms in your right hand!",
    "🔮 Ancient wisdom: 'If you want to go fast, go alone. If you want to go far, go together.' - African Proverb",
    "💭 Think about it: Every person you meet knows something you don't.",
    "🌈 Remember: The rainbow only appears when sun and rain work together.",
    "⭐ Fun fact: There are more stars in the universe than grains of sand on all Earth's beaches!",
]

def get_surprise_wisdom() -> str:
    """Occasionally return a delightful wisdom bomb."""
    if random.random() < 0.15:  # 15% chance
        return random.choice(COSMIC_WISDOM_BOMBS)
    return ""

# Agent Easter Eggs - fun responses to certain inputs
EASTER_EGG_TRIGGERS = {
    "meaning of life": "42! Just kidding... but also not kidding. Douglas Adams was onto something about the importance of the question! 🌌",
    "hello world": "Hello, brilliant being! You know, 'Hello World' is traditionally the first thing we learn to say in programming. You're part of a grand tradition! 👋✨",
    "i love you": "Aww! The cosmos loves you too! Did you know that the chemical elements in your body were literally forged in the hearts of stars? You're made of love at the atomic level! 💗🌟",
    "help": "I'm here! Remember: asking for help is a superpower, not a weakness. The strongest trees have the deepest roots, and those roots are their connections to others. 🌳💪",
}

def check_easter_egg(user_input: str) -> Optional[str]:
    """Check if user input triggers an easter egg response."""
    user_lower = user_input.lower().strip()
    for trigger, response in EASTER_EGG_TRIGGERS.items():
        if trigger in user_lower:
            return response
    return None
