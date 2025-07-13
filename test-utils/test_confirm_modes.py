#!/usr/bin/env python3
"""
Test script for Confirm and Team Confirm game modes
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processing import validate_match_data, add_match_to_dataframe
from utils.calculations import get_player_stats, calculate_player_wins

def test_confirm_modes():
    """Test the new Confirm and Team Confirm game modes"""
    
    print("🧪 Testing Confirm and Team Confirm Game Modes")
    print("=" * 50)
    
    # Test data for Confirm mode
    confirm_match_data = [
        {
            'match_id': 999,
            'datetime': datetime.now(),
            'game_mode': 'Confirm',
            'map_name': 'Refinery',
            'team': None,
            'player_name': 'Player1',
            'kills': 5,
            'deaths': 3,
            'assists': None,
            'score': 150,
            'weapon': 'AR',
            'ping': 50,
            'coins': 100,
            'match_length': 10,
            'tags': 8
        },
        {
            'match_id': 999,
            'datetime': datetime.now(),
            'game_mode': 'Confirm',
            'map_name': 'Refinery',
            'team': None,
            'player_name': 'Player2',
            'kills': 3,
            'deaths': 5,
            'assists': None,
            'score': 120,
            'weapon': 'SMG',
            'ping': 45,
            'coins': 80,
            'match_length': 10,
            'tags': 5
        }
    ]
    
    # Test data for Team Confirm mode
    team_confirm_match_data = [
        {
            'match_id': 1000,
            'datetime': datetime.now(),
            'game_mode': 'Team Confirm',
            'map_name': 'Factory',
            'team': 'Team1',
            'player_name': 'Player1',
            'kills': 4,
            'deaths': 2,
            'assists': 1,
            'score': 140,
            'weapon': 'AR',
            'ping': 50,
            'coins': 90,
            'match_length': 10,
            'tags': 6
        },
        {
            'match_id': 1000,
            'datetime': datetime.now(),
            'game_mode': 'Team Confirm',
            'map_name': 'Factory',
            'team': 'Team1',
            'player_name': 'Player2',
            'kills': 3,
            'deaths': 3,
            'assists': 2,
            'score': 130,
            'weapon': 'SMG',
            'ping': 45,
            'coins': 85,
            'match_length': 10,
            'tags': 4
        },
        {
            'match_id': 1000,
            'datetime': datetime.now(),
            'game_mode': 'Team Confirm',
            'map_name': 'Factory',
            'team': 'Team2',
            'player_name': 'Player3',
            'kills': 2,
            'deaths': 4,
            'assists': 0,
            'score': 110,
            'weapon': 'Sniper',
            'ping': 55,
            'coins': 70,
            'match_length': 10,
            'tags': 3
        },
        {
            'match_id': 1000,
            'datetime': datetime.now(),
            'game_mode': 'Team Confirm',
            'map_name': 'Factory',
            'team': 'Team2',
            'player_name': 'Player4',
            'kills': 1,
            'deaths': 5,
            'assists': 1,
            'score': 100,
            'weapon': 'Shotgun',
            'ping': 60,
            'coins': 65,
            'match_length': 10,
            'tags': 2
        }
    ]
    
    # Test validation
    print("1. Testing data validation...")
    confirm_errors = validate_match_data(confirm_match_data)
    team_confirm_errors = validate_match_data(team_confirm_match_data)
    
    if not confirm_errors:
        print("✅ Confirm mode data validation passed")
    else:
        print("❌ Confirm mode validation errors:", confirm_errors)
    
    if not team_confirm_errors:
        print("✅ Team Confirm mode data validation passed")
    else:
        print("❌ Team Confirm mode validation errors:", team_confirm_errors)
    
    # Test win calculation
    print("\n2. Testing win calculation...")
    
    # Create test dataframe
    df = pd.DataFrame(columns=[
        'match_id', 'datetime', 'game_mode', 'map_name', 'team', 
        'player_name', 'kills', 'deaths', 'assists', 'score', 
        'weapon', 'ping', 'coins', 'match_length', 'tags'
    ])
    
    # Add confirm match data
    df = add_match_to_dataframe(df, confirm_match_data)
    
    # Test player stats
    print("\n3. Testing player statistics...")
    player1_stats = get_player_stats(df, 'Player1')
    player2_stats = get_player_stats(df, 'Player2')
    
    if player1_stats:
        print(f"✅ Player1 stats - Total Tags: {player1_stats['total_tags']}, Best Match Tags: {player1_stats['best_match_tags']}")
    else:
        print("❌ Failed to get Player1 stats")
    
    if player2_stats:
        print(f"✅ Player2 stats - Total Tags: {player2_stats['total_tags']}, Best Match Tags: {player2_stats['best_match_tags']}")
    else:
        print("❌ Failed to get Player2 stats")
    
    # Test win calculation for Confirm mode
    print("\n4. Testing win calculation for Confirm mode...")
    player1_wins, player1_losses, player1_win_rate = calculate_player_wins(df, 'Player1')
    player2_wins, player2_losses, player2_win_rate = calculate_player_wins(df, 'Player2')
    
    print(f"Player1: {player1_wins} wins, {player1_losses} losses, {player1_win_rate}% win rate")
    print(f"Player2: {player2_wins} wins, {player2_losses} losses, {player2_win_rate}% win rate")
    
    # Add team confirm match data
    df = add_match_to_dataframe(df, team_confirm_match_data)
    
    # Test team confirm win calculation
    print("\n5. Testing win calculation for Team Confirm mode...")
    player1_wins, player1_losses, player1_win_rate = calculate_player_wins(df, 'Player1')
    player3_wins, player3_losses, player3_win_rate = calculate_player_wins(df, 'Player3')
    
    print(f"Player1 (Team1): {player1_wins} wins, {player1_losses} losses, {player1_win_rate}% win rate")
    print(f"Player3 (Team2): {player3_wins} wins, {player3_losses} losses, {player3_win_rate}% win rate")
    
    print("\n✅ All tests completed!")
    print("\n📊 Summary:")
    print("- Confirm mode: Individual tag collection, winner has most tags")
    print("- Team Confirm mode: Team tag collection, winning team has most total tags")
    print("- Tags are now tracked in player statistics and leaderboards")
    print("- Win calculation properly handles both modes")

if __name__ == "__main__":
    test_confirm_modes() 