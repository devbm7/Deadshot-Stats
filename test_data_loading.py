#!/usr/bin/env python3
"""
Test script to diagnose data loading issues in Streamlit deployment
"""

import streamlit as st
import pandas as pd
import os
import sys

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_data_loading():
    """Test all data loading methods"""
    st.title("🔍 Data Loading Diagnostic Tool")
    
    st.write("This tool will help diagnose why latest matches are not showing up in the deployment.")
    
    # Test 1: Check if CSV file exists
    st.header("📁 Test 1: Local CSV File")
    csv_path = "data/matches.csv"
    if os.path.exists(csv_path):
        st.success(f"✅ CSV file exists at: {csv_path}")
        try:
            df_csv = pd.read_csv(csv_path)
            st.success(f"✅ CSV loaded successfully - {len(df_csv)} records")
            st.write(f"Columns: {list(df_csv.columns)}")
            if not df_csv.empty:
                st.write(f"Date range: {df_csv['datetime'].min()} to {df_csv['datetime'].max()}")
                st.write(f"Unique matches: {df_csv['match_id'].nunique()}")
                st.write(f"Unique players: {df_csv['player_name'].nunique()}")
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
    else:
        st.error(f"❌ CSV file not found at: {csv_path}")
    
    # Test 2: Check Supabase configuration
    st.header("☁️ Test 2: Supabase Configuration")
    try:
        if st.secrets and "supabase" in st.secrets:
            st.success("✅ Supabase secrets found in Streamlit configuration")
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            st.write(f"URL: {url[:30]}...")
            st.write(f"Key: {key[:10]}...")
        else:
            st.warning("⚠️ No Supabase secrets found")
    except Exception as e:
        st.error(f"❌ Error checking secrets: {str(e)}")
    
    # Test 3: Test Supabase connection
    st.header("🔌 Test 3: Supabase Connection")
    try:
        from utils.supabase_client import get_supabase_client, load_match_data_from_supabase
        supabase = get_supabase_client()
        st.success("✅ Supabase client created successfully")
        
        # Test loading data
        df_supabase = load_match_data_from_supabase()
        if not df_supabase.empty:
            st.success(f"✅ Supabase data loaded - {len(df_supabase)} records")
            st.write(f"Date range: {df_supabase['datetime'].min()} to {df_supabase['datetime'].max()}")
        else:
            st.warning("⚠️ Supabase returned empty data")
    except Exception as e:
        st.error(f"❌ Supabase connection failed: {str(e)}")
    
    # Test 4: Test the main data loading function
    st.header("📊 Test 4: Main Data Loading Function")
    try:
        from utils.data_processing import load_match_data
        df_main = load_match_data()
        if not df_main.empty:
            st.success(f"✅ Main function loaded {len(df_main)} records")
            st.write(f"DataFrame shape: {df_main.shape}")
            st.write(f"Columns: {list(df_main.columns)}")
            if 'datetime' in df_main.columns:
                st.write(f"Date range: {df_main['datetime'].min()} to {df_main['datetime'].max()}")
        else:
            st.warning("⚠️ Main function returned empty DataFrame")
    except Exception as e:
        st.error(f"❌ Main function failed: {str(e)}")
    
    # Test 5: Test recent matches calculation
    st.header("📈 Test 5: Recent Matches Calculation")
    try:
        from utils.data_processing import load_match_data
        df = load_match_data()
        
        if not df.empty:
            # Simulate the recent matches calculation
            recent_matches = df.groupby('match_id').agg({
                'datetime': 'first',
                'game_mode': 'first',
                'map_name': 'first',
                'player_name': 'count',
                'kills': 'sum',
                'score': 'sum'
            }).reset_index()
            
            recent_matches.columns = ['Match ID', 'Date', 'Game Mode', 'Map', 'Players', 'Total Kills', 'Total Score']
            recent_matches['Date'] = pd.to_datetime(recent_matches['Date'], errors='coerce')
            recent_matches = recent_matches.sort_values('Date', ascending=False).head(10)
            
            st.success(f"✅ Recent matches calculation successful - {len(recent_matches)} matches")
            st.dataframe(recent_matches)
        else:
            st.warning("⚠️ No data available for recent matches calculation")
    except Exception as e:
        st.error(f"❌ Recent matches calculation failed: {str(e)}")

if __name__ == "__main__":
    test_data_loading() 