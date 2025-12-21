#!/usr/bin/env python3
"""
Initialize Star Collection System Database

This script initializes the database with the star collection tables
and populates the star database with initial stars.
"""

import os
import sys
from database import init_db, SessionLocal, Star
from star_system import (
    STAR_DATABASE,
    calculate_rarity_score,
    get_rarity_tier,
    can_star_chat
)

def initialize_stars():
    """Initialize the star database."""
    print("🌟 Initializing Star Collection System...")
    print("-" * 50)
    
    # Initialize database schema
    print("Creating database tables...")
    try:
        init_db()
        print("✓ Database tables created")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False
    
    # Connect to database
    db = SessionLocal()
    
    try:
        # Check if stars already exist
        existing_count = db.query(Star).count()
        if existing_count > 0:
            print(f"⚠️  {existing_count} stars already exist in database")
            response = input("Do you want to reinitialize? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return True
            
            # Clear existing stars
            db.query(Star).delete()
            db.commit()
            print("✓ Cleared existing stars")
        
        # Add stars
        print(f"\nAdding {len(STAR_DATABASE)} stars to database...")
        stars_added = 0
        
        for star_data in STAR_DATABASE:
            # Calculate initial rarity
            rarity_score = calculate_rarity_score(
                star_data["base_rarity"],
                star_data["category"]
            )
            rarity_tier = get_rarity_tier(rarity_score)
            can_chat_flag, chat_duration = can_star_chat(rarity_tier)
            
            star = Star(
                name=star_data["name"],
                category=star_data["category"],
                rarity=rarity_tier,
                rarity_score=rarity_score,
                color=star_data["color"],
                tone_frequency=star_data["tone_frequency"],
                personality=star_data["personality"],
                can_chat=can_chat_flag,
                chat_duration=chat_duration,
                right_ascension=star_data["right_ascension"],
                declination=star_data["declination"],
                properties={}
            )
            db.add(star)
            stars_added += 1
            print(f"  ✓ Added {star.name} ({star.category}, {star.rarity})")
        
        db.commit()
        print(f"\n✅ Successfully added {stars_added} stars to database!")
        
        # Print summary
        print("\n" + "=" * 50)
        print("Star Collection System Summary")
        print("=" * 50)
        
        categories = {}
        rarities = {}
        
        for star in db.query(Star).all():
            categories[star.category] = categories.get(star.category, 0) + 1
            rarities[star.rarity] = rarities.get(star.rarity, 0) + 1
        
        print("\nBy Category:")
        for category, count in sorted(categories.items()):
            print(f"  {category:12s}: {count}")
        
        print("\nBy Rarity:")
        for rarity, count in sorted(rarities.items(), key=lambda x: ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic"].index(x[0])):
            print(f"  {rarity:12s}: {count}")
        
        print("\n🌌 Star Collection System is ready!")
        print("Users can now collect stars by visiting the Star Finder page.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error initializing stars: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Check if database URL is set
    database_url = os.environ.get("DATABASE_URL")
    if not database_url or database_url == "postgresql://user:password@host:port/database":
        print("⚠️  WARNING: DATABASE_URL environment variable is not properly set!")
        print("Please set DATABASE_URL to your PostgreSQL connection string.")
        print("\nExample:")
        print('export DATABASE_URL="postgresql://username:password@host:5432/dbname"')
        sys.exit(1)
    
    success = initialize_stars()
    sys.exit(0 if success else 1)
