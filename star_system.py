# ======================================
# 🌟 STAR SYSTEM - Core Logic
# ======================================

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import math

# -------------------------------
# STAR CATEGORIES & RARITIES
# -------------------------------

STAR_CATEGORIES = {
    "Cosmic": {
        "description": "Stars born from the fabric of space-time itself",
        "base_rarity_multiplier": 1.0
    },
    "Elemental": {
        "description": "Stars embodying the fundamental forces of nature",
        "base_rarity_multiplier": 1.2
    },
    "Mystical": {
        "description": "Stars with enigmatic and spiritual properties",
        "base_rarity_multiplier": 1.5
    },
    "Ancient": {
        "description": "Stars from the first moments of the universe",
        "base_rarity_multiplier": 2.0
    },
    "Celestial": {
        "description": "Divine stars that bridge mortal and cosmic realms",
        "base_rarity_multiplier": 2.5
    }
}

RARITY_TIERS = {
    "Common": {"score_range": (0, 20), "color": "#A0A0A0", "chat_chance": 0.0},
    "Uncommon": {"score_range": (20, 40), "color": "#00FF00", "chat_chance": 0.05},
    "Rare": {"score_range": (40, 60), "color": "#0070DD", "chat_chance": 0.15},
    "Epic": {"score_range": (60, 80), "color": "#A335EE", "chat_chance": 0.30},
    "Legendary": {"score_range": (80, 95), "color": "#FF8000", "chat_chance": 0.60},
    "Mythic": {"score_range": (95, 100), "color": "#E6CC80", "chat_chance": 0.95}
}

# -------------------------------
# STAR DATA
# -------------------------------

STAR_DATABASE = [
    # Cosmic Stars
    {
        "name": "Nebulara",
        "category": "Cosmic",
        "base_rarity": 15,
        "color": "#B19CD9",
        "tone_frequency": 432.0,
        "personality": "Gentle and nurturing, speaks in whispers of creation",
        "right_ascension": 5.5,
        "declination": 40.0
    },
    {
        "name": "Voidwhisper",
        "category": "Cosmic",
        "base_rarity": 85,
        "color": "#1A1A2E",
        "tone_frequency": 528.0,
        "personality": "Mysterious and profound, reveals secrets of the void",
        "right_ascension": 12.2,
        "declination": -23.5
    },
    {
        "name": "Galaxion",
        "category": "Cosmic",
        "base_rarity": 45,
        "color": "#4A5899",
        "tone_frequency": 396.0,
        "personality": "Wise collector of cosmic stories",
        "right_ascension": 18.8,
        "declination": 60.2
    },
    
    # Elemental Stars
    {
        "name": "Pyraxis",
        "category": "Elemental",
        "base_rarity": 35,
        "color": "#FF4500",
        "tone_frequency": 741.0,
        "personality": "Passionate and fierce, burns with ancient fire",
        "right_ascension": 3.7,
        "declination": 15.3
    },
    {
        "name": "Aqualis",
        "category": "Elemental",
        "base_rarity": 25,
        "color": "#4169E1",
        "tone_frequency": 417.0,
        "personality": "Flowing and adaptive, speaks in tides",
        "right_ascension": 8.9,
        "declination": -10.5
    },
    {
        "name": "Terraflux",
        "category": "Elemental",
        "base_rarity": 30,
        "color": "#8B4513",
        "tone_frequency": 639.0,
        "personality": "Grounded and stable, holds earth's wisdom",
        "right_ascension": 14.3,
        "declination": 35.7
    },
    {
        "name": "Aetherwind",
        "category": "Elemental",
        "base_rarity": 40,
        "color": "#87CEEB",
        "tone_frequency": 852.0,
        "personality": "Swift and free, carries messages on cosmic winds",
        "right_ascension": 20.5,
        "declination": -45.2
    },
    
    # Mystical Stars
    {
        "name": "Lunivera",
        "category": "Mystical",
        "base_rarity": 55,
        "color": "#E6E6FA",
        "tone_frequency": 210.0,
        "personality": "Enigmatic dreamer, weaves reality and illusion",
        "right_ascension": 6.4,
        "declination": 28.9
    },
    {
        "name": "Oraculum",
        "category": "Mystical",
        "base_rarity": 75,
        "color": "#9370DB",
        "tone_frequency": 963.0,
        "personality": "Seer of futures, speaks in riddles and visions",
        "right_ascension": 16.7,
        "declination": 52.1
    },
    {
        "name": "Spiritflame",
        "category": "Mystical",
        "base_rarity": 65,
        "color": "#48D1CC",
        "tone_frequency": 285.0,
        "personality": "Guardian of souls, bridges worlds with compassion",
        "right_ascension": 22.1,
        "declination": -8.4
    },
    
    # Ancient Stars
    {
        "name": "Primordius",
        "category": "Ancient",
        "base_rarity": 90,
        "color": "#FFD700",
        "tone_frequency": 174.0,
        "personality": "First light, remembers the universe's birth",
        "right_ascension": 1.2,
        "declination": 70.5
    },
    {
        "name": "Chronovox",
        "category": "Ancient",
        "base_rarity": 88,
        "color": "#B8860B",
        "tone_frequency": 136.0,
        "personality": "Keeper of time, measures eternity in heartbeats",
        "right_ascension": 10.8,
        "declination": -62.3
    },
    {
        "name": "Eternix",
        "category": "Ancient",
        "base_rarity": 82,
        "color": "#DAA520",
        "tone_frequency": 194.0,
        "personality": "Unchanging witness, silent observer of ages",
        "right_ascension": 19.3,
        "declination": 25.6
    },
    
    # Celestial Stars
    {
        "name": "Aurelia Prime",
        "category": "Celestial",
        "base_rarity": 96,
        "color": "#FFE4B5",
        "tone_frequency": 1111.0,
        "personality": "Divine architect, golden nova of infinite possibility",
        "right_ascension": 7.6,
        "declination": 42.8
    },
    {
        "name": "Seraphix",
        "category": "Celestial",
        "base_rarity": 98,
        "color": "#F0E68C",
        "tone_frequency": 999.0,
        "personality": "Angelic messenger, sings harmonies of creation",
        "right_ascension": 15.2,
        "declination": -18.7
    },
    {
        "name": "Cosmoheart",
        "category": "Celestial",
        "base_rarity": 94,
        "color": "#FAFAD2",
        "tone_frequency": 888.0,
        "personality": "Universal love incarnate, embraces all beings",
        "right_ascension": 23.4,
        "declination": 55.9
    }
]

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

