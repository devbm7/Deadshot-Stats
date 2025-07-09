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
    get_map_stats, get_recent_activity, get_match_summary, get_player_evolution_timeline,
    get_performance_clusters, get_player_streaks, get_team_chemistry_matrix,
    get_player_role_analysis, get_team_formation_performance, get_battle_royale_rankings,
    get_achievement_badges, get_gaming_session_analysis
)
from utils.visualizations import (
    create_overview_cards, create_kd_leaderboard_chart, create_player_performance_trend,
    create_weapon_usage_chart, create_map_performance_chart, create_team_performance_chart,
    create_player_comparison_radar, create_match_timeline, create_ping_impact_chart,
    create_mode_wise_analysis, create_map_wise_analysis, create_weapon_map_analysis,
    create_player_evolution_chart, create_performance_clusters_chart, create_streak_analysis_chart,
    create_team_chemistry_heatmap, create_role_analysis_chart, create_team_formation_chart,
    create_battle_royale_rankings_chart, create_achievement_badges_chart, create_gaming_session_analysis_chart,
    create_achievement_details
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
        color: #000000;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background-color: #2d3748;
            color: #ffffff;
        }
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
     "🎮 Data Input", "🔧 Advanced Analytics", "📋 Leaderboards", "🎉 Fun Features"]
)

# Load data
df = st.session_state.match_data

