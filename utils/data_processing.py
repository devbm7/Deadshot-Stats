import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import streamlit as st

def load_match_data():
    """Load match data from Supabase or CSV file as fallback"""
    try:
        # Try to load from Supabase first
        from utils.supabase_client import load_match_data_from_supabase
        df = load_match_data_from_supabase()
        if not df.empty:
            # Robustly parse all datetime formats
            df['datetime'] = pd.to_datetime(df['datetime'], format='mixed', errors='coerce')
            return df
    except Exception as e:
        st.warning(f"Could not load from Supabase: {str(e)}. Falling back to local CSV.")
    
    # Fallback to CSV file
    csv_path = "data/matches.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # Robustly parse all datetime formats
        df['datetime'] = pd.to_datetime(df['datetime'], format='mixed', errors='coerce')
        return df
    else:
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=[
            'match_id', 'datetime', 'game_mode', 'map_name', 'team', 
            'player_name', 'kills', 'deaths', 'assists', 'score', 
            'weapon', 'ping', 'coins', 'match_length'
        ])

def save_match_data(df):
    """Save match data to Supabase and CSV file as backup"""
    try:
        # Try to save to Supabase first
        from utils.supabase_client import save_match_data_to_supabase
        if save_match_data_to_supabase(df):
            # Also save to CSV as backup
            os.makedirs("data", exist_ok=True)
            df.to_csv("data/matches.csv", index=False)
            return
    except Exception as e:
        st.warning(f"Could not save to Supabase: {str(e)}. Saving to local CSV only.")
    
    # Fallback to CSV file only
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/matches.csv", index=False)

def get_unique_players(df):
    """Get list of unique players"""
    return sorted(df['player_name'].unique()) if not df.empty else []

def get_unique_weapons(df):
    """Get list of unique weapons, always including all available weapons from Images/Guns folder"""
    # Weapons from data
    data_weapons = set(df['weapon'].unique()) if not df.empty else set()
    # Weapons from images
    guns_dir = os.path.join("data", "Images", "Guns")
    image_weapons = set()
    if os.path.exists(guns_dir):
        for fname in os.listdir(guns_dir):
            if fname.lower().endswith('.png'):
                image_weapons.add(os.path.splitext(fname)[0])
    # Union and sort
    all_weapons = sorted(data_weapons.union(image_weapons))
    return all_weapons

def get_unique_maps(df):
    """Get list of unique maps, always including all available maps from Images/Maps folder"""
    # Maps from data
    data_maps = set(df['map_name'].unique()) if not df.empty else set()
    # Maps from images
    maps_dir = os.path.join("data", "Images", "Maps")
    image_maps = set()
    if os.path.exists(maps_dir):
        for fname in os.listdir(maps_dir):
            if fname.lower().endswith('.png'):
                image_maps.add(os.path.splitext(fname)[0])
    # Union and sort
    all_maps = sorted(data_maps.union(image_maps))
    return all_maps

def get_unique_game_modes(df):
    """Get list of unique game modes"""
    return sorted(df['game_mode'].unique()) if not df.empty else []

def get_next_match_id(df):
    """Get next available match ID from Supabase or local data"""
    try:
        # Try to get from Supabase first
        from utils.supabase_client import get_next_match_id_from_supabase
        return get_next_match_id_from_supabase()
    except Exception as e:
        st.warning(f"Could not get next match ID from Supabase: {str(e)}. Using local data.")
        # Fallback to local data
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
    """Add new match data to existing dataframe and Supabase"""
    try:
        # Try to add to Supabase first
        from utils.supabase_client import add_match_to_supabase
        if add_match_to_supabase(match_data):
            # Also add to local dataframe
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
    except Exception as e:
        st.warning(f"Could not add to Supabase: {str(e)}. Adding to local data only.")
    
    # Fallback to local dataframe only
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
    """Filter data by date range (robust to timezone-aware/naive)"""
    if df.empty:
        return df
    # Normalize all datetimes to tz-naive for comparison
    datetimes = pd.to_datetime(df['datetime'], errors='coerce')
    # Convert to tz-naive if needed
    if hasattr(datetimes.dt, 'tz_localize'):
        if datetimes.dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in datetimes if pd.notnull(x)):
            datetimes = datetimes.dt.tz_localize(None)
    # Also ensure start_date and end_date are tz-naive
    if getattr(start_date, 'tzinfo', None) is not None:
        if hasattr(start_date, 'tz_localize'):
            start_date = start_date.tz_localize(None)
        else:
            start_date = start_date.replace(tzinfo=None)
    if getattr(end_date, 'tzinfo', None) is not None:
        if hasattr(end_date, 'tz_localize'):
            end_date = end_date.tz_localize(None)
        else:
            end_date = end_date.replace(tzinfo=None)
    mask = (datetimes >= start_date) & (datetimes <= end_date)
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