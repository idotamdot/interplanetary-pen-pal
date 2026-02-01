# ======================================
#  DATABASE SETUP
# ======================================

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@host:port/database")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------------
#  DATABASE MODELS
# -------------------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    is_premium = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    star_name = Column(String)
    symbol = Column(String)
    dream = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    age = Column(Integer)  # User's age for adaptive content
    user = relationship("User", back_populates="profile")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipient_type = Column(String)
    elemental_tone = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Echo(Base):
    __tablename__ = "echoes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DreamSeed(Base):
    __tablename__ = "dream_seeds"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Star(Base):
    __tablename__ = "stars"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # Cosmic, Elemental, Mystical, Ancient, Celestial
    rarity = Column(String)  # Common, Uncommon, Rare, Epic, Legendary, Mythic
    rarity_score = Column(Float)
    color = Column(String)
    tone_frequency = Column(Float)
    personality = Column(Text)
    can_chat = Column(Boolean, default=False)
    chat_duration = Column(Integer)  # seconds
    right_ascension = Column(Float)
    declination = Column(Float)
    properties = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class CollectedStar(Base):
    __tablename__ = "collected_stars"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    star_id = Column(Integer, ForeignKey("stars.id"))
    collected_at = Column(DateTime, default=datetime.utcnow)
    encounter_location_lat = Column(Float)
    encounter_location_lon = Column(Float)
    star = relationship("Star")

class StarNote(Base):
    __tablename__ = "star_notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    star_id = Column(Integer, ForeignKey("stars.id"))
    content = Column(Text)
    note_type = Column(String)  # poem, wisdom, insight, uplifting
    color = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    star = relationship("Star")

class StarInteraction(Base):
    __tablename__ = "star_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    star_id = Column(Integer, ForeignKey("stars.id"))
    interaction_type = Column(String)  # encounter, chat, trade
    metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    star = relationship("Star")

# -------------------------------
# DIPLOMATIC ACADEMY MODELS
# -------------------------------

class DiplomaticProgress(Base):
    """Tracks user progress in the Diplomatic Academy"""
    __tablename__ = "diplomatic_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    perspective_exercises = Column(Integer, default=0)
    council_consults = Column(Integer, default=0)
    bridge_uses = Column(Integer, default=0)
    scenarios_completed = Column(Integer, default=0)
    perspectives_understood = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    achievements = Column(JSON, default=list)  # List of earned achievement keys
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DiplomaticExercise(Base):
    """Records individual diplomatic exercises completed by users"""
    __tablename__ = "diplomatic_exercises"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_type = Column(String)  # scenario, council, bridge, meditation
    scenario_title = Column(String)
    user_response = Column(Text)
    ai_feedback = Column(Text)
    council_members = Column(JSON)  # List of council members who participated
    age_profile_used = Column(String)  # young_explorer, teen_navigator, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)

# -------------------------------
# DATABASE INITIALIZATION
# -------------------------------

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