# Dashboard Page
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">Deadshot Stats Dashboard</h1>', unsafe_allow_html=True)
    
    # Overview cards
    overview_stats = create_overview_cards(df)
    
    col1, col2, col3 = st.columns(3)
    
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
            <h3>Avg K/D Ratio</h3>
            <h2>{overview_stats['avg_kd_ratio']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    recent_activity = get_recent_activity(df)
    
    if recent_activity:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recent Matches", recent_activity['recent_matches'])
        with col2:
            st.metric("Recent Kills", recent_activity['recent_kills'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_kd_leaderboard_chart(df), use_container_width=True, key="kd_leaderboard_chart")
    
    with col2:
        st.plotly_chart(create_weapon_usage_chart(df), use_container_width=True, key="weapon_usage_chart")
    
    # Match timeline
    st.plotly_chart(create_match_timeline(df), use_container_width=True, key="match_timeline")

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
                    st.metric("Win Rate", f"{player_stats['win_rate']}%")
                with col3:
                    st.metric("Kills/Min", f"{player_stats['kills_per_minute']}")
                with col4:
                    st.metric("Total Matches", player_stats['total_matches'])
                
                # Performance trend
                st.subheader("Performance Over Time (Per-Minute)")
                st.plotly_chart(create_player_performance_trend(df, selected_player), use_container_width=True, key="player_performance_trend")
                
                # Player details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Player Details")
                    st.write(f"**Favorite Weapon:** {player_stats['favorite_weapon']}")
                    st.write(f"**Wins:** {player_stats['wins']}")
                    st.write(f"**Losses:** {player_stats['losses']}")
                    st.write(f"**Total Time Played:** {player_stats['total_minutes']} minutes")
                    st.write(f"**Best Match Kills:** {player_stats['best_match_kills']}")
                    st.write(f"**Best Match Score:** {player_stats['best_match_score']}")
                    st.write(f"**Best Match Assists:** {player_stats['best_match_assists']}")
                    if player_stats['avg_ping']:
                        st.write(f"**Average Ping:** {player_stats['avg_ping']}ms")
                
                with col2:
                    st.subheader("Per-Minute Metrics")
                    st.write(f"**Kills per Minute:** {player_stats['kills_per_minute']}")
                    st.write(f"**Deaths per Minute:** {player_stats['deaths_per_minute']}")
                    st.write(f"**Assists per Minute:** {player_stats['assists_per_minute']}")
                    st.write(f"**Score per Minute:** {player_stats['score_per_minute']}")
                    st.write(f"**Total Coins:** {player_stats['total_coins']}")
    else:
        st.info("No player data available. Add some matches first!")

# Team Analysis Page
elif page == "👥 Team Analysis":
    st.title("👥 Team Analysis")
    
    team_stats = get_team_stats(df)
    
    if team_stats:
        # Team performance chart
        st.plotly_chart(create_team_performance_chart(df), use_container_width=True, key="team_performance_chart")
        
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
    
    # Team Dynamics Analysis
    st.header("🔗 Team Dynamics")
    
    # Team Chemistry Matrix
    st.subheader("🧪 Team Chemistry Matrix")
    st.write("Shows win rates when players team up together. Green = high win rate, Red = low win rate.")
    chemistry_fig = create_team_chemistry_heatmap(df)
    st.plotly_chart(chemistry_fig, use_container_width=True, key="team_chemistry_heatmap")
    
    # Role Analysis
    st.subheader("🎭 Player Role Analysis")
    st.write("Radar chart showing each player's strengths and their primary role in the team.")
    role_fig = create_role_analysis_chart(df)
    st.plotly_chart(role_fig, use_container_width=True, key="role_analysis_chart")
    
    # Show role details
    role_analysis = get_player_role_analysis(df)
    if role_analysis:
        st.write("**Player Roles:**")
        for player, analysis in role_analysis.items():
            with st.expander(f"{player} - {analysis['primary_role']}"):
                st.write(f"**Role:** {analysis['primary_role']}")
                st.write(f"**Description:** {analysis['role_description']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Stats:**")
                    st.write(f"• K/D Ratio: {analysis['stats']['kd_ratio']:.2f}")
                    st.write(f"• Kills/Min: {analysis['stats']['kills_per_minute']:.2f}")
                    st.write(f"• Assists/Min: {analysis['stats']['assists_per_minute']:.2f}")
                with col2:
                    st.write("**Strengths:**")
                    st.write(f"• Killing Power: {analysis['role_strengths']['killing_power']:.1%}")
                    st.write(f"• Support Value: {analysis['role_strengths']['support_value']:.1%}")
                    st.write(f"• Survival Rate: {analysis['role_strengths']['survival_rate']:.1%}")
    
    # Team Formation Performance
    st.subheader("🏆 Team Formation Performance")
    st.write("Bubble chart showing how different team combinations perform. Size = number of matches, Color = win rate.")
    formation_fig = create_team_formation_chart(df)
    st.plotly_chart(formation_fig, use_container_width=True, key="team_formation_chart")
    
    # Show formation details
    formation_stats = get_team_formation_performance(df)
    if formation_stats:
        st.write("**Top Team Formations:**")
        for i, (formation_key, stats) in enumerate(formation_stats.items()):
            if i < 5:  # Show top 5 formations
                with st.expander(f"Formation {i+1}: {' + '.join(stats['players'])}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Win Rate", f"{stats['win_rate']}%")
                        st.metric("Matches", stats['matches'])
                    with col2:
                        st.metric("Avg Kills", f"{stats['avg_kills_per_match']:.1f}")
                        st.metric("Avg Score", f"{stats['avg_score_per_match']:.1f}")
                    with col3:
                        st.write("**Formation Size:**", stats['formation_size'])
                        if stats['win_rate'] > 70:
                            st.success("Elite Formation")
                        elif stats['win_rate'] > 50:
                            st.info("Good Formation")
                        else:
                            st.warning("Needs Improvement")
    
    if not team_stats and not formation_stats:
        st.info("No team data available. Team matches will appear here.")

# Match History Page
elif page == "📈 Match History":
    st.title("📈 Match History")
    
    # Debug: Show available players (can be removed later)
    if st.checkbox("Show Debug Info"):
        st.write("Available players:", get_unique_players(df))
        st.write("Available game modes:", get_unique_game_modes(df))
        st.write("Available maps:", get_unique_maps(df))
    
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
        selected_players = st.multiselect("Filter by Players", players, help="Select players to filter matches")
    
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
    st.plotly_chart(create_match_timeline(filtered_df), use_container_width=True, key="filtered_match_timeline")
    
    # Map performance
    st.plotly_chart(create_map_performance_chart(filtered_df), use_container_width=True, key="filtered_map_performance_chart")
    
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
        # Use date and time inputs separately since datetime_input doesn't exist
        match_date = st.date_input("Match Date", value=datetime.now().date())
        match_time = st.time_input("Match Time", value=datetime.now().time())
        match_datetime = datetime.combine(match_date, match_time)
    
    with col2:
        game_mode = st.selectbox("Game Mode", ["Team", "FFA"])
    
    with col3:
        maps = get_unique_maps(df)
        if maps:
            map_name = st.selectbox("Map", maps)
        else:
            map_name = st.text_input("Map Name", "Desert")
        match_length = st.selectbox("Match Length (minutes)", [5, 10, 20], index=1)
    
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
                player_data['match_length'] = match_length
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
    
    # Get unique players
    players = get_unique_players(df)
    
    # Advanced Analytics
    st.header("🔬 Advanced Analytics")
    
    # Player Evolution Timeline
    st.subheader("📈 Player Evolution Timeline")
    selected_player_evolution = st.selectbox(
        "Select player for evolution analysis:",
        options=players,
        key="evolution_player"
    )
    
    if selected_player_evolution:
        evolution_fig = create_player_evolution_chart(df, selected_player_evolution)
        st.plotly_chart(evolution_fig, use_container_width=True, key="evolution_chart")
        
        # Show evolution insights
        evolution_data = get_player_evolution_timeline(df, selected_player_evolution)
        if evolution_data:
            evolution_df = pd.DataFrame(evolution_data)
            if len(evolution_df) > 1:
                first_match = evolution_df.iloc[0]
                last_match = evolution_df.iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("K/D Improvement", 
                            f"{last_match['kd_ratio'] - first_match['kd_ratio']:.2f}",
                            f"{first_match['kd_ratio']:.2f} → {last_match['kd_ratio']:.2f}")
                with col2:
                    st.metric("Kills/Min Improvement",
                            f"{last_match['kills_per_minute'] - first_match['kills_per_minute']:.2f}",
                            f"{first_match['kills_per_minute']:.2f} → {last_match['kills_per_minute']:.2f}")
                with col3:
                    st.metric("Score/Min Improvement",
                            f"{last_match['score_per_minute'] - first_match['score_per_minute']:.2f}",
                            f"{first_match['score_per_minute']:.2f} → {last_match['score_per_minute']:.2f}")
    
    # Performance Clusters
    st.subheader("🎯 Performance Clusters")
    st.write("Players grouped by similar playing styles based on K/D ratio, kills per minute, assists, and win rate.")
    
    clusters_fig = create_performance_clusters_chart(df)
    st.plotly_chart(clusters_fig, use_container_width=True, key="clusters_chart")
    
    # Show cluster details
    cluster_stats = get_performance_clusters(df)
    if cluster_stats:
        st.write("**Cluster Analysis:**")
        for cluster_id, stats in cluster_stats.items():
            with st.expander(f"Cluster {cluster_id + 1} ({stats['cluster_size']} players)"):
                st.write(f"**Players:** {', '.join(stats['players'])}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg K/D Ratio", f"{stats['avg_kd_ratio']:.2f}")
                    st.metric("Avg Kills/Min", f"{stats['avg_kills_per_min']:.2f}")
                with col2:
                    st.metric("Avg Assists/Min", f"{stats['avg_assists_per_min']:.2f}")
                    st.metric("Avg Win Rate", f"{stats['avg_win_rate']:.1f}%")
                with col3:
                    st.write("**Cluster Characteristics:**")
                    if stats['avg_kd_ratio'] > 1.5 and stats['avg_win_rate'] > 60:
                        st.success("High Performers")
                    elif stats['avg_kd_ratio'] < 0.8 and stats['avg_win_rate'] < 40:
                        st.error("Struggling Players")
                    else:
                        st.info("Balanced Players")
    
    # Streak Analysis
    st.subheader("🔥 Streak Analysis")
    selected_player_streak = st.selectbox(
        "Select player for streak analysis:",
        options=players,
        key="streak_player"
    )
    
    if selected_player_streak:
        streak_fig = create_streak_analysis_chart(df, selected_player_streak)
        st.plotly_chart(streak_fig, use_container_width=True, key="streak_chart")
        
        # Show streak details
        streak_data = get_player_streaks(df, selected_player_streak)
        if streak_data:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Streak", 
                        streak_data['current_streak'])
            with col2:
                st.metric("Max Win Streak", streak_data['max_win_streak'])
            with col3:
                st.metric("Max Loss Streak", streak_data['max_loss_streak'])
            with col4:
                st.metric("Recent Win Rate", f"{streak_data['recent_win_rate']:.1f}%")
                
                # Streak insights
                if streak_data['current_streak'] > 0:
                    st.success(f"🔥 {selected_player_streak} is on a {streak_data['current_streak']}-match winning streak!")
                elif streak_data['current_streak'] < 0:
                    st.error(f"😔 {selected_player_streak} is on a {abs(streak_data['current_streak'])}-match losing streak.")
                else:
                    st.info(f"⚖️ {selected_player_streak} broke their streak in the last match.")
    
    # Mode-wise Analysis
    st.subheader("🎮 Game Mode Analysis")
    mode_fig = create_mode_wise_analysis(df)
    st.plotly_chart(mode_fig, use_container_width=True, key="mode_analysis_chart")
    
    # Map-wise Analysis
    st.subheader("🗺️ Map Performance Analysis")
    map_fig = create_map_wise_analysis(df)
    st.plotly_chart(map_fig, use_container_width=True, key="map_analysis_chart")
    
    # Weapon-Map Combinations
    st.subheader("🔫 Weapon-Map Combinations")
    weapon_map_fig = create_weapon_map_analysis(df)
    st.plotly_chart(weapon_map_fig, use_container_width=True, key="weapon_map_chart")
    
    # Player comparison
    st.subheader("👥 Player Comparison")
    players = get_unique_players(df)
    if len(players) >= 2:
        selected_players = st.multiselect("Select Players to Compare", players, max_selections=5)
        if len(selected_players) >= 2:
            st.plotly_chart(create_player_comparison_radar(df, selected_players), use_container_width=True, key="player_comparison_radar")
    
    # Ping impact analysis
    st.subheader("📡 Ping Impact Analysis")
    st.plotly_chart(create_ping_impact_chart(df), use_container_width=True, key="ping_impact_chart")
    
    # Weapon meta analysis
    st.subheader("⚔️ Weapon Meta Analysis")
    weapon_stats = get_weapon_stats(df)
    if weapon_stats:
        weapon_df = pd.DataFrame.from_dict(weapon_stats, orient='index')
        weapon_df = weapon_df.sort_values('usage_count', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Most Popular Weapons**")
            st.dataframe(weapon_df[['usage_count', 'kd_ratio']].head(), use_container_width=True)
        
        with col2:
            st.write("**Best Performing Weapons**")
            best_weapons = weapon_df.sort_values('kd_ratio', ascending=False)
            st.dataframe(best_weapons[['usage_count', 'kd_ratio']].head(), use_container_width=True)

# Leaderboards Page
elif page == "📋 Leaderboards":
    st.title("📋 Leaderboards")
    
    # Leaderboard type selection
    leaderboard_type = st.selectbox(
        "Leaderboard Type",
        ["K/D Ratio", "Total Kills", "Avg Kills per Match", "Total Score", "Total Coins", "Total Assists", "Win Rate"]
    )
    
    # Get leaderboard data
    metric_map = {
        "K/D Ratio": "kd_ratio",
        "Total Kills": "total_kills",
        "Avg Kills per Match": "avg_kills_per_match",
        "Total Score": "total_score",
        "Total Coins": "total_coins",
        "Total Assists": "total_assists",
        "Win Rate": "win_rate"
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

# Fun Features Page
elif page == "🎉 Fun Features":
    st.title("🎉 Fun & Engaging Features")
    
    # Battle Royale Rankings
    st.header("🏆 Battle Royale Rankings")
    st.write("Tournament-style rankings with tier system based on overall performance.")
    
    rankings_fig = create_battle_royale_rankings_chart(df)
    st.plotly_chart(rankings_fig, use_container_width=True, key="battle_royale_rankings")
    
    # Show ranking details
    rankings_data = get_battle_royale_rankings(df)
    if rankings_data:
        st.write("**Tier System:**")
        for tier_name, players in rankings_data['tiers'].items():
            if players:
                with st.expander(f"{tier_name} Tier ({len(players)} players)"):
                    for i, player in enumerate(players):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{i+1}.** {player['player_name']}")
                        with col2:
                            st.write(f"Score: {player['ranking_score']:.1f}")
                        with col3:
                            st.write(f"K/D: {player['kd_ratio']:.2f}")
    
    # Achievement Badges
    st.header("🏅 Achievement Badges")
    st.write("Unlockable achievements based on performance milestones.")
    
    badges_fig = create_achievement_badges_chart(df)
    st.plotly_chart(badges_fig, use_container_width=True, key="achievement_badges")
    
    # Show achievement details for selected player
    players = get_unique_players(df)
    if players:
        selected_player_achievements = st.selectbox(
            "Select player to view achievements:",
            options=players,
            key="achievement_player"
        )
        
        if selected_player_achievements:
            achievement_details_fig = create_achievement_details(df, selected_player_achievements)
            st.plotly_chart(achievement_details_fig, use_container_width=True, key="achievement_details")
            
            # Show achievement list
            achievements_data = get_achievement_badges(df)
            if achievements_data and selected_player_achievements in achievements_data:
                player_achievements = achievements_data[selected_player_achievements]['achievements']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Unlocked Achievements:**")
                    for achievement in player_achievements:
                        if achievement['unlocked']:
                            st.success(f"✅ {achievement['name']} - {achievement['description']}")
                
                with col2:
                    st.write("**In Progress:**")
                    for achievement in player_achievements:
                        if not achievement['unlocked']:
                            st.info(f"🔄 {achievement['name']} - {achievement['progress']:.0f}%")
    
    # Gaming Session Analysis
    st.header("🎮 Gaming Session Analysis")
    st.write("Analyze performance patterns over time and identify optimal gaming sessions.")
    
    session_fig = create_gaming_session_analysis_chart(df)
    st.plotly_chart(session_fig, use_container_width=True, key="gaming_session_analysis")
    
    # Show session insights
    session_data = get_gaming_session_analysis(df)
    if session_data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sessions", session_data['total_sessions'])
        with col2:
            st.metric("Avg Session Duration", f"{session_data['avg_session_duration']:.1f} days")
        with col3:
            if session_data['hourly_performance']:
                best_hour = max(session_data['hourly_performance'], key=lambda x: x['kills'])
                st.metric("Best Gaming Hour", f"{best_hour['hour']}:00")
        
        # Show session details
        if session_data['session_analysis']:
            st.write("**Session Details:**")
            for session_id, session_info in session_data['session_analysis'].items():
                with st.expander(f"Session {session_id} ({session_info['duration_days']} days)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Period:** {session_info['start_date']} to {session_info['end_date']}")
                        st.write(f"**Matches:** {session_info['total_matches']}")
                    with col2:
                        st.write(f"**Avg K/D:** {session_info['avg_kd_ratio']:.2f}")
                        st.write(f"**Total Kills:** {session_info['total_kills']}")
                    with col3:
                        st.write(f"**Peak Day:** {session_info['peak_performance_day']}")
                        st.write(f"**Peak K/D:** {session_info['peak_kd_ratio']:.2f}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Deadshot Stats Dashboard**")
st.sidebar.markdown("Track your gaming performance!")

# Data info
if not df.empty:
    st.sidebar.markdown(f"**Data Summary:**")
    st.sidebar.markdown(f"• {len(df['match_id'].unique())} matches")
    st.sidebar.markdown(f"• {df['kills'].sum()} total kills")
else:
    st.sidebar.markdown("No data loaded yet.") 