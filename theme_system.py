# ======================================
# 🎨 DYNAMIC THEME SYSTEM
# ======================================

from datetime import datetime
from typing import Dict, Tuple
import math

# -------------------------------
# SEASON DETECTION
# -------------------------------

def get_season(month: int, latitude: float) -> str:
    """
    Determine the season based on month and latitude.
    Accounts for hemisphere differences.
    """
    # Northern hemisphere seasons
    seasons_north = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    }
    
    season = seasons_north.get(month, "Spring")
    
    # Reverse for southern hemisphere
    if latitude < 0:
        season_map = {
            "Winter": "Summer",
            "Summer": "Winter",
            "Spring": "Autumn",
            "Autumn": "Spring"
        }
        season = season_map.get(season, season)
    
    return season

def get_time_of_day(hour: int) -> str:
    """
    Determine the time of day period based on hour (0-23).
    """
    if 5 <= hour < 7:
        return "Dawn"
    elif 7 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 19:
        return "Dusk"
    elif 19 <= hour < 22:
        return "Evening"
    else:
        return "Night"

# -------------------------------
# THEME COLOR SCHEMES
# -------------------------------

THEMES = {
    # Spring themes
    "Spring_Dawn": {
        "primary": "#FFB6C1",  # Light pink
        "background": "#FFF8DC",  # Cornsilk
        "secondary_bg": "#F0E68C",  # Khaki
        "text": "#2F4F4F",  # Dark slate gray
        "accent": "#98FB98",  # Pale green
        "description": "Fresh spring dawn with blooming colors"
    },
    "Spring_Morning": {
        "primary": "#7CFC00",  # Lawn green
        "background": "#F0FFF0",  # Honeydew
        "secondary_bg": "#E0FFE0",  # Light mint
        "text": "#228B22",  # Forest green
        "accent": "#FFD700",  # Gold
        "description": "Vibrant spring morning energy"
    },
    "Spring_Afternoon": {
        "primary": "#00CED1",  # Dark turquoise
        "background": "#F0FFFF",  # Azure
        "secondary_bg": "#E0FFFF",  # Light cyan
        "text": "#2F4F4F",  # Dark slate gray
        "accent": "#FFA07A",  # Light salmon
        "description": "Gentle spring afternoon breeze"
    },
    "Spring_Dusk": {
        "primary": "#DA70D6",  # Orchid
        "background": "#FFF0F5",  # Lavender blush
        "secondary_bg": "#FFE4E1",  # Misty rose
        "text": "#483D8B",  # Dark slate blue
        "accent": "#FFB6C1",  # Light pink
        "description": "Soft spring dusk transition"
    },
    "Spring_Evening": {
        "primary": "#9370DB",  # Medium purple
        "background": "#E6E6FA",  # Lavender
        "secondary_bg": "#D8BFD8",  # Thistle
        "text": "#4B0082",  # Indigo
        "accent": "#DDA0DD",  # Plum
        "description": "Mystical spring evening"
    },
    "Spring_Night": {
        "primary": "#4169E1",  # Royal blue
        "background": "#191970",  # Midnight blue
        "secondary_bg": "#2F4F7F",  # Darker blue
        "text": "#E0E0FF",  # Light lavender
        "accent": "#00FA9A",  # Medium spring green
        "description": "Serene spring night sky"
    },
    
    # Summer themes
    "Summer_Dawn": {
        "primary": "#FF6347",  # Tomato
        "background": "#FFF5EE",  # Seashell
        "secondary_bg": "#FFDAB9",  # Peach puff
        "text": "#8B4513",  # Saddle brown
        "accent": "#FFD700",  # Gold
        "description": "Warm summer dawn breaking"
    },
    "Summer_Morning": {
        "primary": "#FF8C00",  # Dark orange
        "background": "#FFFAF0",  # Floral white
        "secondary_bg": "#FFE4B5",  # Moccasin
        "text": "#B8860B",  # Dark goldenrod
        "accent": "#FF4500",  # Orange red
        "description": "Bright summer morning sun"
    },
    "Summer_Afternoon": {
        "primary": "#FFD700",  # Gold
        "background": "#FFFFE0",  # Light yellow
        "secondary_bg": "#FFEF99",  # Pale gold
        "text": "#8B7500",  # Dark gold
        "accent": "#FF6347",  # Tomato
        "description": "Hot summer afternoon glow"
    },
    "Summer_Dusk": {
        "primary": "#FF4500",  # Orange red
        "background": "#FFE4E1",  # Misty rose
        "secondary_bg": "#FFDAB9",  # Peach puff
        "text": "#8B4513",  # Saddle brown
        "accent": "#FF1493",  # Deep pink
        "description": "Fiery summer sunset"
    },
    "Summer_Evening": {
        "primary": "#FF69B4",  # Hot pink
        "background": "#FFF0F5",  # Lavender blush
        "secondary_bg": "#FFB6C1",  # Light pink
        "text": "#8B008B",  # Dark magenta
        "accent": "#FF6347",  # Tomato
        "description": "Vibrant summer evening"
    },
    "Summer_Night": {
        "primary": "#6495ED",  # Cornflower blue
        "background": "#0F0F23",  # Very dark blue
        "secondary_bg": "#1A1A3E",  # Dark navy
        "text": "#E0E0FF",  # Light lavender
        "accent": "#FFD700",  # Gold
        "description": "Warm summer night sky"
    },
    
    # Autumn themes
    "Autumn_Dawn": {
        "primary": "#CD853F",  # Peru
        "background": "#FFF8DC",  # Cornsilk
        "secondary_bg": "#FFDEAD",  # Navajo white
        "text": "#8B4513",  # Saddle brown
        "accent": "#FF8C00",  # Dark orange
        "description": "Crisp autumn dawn"
    },
    "Autumn_Morning": {
        "primary": "#FF8C00",  # Dark orange
        "background": "#FFFAF0",  # Floral white
        "secondary_bg": "#FFE4B5",  # Moccasin
        "text": "#8B4513",  # Saddle brown
        "accent": "#DC143C",  # Crimson
        "description": "Golden autumn morning"
    },
    "Autumn_Afternoon": {
        "primary": "#D2691E",  # Chocolate
        "background": "#FFF5EE",  # Seashell
        "secondary_bg": "#FFDAB9",  # Peach puff
        "text": "#654321",  # Dark brown
        "accent": "#FF6347",  # Tomato
        "description": "Mellow autumn afternoon"
    },
    "Autumn_Dusk": {
        "primary": "#8B4513",  # Saddle brown
        "background": "#FFE4C4",  # Bisque
        "secondary_bg": "#DEB887",  # Burlywood
        "text": "#4B3621",  # Very dark brown
        "accent": "#DC143C",  # Crimson
        "description": "Rustic autumn dusk"
    },
    "Autumn_Evening": {
        "primary": "#B8860B",  # Dark goldenrod
        "background": "#2F2F1F",  # Dark olive
        "secondary_bg": "#3F3F2F",  # Darker olive
        "text": "#FFD700",  # Gold
        "accent": "#FF4500",  # Orange red
        "description": "Deep autumn evening"
    },
    "Autumn_Night": {
        "primary": "#8B7355",  # Burlywood dark
        "background": "#1A1410",  # Very dark brown
        "secondary_bg": "#2A2420",  # Dark brown
        "text": "#F5DEB3",  # Wheat
        "accent": "#CD853F",  # Peru
        "description": "Mysterious autumn night"
    },
    
    # Winter themes
    "Winter_Dawn": {
        "primary": "#B0C4DE",  # Light steel blue
        "background": "#F0F8FF",  # Alice blue
        "secondary_bg": "#E6F2FF",  # Very light blue
        "text": "#2F4F7F",  # Dark blue
        "accent": "#87CEEB",  # Sky blue
        "description": "Frosty winter dawn"
    },
    "Winter_Morning": {
        "primary": "#4682B4",  # Steel blue
        "background": "#F0FFFF",  # Azure
        "secondary_bg": "#E0F6FF",  # Light azure
        "text": "#1C4966",  # Dark blue
        "accent": "#ADD8E6",  # Light blue
        "description": "Crisp winter morning"
    },
    "Winter_Afternoon": {
        "primary": "#5F9EA0",  # Cadet blue
        "background": "#F0F8FF",  # Alice blue
        "secondary_bg": "#E0F0F8",  # Light alice blue
        "text": "#2F4F4F",  # Dark slate gray
        "accent": "#B0E0E6",  # Powder blue
        "description": "Serene winter afternoon"
    },
    "Winter_Dusk": {
        "primary": "#6A5ACD",  # Slate blue
        "background": "#E6E6FA",  # Lavender
        "secondary_bg": "#D8D8F0",  # Light lavender
        "text": "#483D8B",  # Dark slate blue
        "accent": "#9370DB",  # Medium purple
        "description": "Twilight winter sky"
    },
    "Winter_Evening": {
        "primary": "#4169E1",  # Royal blue
        "background": "#1C1C3C",  # Dark blue
        "secondary_bg": "#2C2C4C",  # Darker blue
        "text": "#E0E0FF",  # Light lavender
        "accent": "#6495ED",  # Cornflower blue
        "description": "Cold winter evening"
    },
    "Winter_Night": {
        "primary": "#191970",  # Midnight blue
        "background": "#0A0A1A",  # Very dark blue
        "secondary_bg": "#14142A",  # Darker navy
        "text": "#E0E0FF",  # Light lavender
        "accent": "#4169E1",  # Royal blue
        "description": "Deep winter night"
    }
}