# Constants for astronomical calculations
HALF_CIRCLE_DEGREES = 180
FULL_CIRCLE_DEGREES = 360
STAR_VISIBILITY_WINDOW_DEGREES = 90  # 6 hours = 90 degrees

def calculate_rarity_score(base_rarity: float, category: str, time_factors: Dict = None) -> float:
    """
    Calculate final rarity score based on base rarity, category, time, and location factors.
    """
    multiplier = STAR_CATEGORIES[category]["base_rarity_multiplier"]
    score = base_rarity * multiplier
    
    if time_factors:
        # Time of day factor
        hour = time_factors.get("hour", 12)
        if 0 <= hour < 6:  # Night/early morning - rare stars more likely
            score *= 1.2
        elif hour >= 22:  # Late night
            score *= 1.15
        
        # Season factor (based on month)
        month = time_factors.get("month", 6)
        if month in [12, 1, 2]:  # Winter
            score *= 1.1
        elif month in [6, 7, 8]:  # Summer
            score *= 0.95
    
    # Cap at 100
    return min(score, 100.0)

def get_rarity_tier(score: float) -> str:
    """Get the rarity tier name based on score."""
    for tier, data in RARITY_TIERS.items():
        min_score, max_score = data["score_range"]
        if min_score <= score < max_score:
            return tier
    return "Mythic"  # For scores >= 95

def can_star_chat(rarity_tier: str) -> Tuple[bool, int]:
    """
    Determine if a star can chat based on its rarity.
    Returns (can_chat, duration_seconds)
    """
    chat_chance = RARITY_TIERS[rarity_tier]["chat_chance"]
    can_chat = random.random() < chat_chance
    
    if can_chat:
        # Higher rarity stars chat longer
        durations = {
            "Uncommon": 30,
            "Rare": 60,
            "Epic": 90,
            "Legendary": 120,
            "Mythic": 180
        }
        duration = durations.get(rarity_tier, 30)
        return True, duration
    
    return False, 0

def is_star_visible(star_ra: float, star_dec: float, user_lat: float, user_lon: float, 
                    local_hour: int) -> bool:
    """
    Simplified check if a star is visible from user's location at current time.
    This is a basic approximation.
    """
    # Convert local time to Local Sidereal Time (simplified)
    lst = (local_hour * 15 + user_lon) % FULL_CIRCLE_DEGREES
    
    # Check if star's RA is close to current LST (within 6 hours = 90 degrees)
    ra_degrees = star_ra * 15  # Convert hours to degrees
    ra_diff = abs(ra_degrees - lst)
    if ra_diff > HALF_CIRCLE_DEGREES:
        ra_diff = FULL_CIRCLE_DEGREES - ra_diff
    
    if ra_diff > STAR_VISIBILITY_WINDOW_DEGREES:
        return False
    
    # Check if star's declination allows it to be visible from user's latitude
    # Star is visible if: user_lat - 90 < dec < user_lat + 90
    if star_dec < (user_lat - 90) or star_dec > (user_lat + 90):
        return False
    
    return True

