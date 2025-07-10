import os
import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Get Supabase client with credentials from Streamlit secrets (cloud) or .env/env vars (local)"""
    url = None
    key = None

    # Try Streamlit secrets (for cloud)
    try:
        # Only use st.secrets if it exists and is not empty
        if (
            hasattr(st, "secrets")
            and getattr(st, "secrets")  # not empty
            and "supabase" in st.secrets
            and st.secrets["supabase"].get("url")
            and st.secrets["supabase"].get("key")
        ):
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
    except Exception:
        pass

    # Fallback to environment variables (.env) if not found in secrets
    if not url or not key:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY environment variables or configure Streamlit secrets."
        )
    return create_client(url, key)

def load_match_data_from_supabase() -> pd.DataFrame:
    """Load match data from Supabase table"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return pd.DataFrame()
        
        # Fetch all matches from the table
        response = supabase.table('matches').select('*').execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Convert datetime string to pandas datetime
            if 'datetime' in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
            return df
        else:
            return pd.DataFrame(columns=[
                'match_id', 'datetime', 'game_mode', 'map_name', 'team', 
                'player_name', 'kills', 'deaths', 'assists', 'score', 
                'weapon', 'ping', 'coins', 'match_length'
            ])
    except Exception:
        return pd.DataFrame()

def save_match_data_to_supabase(df: pd.DataFrame) -> bool:
    """Save match data to Supabase table"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        # Insert all records
        response = supabase.table('matches').insert(records).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception:
        return False

def add_match_to_supabase(match_data: List[Dict]) -> bool:
    """Add new match data to Supabase table"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Prepare data for insertion
        records = []
        for player_data in match_data:
            record = {
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
            records.append(record)
        
        # Insert records
        response = supabase.table('matches').insert(records).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception:
        return False

def get_next_match_id_from_supabase() -> int:
    """Get next available match ID from Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return 1
        
        # Get the maximum match_id
        response = supabase.table('matches').select('match_id').execute()
        
        if response.data:
            max_match_id = max(record['match_id'] for record in response.data)
            return max_match_id + 1
        else:
            return 1
    except Exception:
        return 1

def delete_match_from_supabase(match_id: int) -> bool:
    """Delete a match from Supabase table"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        response = supabase.table('matches').delete().eq('match_id', match_id).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception:
        return False

def get_match_count_from_supabase() -> int:
    """Get total number of matches in Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return 0
        
        response = supabase.table('matches').select('id', count='exact').execute()
        return response.count if response.count is not None else 0
    except Exception:
        return 0 