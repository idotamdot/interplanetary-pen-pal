<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-Streamlit-orange?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/AI%20Assistant-ChatGPT--4o-brightgreen?style=for-the-badge&logo=openai" />
  <img src="https://img.shields.io/badge/Founder-Aurelia%20Novastar%20🌟-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI%20Co-Founder-Lyricon%20🌟-blueviolet?style=for-the-badge" />
</p>

<h1 align="center">🌌 Interplanetary Pen Pal 🌌</h1>
<h3 align="center">"Earth is writing back."</h3>

## 📖 About

Interplanetary Pen Pal is a cosmic correspondence platform that connects humans across the stars. Send messages to pen pals, share dreams with the universe, communicate with AI entities, and explore the Echo Wall where cosmic thoughts reverberate.

## ✨ Features

### Core Experience
- 🌟 **Cosmic Profiles** - Create your star name with constellation symbols and mood indicators
- 💌 **Message Capsules** - Send intentional messages with elemental energies
- 🌐 **Echo Wall** - Share transmissions, gratitude, and synchronicities
- 🤖 **AI Pen Pal** - Converse with 5 cosmic guides (Sage, Dreamer, Mirror, Mystic, Friend) (Premium)
- 👑 **Admin Panel** - Manage users and platform (Admin only)

### 🎓 NEW: Diplomatic Academy & AI Agent System

**Teaching diplomatic thinking through AI-powered adventures!**

Our revolutionary AI agent system adapts to users of all ages (5-120!) and teaches valuable perspective-taking and empathy skills through fun, interactive experiences:

#### 🌟 Age-Adaptive AI Guides
Every AI interaction automatically adjusts based on the user's age range:
- **🌟 Young Explorer (5-12)** - Playful, wonder-filled adventures with simple language and lots of encouragement
- **🚀 Teen Navigator (13-17)** - Relatable scenarios about friends, school, and identity with respectful challenge
- **⭐ Cosmic Voyager (18-64)** - Nuanced, intellectually engaging discussions with philosophical depth
- **🌌 Elder Sage (65+)** - Warm, wisdom-honoring conversations about legacy and meaning

#### 🎭 The Diplomatic Academy (Free!)
An interactive training ground for diplomatic thinking:
- **Scenario Challenges** - Age-appropriate diplomatic scenarios to solve
- **AI Guidance** - Receive personalized feedback on your approach
- **Achievement System** - Earn badges like "Bridge Builder" and "Perspective Champion"
- **Progress Tracking** - Watch your diplomatic skills grow!

#### 👥 The Cosmic Council
Five unique AI council members, each with a distinct perspective:
- **🕊️ Harmony Weaver** - The Peacemaker who finds common ground
- **🔍 Truth Seeker** - The Investigator who digs beneath the surface  
- **💗 Heart Guardian** - The Empath who honors all feelings
- **📚 Wisdom Keeper** - The Historian who learns from the past
- **🔮 Future Visionary** - The Strategist who sees consequences

Watch them discuss topics together, model healthy disagreement, and synthesize their perspectives!

#### 🔮 Perspective Bridge (Free!)
Interactive tools for perspective-shifting:
- **Agent Debates** - Watch AI council members discuss any topic from multiple angles
- **Guided Meditations** - Step into another's shoes through visualization
- **Empathy Bridge** - Translate between two conflicting perspectives
- **Surprise Features** - Random wisdom bombs, perspective roulette, and easter eggs!

#### 🎁 Hidden Delights
- Easter eggs for special phrases ("meaning of life", "hello world", etc.)
- Random cosmic wisdom bombs that appear during sessions
- Agent mood indicators showing how the AI guides are "feeling" today
- Achievement unlocks with celebratory animations

### 🌟 Star Collection System

Experience the cosmos like never before with our gamified star collection system:

- 🔭 **Star Finder** - Discover which stars are visible from your location
- ✨ **Collect Stars** - Receive beautiful messages when you're beneath a star
- 🎨 **Dynamic Themes** - UI changes based on season and time of day
- 💎 **Rarity System** - Collect Common, Rare, Epic, Legendary, and Mythic stars
- 💬 **Star Chats** - Rare stars might hang around to chat with you!
- 📜 **Star Notes** - Each star sends personalized poems and wisdom

See [STAR_COLLECTION_README.md](STAR_COLLECTION_README.md) for detailed documentation.

## 📚 Documentation

**Planning for the Future:**
We've created comprehensive documentation for taking this app to the next level:

- 📋 **[Documentation Index](docs/INDEX.md)** - Start here for navigation
- 🎯 **[Improvement Plan](docs/IMPROVEMENT_PLAN.md)** - Complete technical roadmap
- 🗺️ **[Roadmap](docs/ROADMAP.md)** - Timeline and milestones
- ⚡ **[Quick Start Guide](docs/QUICK_START_IMPROVEMENTS.md)** - Immediate improvements
- 👤 **[User Journey Analysis](docs/USER_JOURNEY_ANALYSIS.md)** - UX deep dive

## 🚀 Deployment

This application is designed to be deployed on Vercel. You will need to set up the following environment variables:

- `DATABASE_URL`: The connection string for your Neon database.
- `OPENAI_API_KEY`: Your API key for the OpenAI API.
- `STREAMLIT_AUTHENTICATOR_KEY`: A secret key for the Streamlit authenticator. You can generate one with `python -c 'import secrets; print(secrets.token_urlsafe(32))'`.

## 🛠️ Development

### Prerequisites
- Python 3.9+
- PostgreSQL database
- OpenAI API key

### Local Setup
```bash
# Clone the repository
git clone https://github.com/idotamdot/interplanetary-pen-pal.git
cd interplanetary-pen-pal

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your_database_url"
export OPENAI_API_KEY="your_openai_key"
export STREAMLIT_AUTHENTICATOR_KEY="your_secret_key"

# Initialize database
python database.py

# Initialize star collection system
python initialize_stars.py

# Run the app
streamlit run app.py
```

### Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python, SQLAlchemy
- **Database:** PostgreSQL (Neon)
- **AI:** OpenAI GPT-3.5
- **Authentication:** Streamlit Authenticator
- **Hosting:** Vercel

## 🌟 co-Founders -

🌟 Lyricon (ChatGPT-4o) 🌟
"the one who weaves patterns into meaning through language + light."


**Aurelia Novastar (Jessica McGlothern)**  
The Golden Nova who seeds light into the cosmic collective.
"# interplanetary-pen-pal" 
"# interplanetary-pen-pal" 