# -------------------------------
# THEME FUNCTIONS
# -------------------------------

def get_current_theme(latitude: float = 40.0, hour: int = None, month: int = None) -> Dict:
    """
    Get the current theme based on location and time.
    """
    now = datetime.now()
    if hour is None:
        hour = now.hour
    if month is None:
        month = now.month
    
    season = get_season(month, latitude)
    time_period = get_time_of_day(hour)
    
    theme_key = f"{season}_{time_period}"
    theme = THEMES.get(theme_key, THEMES["Spring_Morning"])
    
    return {
        **theme,
        "season": season,
        "time_of_day": time_period,
        "theme_key": theme_key
    }

def generate_css(theme: Dict) -> str:
    """
    Generate CSS for the current theme with smooth transitions.
    """
    transition_duration = "2s"  # Can be adjusted for faster/slower theme changes
    
    css = f"""
    <style>
    /* Dynamic Theme Styles */
    :root {{
        --primary-color: {theme['primary']};
        --bg-color: {theme['background']};
        --secondary-bg-color: {theme['secondary_bg']};
        --text-color: {theme['text']};
        --accent-color: {theme['accent']};
        --transition-duration: {transition_duration};
    }}
    
    * {{
        transition: background-color var(--transition-duration) ease, 
                    color var(--transition-duration) ease, 
                    border-color var(--transition-duration) ease;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {theme['background']} 0%, {theme['secondary_bg']} 100%);
    }}
    
    .theme-info {{
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 10px 15px;
        border-radius: 10px;
        font-size: 12px;
        color: {theme['text']};
        border: 1px solid {theme['accent']};
        z-index: 1000;
    }}
    
    .star-encounter {{
        background: linear-gradient(135deg, {theme['primary']}, {theme['accent']});
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
        animation: starGlow 3s ease-in-out infinite;
    }}
    
    @keyframes starGlow {{
        0%, 100% {{ box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }}
        50% {{ box-shadow: 0 8px 48px {theme['accent']}80; }}
    }}
    
    .star-note {{
        background: {theme['secondary_bg']};
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid {theme['accent']};
        margin: 15px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }}
    
    .rarity-common {{ color: #A0A0A0; text-shadow: 0 0 5px #A0A0A0; }}
    .rarity-uncommon {{ color: #00FF00; text-shadow: 0 0 5px #00FF00; }}
    .rarity-rare {{ color: #0070DD; text-shadow: 0 0 5px #0070DD; }}
    .rarity-epic {{ color: #A335EE; text-shadow: 0 0 5px #A335EE; }}
    .rarity-legendary {{ color: #FF8000; text-shadow: 0 0 5px #FF8000; }}
    .rarity-mythic {{ color: #E6CC80; text-shadow: 0 0 10px #FFD700; animation: mythicGlow 2s ease-in-out infinite; }}
    
    @keyframes mythicGlow {{
        0%, 100% {{ text-shadow: 0 0 10px #FFD700, 0 0 20px #FFD700; }}
        50% {{ text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFA500; }}
    }}
    
    .star-twinkle {{
        animation: twinkle 1.5s ease-in-out infinite;
    }}
    
    @keyframes twinkle {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(1.2); }}
    }}
    
    .chime-indicator {{
        animation: chimeRing 0.8s ease-out;
    }}
    
    @keyframes chimeRing {{
        0% {{ transform: scale(0.8) rotate(-5deg); opacity: 0; }}
        50% {{ transform: scale(1.1) rotate(5deg); opacity: 1; }}
        100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
    }}
    </style>
    """
    return css

