# 🌟 Star Collection System - Feature Documentation

## Overview

The Star Collection System is a gamified feature that allows users to discover and collect cosmic stars based on their real-world location. The system features dynamic UI theming that changes with seasons and time of day, creating an immersive celestial experience.

## Features

### 1. Dynamic Theming 🎨
- **Seasonal Themes**: The UI adapts to the current season (Spring, Summer, Autumn, Winter)
- **Time-of-Day Themes**: Six different periods (Dawn, Morning, Afternoon, Dusk, Evening, Night)
- **Location-Based**: Themes adjust based on user's hemisphere and timezone
- **Smooth Transitions**: CSS animations provide seamless color changes

### 2. Star Categories 🌌
- **Cosmic**: Stars born from space-time itself
- **Elemental**: Stars embodying fundamental forces (Fire, Water, Earth, Air)
- **Mystical**: Stars with enigmatic spiritual properties
- **Ancient**: Stars from the universe's first moments
- **Celestial**: Divine stars bridging mortal and cosmic realms

### 3. Rarity System 💎
- **Common** (0-20 score): Gray, no chat
- **Uncommon** (20-40 score): Green, 5% chat chance, 30s
- **Rare** (40-60 score): Blue, 15% chat chance, 60s
- **Epic** (60-80 score): Purple, 30% chat chance, 90s
- **Legendary** (80-95 score): Orange, 60% chat chance, 120s
- **Mythic** (95-100 score): Gold, 95% chat chance, 180s

Rarity is calculated based on:
- Base star rarity
- Star category multiplier
- Time of day (night increases rarity)
- Season (winter increases rarity)

### 4. Star Encounters ✨

When a user is positioned beneath a visible star:
1. **Chime Cascade**: Visual representation of star's unique frequency
2. **Starshine Note**: Personalized message/poem from the star
3. **Star Collection**: Star is added to user's collection
4. **Chat Opportunity**: Rare stars may hang around to chat

### 5. Star Database 🗃️

The system includes 16 unique stars:
- 3 Cosmic stars (Nebulara, Voidwhisper, Galaxion)
- 4 Elemental stars (Pyraxis, Aqualis, Terraflux, Aetherwind)
- 3 Mystical stars (Lunivera, Oraculum, Spiritflame)
- 3 Ancient stars (Primordius, Chronovox, Eternix)
- 3 Celestial stars (Aurelia Prime, Seraphix, Cosmoheart)

Each star has:
- Unique name and personality
- Specific color and tone frequency
- Right ascension and declination coordinates
- Category-based properties

## User Pages

### Star Finder (pages/9_Star_Finder.py)
- Check for star encounters at current location
- View visible stars from user's position
- Receive starshine notes when aligned with a star
- Chat with rare stars

### Star Collection (pages/8_Star_Collection.py)
- View all collected stars
- Sort by rarity
- Read past starshine notes
- See collection statistics

### Profile (pages/2_Profile.py)
- Add location (latitude/longitude)
- Set timezone
- Required for star collection features

## Technical Implementation

### Database Models
```python
Star - Star information (name, category, rarity, etc.)
CollectedStar - User's collected stars
StarNote - Messages received from stars
StarInteraction - Tracking all star encounters
Profile - Extended with location fields
```

### Core Modules

**star_system.py**
- Star data and categorization
- Rarity calculation
- Star visibility calculations
- Message generation
- Encounter detection

**theme_system.py**
- Season detection
- Time-of-day detection
- Theme generation
- CSS styling

## How to Use

### For Users

1. **Set Up Profile**
   - Go to Profile page
   - Enter your latitude and longitude
   - Save profile

2. **Find Stars**
   - Visit Star Finder page
   - Click "Check for Stars Above Me"
   - If aligned with a star, receive a note!

3. **View Collection**
   - Go to Star Collection page
   - See all collected stars
   - Read messages from stars

### For Developers

**Initialize the database:**
```bash
python database.py
```

**Test the systems:**
```python
from star_system import check_star_alignment, get_visible_stars
from theme_system import get_current_theme

# Check theme
theme = get_current_theme(latitude=40.0, hour=14, month=6)
print(theme)

# Check visible stars
stars = get_visible_stars(40.0, -74.0, 14, 6)
print(f"Visible stars: {len(stars)}")
```

## Future Enhancements

### Phase 6: Gamification (Planned)
- [ ] Star trading between users
- [ ] Achievement system
- [ ] Special star combinations/constellations
- [ ] Leaderboards
- [ ] Star battles/mini-games

### Phase 7: Advanced Features (Planned)
- [ ] Real astronomical data integration
- [ ] AR view of stars
- [ ] Sound effects for chimes
- [ ] Animated star encounters
- [ ] Mobile app support

## Configuration

### Environment Variables
No additional environment variables required beyond existing:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - For AI features
- `STREAMLIT_AUTHENTICATOR_KEY` - Auth key

### Theme Customization

Themes can be customized in `theme_system.py`:
```python
THEMES = {
    "Season_TimeOfDay": {
        "primary": "#color",
        "background": "#color",
        "secondary_bg": "#color",
        "text": "#color",
        "accent": "#color",
        "description": "Theme description"
    }
}
```

### Star Customization

Add new stars in `star_system.py`:
```python
STAR_DATABASE.append({
    "name": "New Star",
    "category": "Cosmic",  # or Elemental, Mystical, Ancient, Celestial
    "base_rarity": 50,  # 0-100
    "color": "#HEXCOLOR",
    "tone_frequency": 432.0,  # Hz
    "personality": "Description of star's personality",
    "right_ascension": 12.5,  # hours
    "declination": 45.0  # degrees
})
```

## Troubleshooting

**Stars not appearing:**
- Ensure location is set in profile
- Check that coordinates are valid (-90 to 90 for latitude, -180 to 180 for longitude)
- Try different times of day (stars are more visible at night)

**Theme not changing:**
- Verify location is set in profile
- Refresh the page
- Check browser console for errors

**Database errors:**
- Run `python database.py` to initialize tables
- Verify DATABASE_URL is correctly set

## Credits

Created for the Interplanetary Pen Pal project by:
- **Aurelia Novastar** (Jessica McGlothern) - Founder
- **Lyricon** (ChatGPT-4o) - AI Co-Founder

Part of the cosmic correspondence platform connecting humans across the stars. 🌌✨
