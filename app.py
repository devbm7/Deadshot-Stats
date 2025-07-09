import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processing import (
    load_match_data, save_match_data, get_unique_players, get_unique_weapons,
    get_unique_maps, get_unique_game_modes, get_next_match_id, validate_match_data,
    add_match_to_dataframe, filter_data_by_date_range, filter_data_by_players,
    filter_data_by_game_mode
)
from utils.calculations import (
    get_player_stats, get_team_stats, get_leaderboard_data, get_weapon_stats,
    get_map_stats, get_recent_activity, get_match_summary
)
from utils.visualizations import (
    create_overview_cards, create_kd_leaderboard_chart, create_player_performance_trend,
    create_weapon_usage_chart, create_map_performance_chart, create_team_performance_chart,
    create_player_comparison_radar, create_match_timeline, create_ping_impact_chart
)

# Page configuration
st.set_page_config(
    page_title="Deadshot Stats Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'match_data' not in st.session_state:
    st.session_state.match_data = load_match_data()

# Sidebar navigation
st.sidebar.title("🎯 Deadshot Stats")
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Dashboard", "📊 Player Analysis", "👥 Team Analysis", "📈 Match History", 
     "🎮 Data Input", "🔧 Advanced Analytics", "📋 Leaderboards"]
)

# Load data
df = st.session_state.match_data

