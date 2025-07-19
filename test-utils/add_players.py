#!/usr/bin/env python3
"""
Utility script to add new players to the Deadshot Stats system.
This script adds sample matches for new players to populate the system.
"""

import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processing import (
    load_match_data,
    save_match_data,
    get_next_match_id,
    add_match_to_dataframe,
)


def add_sample_matches_for_players(new_players):
    """
    Add sample matches for new players to populate the system.

    Args:
        new_players: List of new player names to add
    """
    print(f"🎮 Adding sample matches for {len(new_players)} new players...")

    # Load existing data
    df = load_match_data()

    # Get the next match ID
    next_match_id = get_next_match_id(df)

    # Create sample matches for each new player
    new_matches = []

    for i, player_name in enumerate(new_players):
        # Create a sample match for each player
        match_data = {
            "match_id": next_match_id + i,
            "datetime": datetime.now() - timedelta(days=len(new_players) - i),
            "game_mode": "FFA",
            "map_name": "City",
            "team": None,
            "player_name": player_name,
            "kills": 15 + (i * 2),  # Vary kills slightly
            "deaths": 8 + (i % 3),  # Vary deaths slightly
            "assists": None,  # FFA mode
            "score": 1500 + (i * 100),
            "weapon": "AK47",
            "ping": 45 + (i * 5),
            "coins": 120 + (i * 20),
            "match_length": 10,
        }
        new_matches.append(match_data)

    # Add matches to dataframe
    for match in new_matches:
        df = add_match_to_dataframe(df, [match])

    # Save the updated data
    save_match_data(df)

    print(f"✅ Added {len(new_matches)} sample matches for new players!")
    print("📊 New players added:")
    for player in new_players:
        print(f"  • {player}")

    return df


def main():
    """Main function to add new players."""
    print("🎯 Deadshot Stats - Add New Players")
    print("=" * 40)

    # List of new players to add
    new_players = ["DevilOHeaven", "MaXiMus22", "Heet63"]

    # You can add more players here
    # new_players.extend([
    #     "Player4",
    #     "Player5",
    #     "Player6"
    # ])

    print(f"📋 Adding {len(new_players)} players to the system...")

    # Add sample matches for new players
    df = add_sample_matches_for_players(new_players)

    print(f"\n✅ Successfully added {len(new_players)} players!")
    print(f"📊 Total players in system: {len(df['player_name'].unique())}")
    print(f"📈 Total matches in system: {len(df['match_id'].unique())}")

    print("\n🚀 You can now run the app:")
    print("streamlit run app.py")

    print("\n💡 The new players will appear in the dropdown menus!")


if __name__ == "__main__":
    main()
