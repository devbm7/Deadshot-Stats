"""
Configuration file for Deadshot Stats App

This file contains configuration settings and instructions for setting up Supabase integration.
"""

import os
import streamlit as st

# Supabase Configuration
SUPABASE_CONFIG = {
    "url": os.getenv("SUPABASE_URL"),
    "key": os.getenv("SUPABASE_KEY"),
}

def check_supabase_config():
    """Check if Supabase is properly configured"""
    if not SUPABASE_CONFIG["url"] or not SUPABASE_CONFIG["key"]:
        return False
    return True

def get_supabase_instructions():
    """Return instructions for setting up Supabase"""
    return """
    ## Supabase Setup Instructions
    
    To use Supabase for data storage, follow these steps:
    
    ### 1. Create a Supabase Project
    1. Go to [supabase.com](https://supabase.com)
    2. Sign up/Login and create a new project
    3. Wait for the project to be ready
    
    ### 2. Get Your Credentials
    1. Go to Settings → API in your Supabase dashboard
    2. Copy the "Project URL" and "anon public" key
    
    ### 3. Set Environment Variables
    Create a `.env` file in your project root with:
    ```
    SUPABASE_URL=your_project_url_here
    SUPABASE_KEY=your_anon_key_here
    ```
    
    ### 4. For Streamlit Cloud Deployment
    Add these secrets in your Streamlit Cloud dashboard:
    - Go to your app settings
    - Add secrets in the format:
    ```
    [supabase]
    url = "your_project_url_here"
    key = "your_anon_key_here"
    ```
    
    ### 5. Create the Database Table
    Run this SQL in your Supabase SQL editor:
    ```sql
    create table public.matches (
      id bigint generated always as identity not null,
      match_id integer not null,
      datetime timestamp with time zone not null,
      game_mode text not null,
      map_name text not null,
      team text null,
      player_name text not null,
      kills integer null,
      deaths integer null,
      assists integer null,
      score integer null,
      weapon text null,
      ping integer null,
      coins integer null,
      match_length integer null,
      created_at timestamp with time zone not null default now(),
      constraint matches_pkey primary key (id)
    );

    create index IF not exists idx_matches_match_id on public.matches using btree (match_id);
    create index IF not exists idx_matches_player_name on public.matches using btree (player_name);
    create index IF not exists idx_matches_datetime on public.matches using btree (datetime);
    ```
    
    ### 6. Set Row Level Security (Optional but Recommended)
    ```sql
    -- Enable RLS
    alter table public.matches enable row level security;
    
    -- Create policy to allow all operations (for demo purposes)
    create policy "Allow all operations" on public.matches for all using (true);
    ```
    """

def show_supabase_status():
    """Show Supabase connection status"""
    if check_supabase_config():
        st.success("✅ Supabase is configured and ready to use!")
        return True
    else:
        st.error("❌ Supabase is not configured")
        st.info("Please set up your Supabase credentials to enable cloud storage.")
        with st.expander("📋 Supabase Setup Instructions"):
            st.markdown(get_supabase_instructions())
        return False 