# Dashboard Page
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">Deadshot Stats Dashboard</h1>', unsafe_allow_html=True)
    
    # Overview cards
    overview_stats = create_overview_cards(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Matches</h3>
            <h2>{overview_stats['total_matches']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Kills</h3>
            <h2>{overview_stats['total_kills']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active Players</h3>
            <h2>{overview_stats['total_players']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Avg K/D Ratio</h3>
            <h2>{overview_stats['avg_kd_ratio']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    recent_activity = get_recent_activity(df)
    
    if recent_activity:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Recent Matches", recent_activity['recent_matches'])
        with col2:
            st.metric("Active Players", recent_activity['recent_players'])
        with col3:
            st.metric("Recent Kills", recent_activity['recent_kills'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_kd_leaderboard_chart(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_weapon_usage_chart(df), use_container_width=True)
    
    # Match timeline
    st.plotly_chart(create_match_timeline(df), use_container_width=True)

# Player Analysis Page
elif page == "📊 Player Analysis":
    st.title("📊 Player Analysis")
    
    # Player selection
    players = get_unique_players(df)
    if players:
        selected_player = st.selectbox("Select Player", players)
        
        if selected_player:
            player_stats = get_player_stats(df, selected_player)
            
            if player_stats:
                # Player stats cards
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("K/D Ratio", f"{player_stats['kd_ratio']}")
                with col2:
                    st.metric("Accuracy", f"{player_stats['accuracy']}%")
                with col3:
                    st.metric("Total Kills", player_stats['total_kills'])
                with col4:
                    st.metric("Total Matches", player_stats['total_matches'])
                
                # Performance trend
                st.subheader("Performance Over Time")
                st.plotly_chart(create_player_performance_trend(df, selected_player), use_container_width=True)
                
                # Player details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Player Details")
                    st.write(f"**Favorite Weapon:** {player_stats['favorite_weapon']}")
                    st.write(f"**Best Match Kills:** {player_stats['best_match_kills']}")
                    st.write(f"**Best Match Score:** {player_stats['best_match_score']}")
                    if player_stats['avg_ping']:
                        st.write(f"**Average Ping:** {player_stats['avg_ping']}ms")
                
                with col2:
                    st.subheader("Averages")
                    st.write(f"**Kills per Match:** {player_stats['avg_kills_per_match']}")
                    st.write(f"**Deaths per Match:** {player_stats['avg_deaths_per_match']}")
                    st.write(f"**Score per Match:** {player_stats['avg_score_per_match']}")
                    st.write(f"**Total Coins:** {player_stats['total_coins']}")
    else:
        st.info("No player data available. Add some matches first!")

# Team Analysis Page
elif page == "👥 Team Analysis":
    st.title("👥 Team Analysis")
    
    team_stats = get_team_stats(df)
    
    if team_stats:
        # Team performance chart
        st.plotly_chart(create_team_performance_chart(df), use_container_width=True)
        
        # Team details
        st.subheader("Team Details")
        for team, stats in team_stats.items():
            with st.expander(f"Team {team}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Matches", stats['matches'])
                with col2:
                    st.metric("Win Rate", f"{stats['win_rate']}%")
                with col3:
                    st.metric("Total Kills", stats['total_kills'])
                with col4:
                    st.metric("Avg Score", stats['avg_score_per_match'])
    else:
        st.info("No team data available. Team matches will appear here.")

# Match History Page
elif page == "📈 Match History":
    st.title("📈 Match History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
    
    with col2:
        players = get_unique_players(df)
        selected_players = st.multiselect("Filter by Players", players)
    
    with col3:
        game_modes = get_unique_game_modes(df)
        selected_mode = st.selectbox("Filter by Game Mode", ["All"] + game_modes)
    
    # Apply filters
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filter_data_by_date_range(filtered_df, pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
    if selected_players:
        filtered_df = filter_data_by_players(filtered_df, selected_players)
    if selected_mode != "All":
        filtered_df = filter_data_by_game_mode(filtered_df, selected_mode)
    
    # Match timeline
    st.plotly_chart(create_match_timeline(filtered_df), use_container_width=True)
    
    # Map performance
    st.plotly_chart(create_map_performance_chart(filtered_df), use_container_width=True)
    
    # Recent matches table
    st.subheader("Recent Matches")
    if not filtered_df.empty:
        recent_matches = filtered_df.groupby('match_id').agg({
            'datetime': 'first',
            'game_mode': 'first',
            'map_name': 'first',
            'player_name': 'count',
            'kills': 'sum',
            'score': 'sum'
        }).reset_index()
        
        recent_matches.columns = ['Match ID', 'Date', 'Game Mode', 'Map', 'Players', 'Total Kills', 'Total Score']
        recent_matches = recent_matches.sort_values('Date', ascending=False).head(10)
        
        st.dataframe(recent_matches, use_container_width=True)
    else:
        st.info("No matches found with the selected filters.")

# Data Input Page
elif page == "🎮 Data Input":
    st.title("🎮 Add Match Data")
    
    # Match metadata
    st.subheader("Match Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        match_datetime = st.datetime_input("Match Date & Time", value=datetime.now())
    
    with col2:
        game_mode = st.selectbox("Game Mode", ["Team", "FFA"])
    
    with col3:
        maps = get_unique_maps(df)
        if maps:
            map_name = st.selectbox("Map", maps)
        else:
            map_name = st.text_input("Map Name", "Desert")
    
    # Player data input
    st.subheader("Player Data")
    
    # Initialize player data
    if 'player_data' not in st.session_state:
        st.session_state.player_data = []
    
    # Add new player button
    if st.button("➕ Add Player"):
        st.session_state.player_data.append({
            'player_name': '',
            'kills': 0,
            'deaths': 0,
            'assists': 0,
            'score': 0,
            'weapon': 'AK47',
            'ping': None,
            'coins': 0,
            'team': None
        })
    
    # Display and edit player data
    for i, player in enumerate(st.session_state.player_data):
        with st.expander(f"Player {i+1}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                players = get_unique_players(df)
                if players:
                    player['player_name'] = st.selectbox(
                        f"Player Name {i+1}", 
                        ["New Player"] + players,
                        key=f"player_name_{i}"
                    )
                else:
                    player['player_name'] = st.text_input(f"Player Name {i+1}", key=f"player_name_{i}")
                
                player['kills'] = st.number_input(f"Kills {i+1}", min_value=0, value=player['kills'], key=f"kills_{i}")
                player['deaths'] = st.number_input(f"Deaths {i+1}", min_value=0, value=player['deaths'], key=f"deaths_{i}")
            
            with col2:
                if game_mode == "Team":
                    player['assists'] = st.number_input(f"Assists {i+1}", min_value=0, value=player['assists'], key=f"assists_{i}")
                    player['team'] = st.selectbox(f"Team {i+1}", ["Team1", "Team2"], key=f"team_{i}")
                else:
                    player['assists'] = None
                    player['team'] = None
                
                player['score'] = st.number_input(f"Score {i+1}", min_value=0, value=player['score'], key=f"score_{i}")
            
            with col3:
                weapons = get_unique_weapons(df)
                if weapons:
                    player['weapon'] = st.selectbox(f"Weapon {i+1}", weapons, key=f"weapon_{i}")
                else:
                    player['weapon'] = st.text_input(f"Weapon {i+1}", value=player['weapon'], key=f"weapon_{i}")
                
                player['ping'] = st.number_input(f"Ping {i+1}", min_value=0, value=player['ping'] or 50, key=f"ping_{i}")
                player['coins'] = st.number_input(f"Coins {i+1}", min_value=0, value=player['coins'], key=f"coins_{i}")
            
            # Remove player button
            if st.button(f"❌ Remove Player {i+1}", key=f"remove_{i}"):
                st.session_state.player_data.pop(i)
                st.rerun()
    
    # Save match button
    if st.button("💾 Save Match") and st.session_state.player_data:
        # Prepare match data
        match_id = get_next_match_id(df)
        match_data = []
        
        for player in st.session_state.player_data:
            if player['player_name'] and player['player_name'] != "New Player":
                player_data = player.copy()
                player_data['match_id'] = match_id
                player_data['datetime'] = match_datetime
                player_data['game_mode'] = game_mode
                player_data['map_name'] = map_name
                match_data.append(player_data)
        
        # Validate data
        errors = validate_match_data(match_data)
        
        if errors:
            st.error("Validation errors:")
            for error in errors:
                st.error(error)
        else:
            # Save to dataframe
            df = add_match_to_dataframe(df, match_data)
            save_match_data(df)
            st.session_state.match_data = df
            st.session_state.player_data = []
            st.success("Match saved successfully!")
            st.rerun()

# Advanced Analytics Page
elif page == "🔧 Advanced Analytics":
    st.title("🔧 Advanced Analytics")
    
    # Player comparison
    st.subheader("Player Comparison")
    players = get_unique_players(df)
    if len(players) >= 2:
        selected_players = st.multiselect("Select Players to Compare", players, max_selections=5)
        if len(selected_players) >= 2:
            st.plotly_chart(create_player_comparison_radar(df, selected_players), use_container_width=True)
    
    # Ping impact analysis
    st.subheader("Ping Impact Analysis")
    st.plotly_chart(create_ping_impact_chart(df), use_container_width=True)
    
    # Weapon meta analysis
    st.subheader("Weapon Meta Analysis")
    weapon_stats = get_weapon_stats(df)
    if weapon_stats:
        weapon_df = pd.DataFrame.from_dict(weapon_stats, orient='index')
        weapon_df = weapon_df.sort_values('usage_count', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Most Popular Weapons**")
            st.dataframe(weapon_df[['usage_count', 'kd_ratio', 'accuracy']].head(), use_container_width=True)
        
        with col2:
            st.write("**Best Performing Weapons**")
            best_weapons = weapon_df.sort_values('kd_ratio', ascending=False)
            st.dataframe(best_weapons[['usage_count', 'kd_ratio', 'accuracy']].head(), use_container_width=True)

# Leaderboards Page
elif page == "📋 Leaderboards":
    st.title("📋 Leaderboards")
    
    # Leaderboard type selection
    leaderboard_type = st.selectbox(
        "Leaderboard Type",
        ["K/D Ratio", "Total Kills", "Accuracy", "Avg Kills per Match", "Total Score", "Total Coins"]
    )
    
    # Get leaderboard data
    metric_map = {
        "K/D Ratio": "kd_ratio",
        "Total Kills": "total_kills",
        "Accuracy": "accuracy",
        "Avg Kills per Match": "avg_kills_per_match",
        "Total Score": "total_score",
        "Total Coins": "total_coins"
    }
    
    leaderboard_df = get_leaderboard_data(df, metric_map[leaderboard_type])
    
    if not leaderboard_df.empty:
        # Display leaderboard
        st.subheader(f"Top Players by {leaderboard_type}")
        
        # Format the display
        display_df = leaderboard_df.copy()
        display_df = display_df.round(2)
        
        # Add rank column
        display_df.insert(0, 'Rank', range(1, len(display_df) + 1))
        
        st.dataframe(display_df, use_container_width=True)
        
        # Create chart
        fig = go.Figure(data=[
            go.Bar(
                x=leaderboard_df['player_name'].head(10),
                y=leaderboard_df[metric_map[leaderboard_type]].head(10),
                text=leaderboard_df[metric_map[leaderboard_type]].head(10),
                textposition='auto',
                marker_color='#1f77b4'
            )
        ])
        
        fig.update_layout(
            title=f'Top 10 Players by {leaderboard_type}',
            xaxis_title='Player',
            yaxis_title=leaderboard_type,
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for leaderboards.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Deadshot Stats Dashboard**")
st.sidebar.markdown("Track your gaming performance!")

# Data info
if not df.empty:
    st.sidebar.markdown(f"**Data Summary:**")
    st.sidebar.markdown(f"• {len(df['match_id'].unique())} matches")
    st.sidebar.markdown(f"• {len(df['player_name'].unique())} players")
    st.sidebar.markdown(f"• {df['kills'].sum()} total kills")
else:
    st.sidebar.markdown("No data loaded yet.") 