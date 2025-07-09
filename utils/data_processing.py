import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def load_match_data():
    """Load match data from CSV file"""
    csv_path = "data/matches.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    else:
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=[
            'match_id', 'datetime', 'game_mode', 'map_name', 'team', 
            'player_name', 'kills', 'deaths', 'assists', 'score', 
            'weapon', 'ping', 'coins', 'match_length'
        ])

def save_match_data(df):
    """Save match data to CSV file"""
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/matches.csv", index=False)

def get_unique_players(df):
    """Get list of unique players"""
    return sorted(df['player_name'].unique()) if not df.empty else []

def get_unique_weapons(df):
    """Get list of unique weapons"""
    return sorted(df['weapon'].unique()) if not df.empty else []

def get_unique_maps(df):
    """Get list of unique maps"""
    return sorted(df['map_name'].unique()) if not df.empty else []

def get_unique_game_modes(df):
    """Get list of unique game modes"""
    return sorted(df['game_mode'].unique()) if not df.empty else []

def get_next_match_id(df):
    """Get next available match ID"""
    if df.empty:
        return 1
    return df['match_id'].max() + 1

def validate_match_data(match_data):
    """Validate match data before saving"""
    errors = []
    
    for player_data in match_data:
        # Check required fields
        required_fields = ['player_name', 'kills', 'deaths', 'score', 'weapon', 'match_length']
        for field in required_fields:
            if not player_data.get(field) and player_data.get(field) != 0:
                errors.append(f"Missing required field: {field}")
        
        # Check numeric fields
        numeric_fields = ['kills', 'deaths', 'score', 'ping', 'coins', 'match_length']
        for field in numeric_fields:
            if field in player_data and player_data[field] is not None:
                try:
                    float(player_data[field])
                except (ValueError, TypeError):
                    errors.append(f"Invalid numeric value for {field}")
        
        # Check assists for team matches
        if player_data.get('game_mode') == 'Team' and player_data.get('assists') is None:
            errors.append("Assists required for team matches")
    
    return errors

def add_match_to_dataframe(df, match_data):
    """Add new match data to existing dataframe"""
    new_rows = []
    
    for player_data in match_data:
        row = {
            'match_id': player_data['match_id'],
            'datetime': player_data['datetime'],
            'game_mode': player_data['game_mode'],
            'map_name': player_data['map_name'],
            'team': player_data.get('team'),
            'player_name': player_data['player_name'],
            'kills': int(player_data['kills']),
            'deaths': int(player_data['deaths']),
            'assists': int(player_data['assists']) if player_data.get('assists') is not None else None,
            'score': int(player_data['score']),
            'weapon': player_data['weapon'],
            'ping': int(player_data['ping']) if player_data.get('ping') else None,
            'coins': int(player_data['coins']) if player_data.get('coins') else None,
            'match_length': int(player_data['match_length']) if player_data.get('match_length') else None
        }
        new_rows.append(row)
    
    new_df = pd.DataFrame(new_rows)
    return pd.concat([df, new_df], ignore_index=True)

def filter_data_by_date_range(df, start_date, end_date):
    """Filter data by date range"""
    if df.empty:
        return df
    
    mask = (df['datetime'] >= start_date) & (df['datetime'] <= end_date)
    return df[mask]

def filter_data_by_players(df, players):
    """Filter data by selected players"""
    if not players or df.empty:
        return df
    
    return df[df['player_name'].isin(players)]

def filter_data_by_game_mode(df, game_mode):
    """Filter data by game mode"""
    if not game_mode or df.empty:
        return df
    
    return df[df['game_mode'] == game_mode] 