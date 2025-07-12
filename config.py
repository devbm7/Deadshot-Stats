"""
Configuration file for Deadshot Stats App

This file contains configuration settings and instructions for setting up Supabase integration.
"""

import streamlit as st

# Supabase Configuration
def get_supabase_config():
    """Get Supabase configuration from Streamlit secrets"""
    if st.secrets and "supabase" in st.secrets:
        return {
            "url": st.secrets["supabase"]["url"],
            "key": st.secrets["supabase"]["key"],
        }
    return {"url": None, "key": None}

# Gemini API Configuration
def get_gemini_api_key():
    """
    Get Gemini API key from Streamlit secrets.
    """
    if st.secrets and "gemini" in st.secrets:
        return st.secrets["gemini"]["api_key"]
    return None

def check_gemini_config():
    """Check if Gemini API is properly configured"""
    api_key = get_gemini_api_key()
    return api_key is not None and api_key.strip() != ""

def get_gemini_instructions():
    """Return instructions for setting up Gemini API"""
    return """
    ## Gemini API Setup Instructions
    
    To use AI-powered image extraction, follow these steps:
    
    ### 1. Get a Gemini API Key
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Create a new API key
    4. Copy the API key
    
    ### 2. For Streamlit Cloud Deployment
    Add this secret in your Streamlit Cloud dashboard:
    - Go to your app settings
    - Add secrets in the format:
    ```
    [gemini]
    api_key = "your_gemini_api_key_here"
    ```
    
    ### 3. For Local Development
    Create a `.streamlit/secrets.toml` file in your project root with:
    ```
    [gemini]
    api_key = "your_gemini_api_key_here"
    ```
    
    ### 4. Usage
    Once configured, you can upload screenshots and the AI will automatically extract match data.
    """

def show_gemini_status():
    """Show Gemini API connection status"""
    if check_gemini_config():
        st.success("✅ Gemini API is configured and ready to use!")
        return True
    else:
        st.error("❌ Gemini API is not configured")
        
        # Provide more specific debugging information
        st.info("**Debugging Information:**")
        
        # Check if secrets are available
        if st.secrets:
            st.write("✅ Streamlit secrets are available")
            try:
                gemini_secret = st.secrets.get("gemini", {})
                if gemini_secret:
                    st.write("✅ Gemini secret section found")
                    if gemini_secret.get("api_key"):
                        st.write("✅ API key found in secrets")
                    else:
                        st.write("❌ No API key in secrets")
                else:
                    st.write("❌ No Gemini secret section found")
            except Exception as e:
                st.write(f"❌ Error reading secrets: {e}")
        else:
            st.write("❌ No Streamlit secrets available")
        
        st.info("Please set up your Gemini API key to enable AI-powered image extraction.")
        with st.expander("📋 Gemini API Setup Instructions"):
            st.markdown(get_gemini_instructions())
        return False

def check_supabase_config():
    """Check if Supabase is properly configured"""
    config = get_supabase_config()
    if not config["url"] or not config["key"]:
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
    
    ### 3. For Streamlit Cloud Deployment
    Add these secrets in your Streamlit Cloud dashboard:
    - Go to your app settings
    - Add secrets in the format:
    ```
    [supabase]
    url = "your_project_url_here"
    key = "your_anon_key_here"
    ```
    
    ### 4. For Local Development
    Create a `.streamlit/secrets.toml` file in your project root with:
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