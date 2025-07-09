#!/usr/bin/env python3
"""
Utility script to add sample matches with new maps and weapons.
This script adds sample data to populate the system with all available maps and weapons.
"""

import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processing import load_match_data, save_match_data, get_next_match_id, add_match_to_dataframe

def add_sample_matches_for_maps_weapons():
    """
    Add sample matches to populate the system with all maps and weapons.
    """
    print("🎮 Adding sample matches for all maps and weapons...")
    
    # Load existing data
    df = load_match_data()
    
    # Get the next match ID
    next_match_id = get_next_match_id(df)
    
    # Define all maps and weapons
    maps = ["Refinery", "Factory", "Forest", "Neo Tokyo", "Vineyard", "Snowfall"]
    weapons = ["AR", "SMG", "Sniper", "Shotgun"]
    players = ["DevilOHeaven", "MaXiMus22", "Heet63"]
    
    # Create sample matches for each map and weapon combination
    new_matches = []
    match_id = next_match_id
    
    for map_name in maps:
        for weapon in weapons:
            # Create a sample match for each map-weapon combination
            for i, player_name in enumerate(players):
                match_data = {
                    'match_id': match_id,
                    'datetime': datetime.now() - timedelta(days=len(maps) * len(weapons) - match_id + next_match_id),
                    'game_mode': 'FFA',
                    'map_name': map_name,
                    'team': None,
                    'player_name': player_name,
                    'kills': 10 + (i * 3),  # Vary kills
                    'deaths': 5 + (i * 2),   # Vary deaths
                    'assists': None,  # FFA mode
                    'score': 1000 + (i * 200),
                    'weapon': weapon,
                    'ping': 45 + (i * 5),
                    'coins': 100 + (i * 30),
                    'match_length': 10
                }
                new_matches.append(match_data)
            match_id += 1
    
    # Add matches to dataframe
    for match in new_matches:
        df = add_match_to_dataframe(df, [match])
    
    # Save the updated data
    save_match_data(df)
    
    print(f"✅ Added {len(new_matches)} sample matches!")
    print(f"📊 Maps added: {', '.join(maps)}")
    print(f"🔫 Weapons added: {', '.join(weapons)}")
    
    return df

def main():
    """Main function to add sample matches for maps and weapons."""
    print("🎯 Deadshot Stats - Update Maps and Weapons")
    print("=" * 50)
    
    print("📋 Adding sample matches for all maps and weapons...")
    
    # Add sample matches for maps and weapons
    df = add_sample_matches_for_maps_weapons()
    
    print(f"\n✅ Successfully updated maps and weapons!")
    print(f"📊 Total players in system: {len(df['player_name'].unique())}")
    print(f"🗺️  Total maps in system: {len(df['map_name'].unique())}")
    print(f"🔫 Total weapons in system: {len(df['weapon'].unique())}")
    print(f"📈 Total matches in system: {len(df['match_id'].unique())}")
    
    print("\n🗺️  Available Maps:")
    for map_name in sorted(df['map_name'].unique()):
        print(f"  • {map_name}")
    
    print("\n🔫 Available Weapons:")
    for weapon in sorted(df['weapon'].unique()):
        print(f"  • {weapon}")
    
    print("\n🚀 You can now run the app:")
    print("streamlit run app.py")
    
    print("\n💡 All maps and weapons will appear in the dropdown menus!")

if __name__ == "__main__":
    main() 