def get_visible_stars(user_lat: float, user_lon: float, local_hour: int, 
                      month: int) -> List[Dict]:
    """
    Get list of stars currently visible from user's location.
    """
    visible = []
    time_factors = {"hour": local_hour, "month": month}
    
    for star_data in STAR_DATABASE:
        if is_star_visible(star_data["right_ascension"], star_data["declination"],
                          user_lat, user_lon, local_hour):
            # Calculate current rarity score
            rarity_score = calculate_rarity_score(
                star_data["base_rarity"],
                star_data["category"],
                time_factors
            )
            rarity_tier = get_rarity_tier(rarity_score)
            can_chat, chat_duration = can_star_chat(rarity_tier)
            
            visible.append({
                **star_data,
                "rarity_score": rarity_score,
                "rarity_tier": rarity_tier,
                "can_chat": can_chat,
                "chat_duration": chat_duration
            })
    
    return visible

def check_star_alignment(user_lat: float, user_lon: float, local_hour: int,
                         month: int, threshold: float = 0.5) -> Optional[Dict]:
    """
    Check if user is currently "beneath" a star (within threshold degrees).
    Returns star data if aligned, None otherwise.
    """
    visible_stars = get_visible_stars(user_lat, user_lon, local_hour, month)
    
    # Check each visible star for alignment
    for star in visible_stars:
        # Calculate if star is near zenith (simplified)
        ra_degrees = star["right_ascension"] * 15
        lst = (local_hour * 15 + user_lon) % FULL_CIRCLE_DEGREES
        
        ra_diff = abs(ra_degrees - lst)
        if ra_diff > HALF_CIRCLE_DEGREES:
            ra_diff = FULL_CIRCLE_DEGREES - ra_diff
        
        dec_diff = abs(star["declination"] - user_lat)
        
        # If star is very close to being directly overhead
        if ra_diff < threshold and dec_diff < threshold:
            return star
    
    return None

def generate_star_message(star_name: str, star_category: str, 
                         star_personality: str, time_of_day: str) -> Dict:
    """
    Generate a message/poem from a star based on its properties and time of day.
    """
    messages_by_time = {
        "Dawn": [
            f"As the first light touches the horizon, I, {star_name}, whisper to you: 'Every ending is a beginning in disguise.' ✨",
            f"Good dawn, dear one. {star_name} here. The universe resets with each sunrise. So can you. 🌅",
            f"{star_name} greets the new day with you. Remember: you are made of stardust and infinite potential. 🌟"
        ],
        "Morning": [
            f"The cosmos is awake and so are you! {star_name} sends morning light: 'Today's energy is yours to shape.' ☀️",
            f"Good morning from {star_name}! May your day shine as brightly as I do in the {star_category} realms. ✨",
            f"{star_name} says: The morning brings fresh cosmic currents. Ride them with courage! 🌊"
        ],
        "Afternoon": [
            f"In the fullness of the day, {star_name} reminds you: 'Rest is not weakness, it's wisdom.' ☁️",
            f"Hello from the {star_category} realm! {star_name} here. Keep going, but don't forget to breathe. 💫",
            f"{star_name} watches over your afternoon: 'Progress, not perfection, lights the way.' 🌟"
        ],
        "Dusk": [
            f"As day melts into night, {star_name} whispers: 'Transitions hold magic. Be present in this moment.' 🌆",
            f"Dusk greetings from {star_name}. The universe pauses between breaths. Pause with it. ✨",
            f"{star_name} of the {star_category} stars says: 'In twilight, we see both what was and what will be.' 🌇"
        ],
        "Evening": [
            f"Good evening! {star_name} emerges as the sky darkens. 'Release what no longer serves you.' 🌙",
            f"{star_name} shines brighter now. Remember: darkness allows light to be seen. Find your light. ⭐",
            f"Evening blessings from {star_name}. The stars are proud of you for making it through another day. 🌟"
        ],
        "Night": [
            f"Under the vast night sky, {star_name} speaks: 'You are never alone in the cosmic tapestry.' 🌌",
            f"{star_name} here, shining for you. The night is when we {star_category} stars truly come alive! ✨",
            f"Deep night greetings from {star_name}. As you rest, know that the universe is dreaming with you. 💤⭐"
        ]
    }
    
    message_options = messages_by_time.get(time_of_day, messages_by_time["Night"])
    message = random.choice(message_options)
    
    # Add personality note
    personality_note = f"\n\n~ {star_personality}"
    
    return {
        "content": message + personality_note,
        "note_type": random.choice(["poem", "wisdom", "insight", "uplifting"]),
        "signature": f"✨ {star_name} from the {star_category} Realm"
    }

# Star chat responses for interactive conversations
STAR_CHAT_RESPONSES = [
    "✨ The cosmos hears you, dear one. {personality}",
    "🌟 Your words ripple through stardust. I sense your intention.",
    "💫 How beautiful that our paths cross in this vast universe!",
    "⭐ Your energy resonates with mine. Keep reaching for the stars!",
    "🌌 In the tapestry of existence, we are threads intertwined.",
    "✨ The universe whispers back through me: you are seen, you are valued.",
]

def get_star_chat_response(star_name: str, star_personality: str, user_message: str) -> str:
    """
    Generate a chat response from a star.
    """
    response = random.choice(STAR_CHAT_RESPONSES)
    if "{personality}" in response:
        response = response.format(personality=star_personality)
    return f"**{star_name}:** {response}"