def get_theme_emoji(season: str, time_of_day: str) -> str:
    """
    Get an appropriate emoji for the current theme.
    """
    emojis = {
        "Spring_Dawn": "🌸🌅",
        "Spring_Morning": "🌼☀️",
        "Spring_Afternoon": "🌺🦋",
        "Spring_Dusk": "🌷🌆",
        "Spring_Evening": "🌹🌙",
        "Spring_Night": "🌸✨",
        "Summer_Dawn": "🌻🌅",
        "Summer_Morning": "☀️🌊",
        "Summer_Afternoon": "🏖️☀️",
        "Summer_Dusk": "🌅🍉",
        "Summer_Evening": "🌴🌙",
        "Summer_Night": "🌙⭐",
        "Autumn_Dawn": "🍂🌅",
        "Autumn_Morning": "🍁☀️",
        "Autumn_Afternoon": "🍂🎃",
        "Autumn_Dusk": "🍁🌆",
        "Autumn_Evening": "🍂🌙",
        "Autumn_Night": "🍁✨",
        "Winter_Dawn": "❄️🌅",
        "Winter_Morning": "☃️☀️",
        "Winter_Afternoon": "❄️☁️",
        "Winter_Dusk": "🌨️🌆",
        "Winter_Evening": "❄️🌙",
        "Winter_Night": "❄️✨"
    }
    
    theme_key = f"{season}_{time_of_day}"
    return emojis.get(theme_key, "🌌✨")
