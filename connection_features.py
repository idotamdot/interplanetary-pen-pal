# ======================================
# 🌟 CONNECTION FEATURES
# Meaningful features for inner and outer connection
# ======================================

import random
from datetime import datetime

# Daily Reflection Prompts
REFLECTION_PROMPTS = [
    "What moment today made you feel most alive?",
    "If your heart could speak without words, what would it say right now?",
    "What are you ready to release into the cosmic void?",
    "What small beauty did you notice today that others might have missed?",
    "If you could send one message to your past self, what would it be?",
    "What does your soul need right now?",
    "What are you becoming?",
    "What invisible thread connects you to someone you've never met?",
    "If your dreams spoke in colors, what hue would tonight be?",
    "What truth have you been avoiding?",
    "What makes you feel infinite?",
    "Who were you before the world told you who to be?",
    "What would you create if you knew no one was watching?",
    "What story are you telling yourself about yourself?",
    "What does home feel like to you?",
]

# Soul Questions for Deep Connection
SOUL_QUESTIONS = [
    "What experience changed you in ways you're still discovering?",
    "If you could live in a moment forever, which would you choose?",
    "What does your intuition keep whispering to you?",
    "What makes you feel connected to something larger than yourself?",
    "What paradox lives inside you?",
    "What do you know to be true that you can't prove?",
    "What would you do if you trusted yourself completely?",
    "What gift do you have that you've been too afraid to give?",
    "What does it feel like when you're exactly where you're supposed to be?",
    "What question do you wish someone would ask you?",
]

# Cosmic Quotes for Inspiration
COSMIC_QUOTES = [
    ("We are all made of stardust, trying to remember our way home.", "Carl Sagan"),
    ("The wound is the place where the Light enters you.", "Rumi"),
    ("What if you already are what you're becoming?", "Unknown"),
    ("You are not a drop in the ocean. You are the entire ocean in a drop.", "Rumi"),
    ("The cosmos is within us. We are made of star-stuff.", "Carl Sagan"),
    ("Your task is not to seek for love, but to find all the barriers within yourself that you have built against it.", "Rumi"),
    ("We are the universe experiencing itself.", "Alan Watts"),
    ("Everything you can imagine is real.", "Pablo Picasso"),
    ("The quieter you become, the more you can hear.", "Ram Dass"),
    ("You are the universe in ecstatic motion.", "Rumi"),
    ("What you seek is seeking you.", "Rumi"),
    ("The only way out is through.", "Robert Frost"),
    ("We are all just walking each other home.", "Ram Dass"),
    ("Let yourself be silently drawn by the strange pull of what you really love.", "Rumi"),
    ("The mystery of life is not a problem to be solved but a reality to be experienced.", "Aart van der Leeuw"),
]

# Elemental Energies
ELEMENTAL_ENERGIES = {
    "Water 🌊": {
        "quality": "Flow, Emotion, Intuition",
        "message": "Like water, you adapt and flow. Trust the currents of your emotions.",
        "color": "#4A90E2"
    },
    "Fire 🔥": {
        "quality": "Passion, Transformation, Courage",
        "message": "Like fire, you transform and illuminate. Let your passion guide you.",
        "color": "#E74C3C"
    },
    "Air 🌬️": {
        "quality": "Thought, Communication, Freedom",
        "message": "Like air, you move freely and connect all things. Your ideas take flight.",
        "color": "#95A5A6"
    },
    "Earth 🌍": {
        "quality": "Grounding, Growth, Stability",
        "message": "Like earth, you are rooted and nurturing. Your presence is an anchor.",
        "color": "#27AE60"
    },
    "Ether ✨": {
        "quality": "Spirit, Connection, Mystery",
        "message": "Like ether, you transcend boundaries. You are the space between all things.",
        "color": "#9B59B6"
    }
}

# Moon Phases
MOON_PHASES = {
    "New Moon 🌑": "Time for new beginnings, setting intentions, planting seeds",
    "Waxing Crescent 🌒": "Time for growth, taking action, building momentum",
    "First Quarter 🌓": "Time for decisions, overcoming challenges, commitment",
    "Waxing Gibbous 🌔": "Time for refinement, adjustment, almost there",
    "Full Moon 🌕": "Time for culmination, celebration, gratitude, releasing",
    "Waning Gibbous 🌖": "Time for sharing, teaching, giving back",
    "Last Quarter 🌗": "Time for forgiveness, letting go, breaking habits",
    "Waning Crescent 🌘": "Time for rest, reflection, surrender",
}

# Gratitude Prompts
GRATITUDE_PROMPTS = [
    "A person who made you smile today",
    "A comfort you often take for granted",
    "A lesson disguised as a challenge",
    "Something beautiful you witnessed",
    "A quality you appreciate in yourself",
    "An unexpected kindness you received",
    "A moment of peace you found",
    "Something your body allows you to do",
    "A connection that nourishes your soul",
    "A dream that still lives within you",
]

def get_daily_reflection():
    """Returns a reflection prompt based on the day"""
    day_of_year = datetime.now().timetuple().tm_yday
    return REFLECTION_PROMPTS[day_of_year % len(REFLECTION_PROMPTS)]

def get_soul_question():
    """Returns a random soul question"""
    return random.choice(SOUL_QUESTIONS)

def get_cosmic_quote():
    """Returns a cosmic quote with attribution"""
    quote, author = random.choice(COSMIC_QUOTES)
    return quote, author

def get_current_moon_phase():
    """Approximates current moon phase (simplified for visual/conceptual purposes)
    
    Note: This is a simplified calculation for user engagement.
    For production, consider using astronomy libraries like 'ephem' or 'astral'
    for accurate lunar calculations based on actual celestial mechanics.
    """
    # Simplified calculation - in production, use astronomy library
    day = datetime.now().day
    phase_index = (day % 29) // 4  # Approximate 8 phases over 29 days
    phases = list(MOON_PHASES.items())
    return phases[min(phase_index, 7)]

def get_element_of_day():
    """Returns element based on day of week"""
    elements = list(ELEMENTAL_ENERGIES.keys())
    day_of_week = datetime.now().weekday()
    return elements[day_of_week % len(elements)]

def get_gratitude_prompt():
    """Returns a random gratitude prompt"""
    return random.choice(GRATITUDE_PROMPTS)

# Constellation symbols for profile
CONSTELLATIONS = [
    "♈ Aries - The Ram",
    "♉ Taurus - The Bull", 
    "♊ Gemini - The Twins",
    "♋ Cancer - The Crab",
    "♌ Leo - The Lion",
    "♍ Virgo - The Maiden",
    "♎ Libra - The Scales",
    "♏ Scorpio - The Scorpion",
    "♐ Sagittarius - The Archer",
    "♑ Capricorn - The Goat",
    "♒ Aquarius - The Water Bearer",
    "♓ Pisces - The Fish",
    "⭐ Polaris - The North Star",
    "🌟 Sirius - The Brightest Star",
    "✨ Pleiades - The Seven Sisters",
    "🌠 Orion - The Hunter",
    "💫 Andromeda - The Chained Maiden",
    "🌌 Cassiopeia - The Queen",
]

# Mood/Energy Colors
MOOD_COLORS = {
    "Peaceful 💙": "#4A90E2",
    "Joyful 💛": "#F1C40F",
    "Creative 💜": "#9B59B6",
    "Energized 🧡": "#E67E22",
    "Reflective 💚": "#27AE60",
    "Dreamy 🩵": "#AED6F1",
    "Passionate ❤️": "#E74C3C",
    "Curious 🤍": "#ECF0F1",
}
