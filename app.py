import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
from PIL import Image

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import show_supabase_status, get_gemini_api_key, show_gemini_status
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
    get_achievement_badges, get_gaming_session_analysis, get_player_comparison_data,
    simulate_team_scenario, get_optimal_team_composition
)
from utils.visualizations import (
    create_overview_cards, create_kd_leaderboard_chart, create_player_performance_trend,
    create_weapon_usage_chart, create_map_performance_chart, create_team_performance_chart,
    create_player_comparison_radar, create_match_timeline, create_detailed_match_timeline, create_ping_impact_chart,
    create_mode_wise_analysis, create_map_wise_analysis, create_weapon_map_analysis,
    create_player_evolution_chart, create_performance_clusters_chart, create_streak_analysis_chart,
    create_team_chemistry_heatmap, create_role_analysis_chart, create_team_formation_chart,
    create_battle_royale_rankings_chart, create_achievement_badges_chart, create_gaming_session_analysis_chart,
    create_achievement_details, create_player_comparison_chart, create_scenario_simulation_chart,
    create_optimal_team_chart
)
from utils.image_processing import (
    extract_data_from_image, validate_extracted_data, format_extracted_data_for_display,
    get_extraction_confidence
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
    /* Modern Gaming Theme */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #f59e0b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: #334155;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--card-bg), #2d3748);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    .metric-card h3 {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-primary);
    }
    
    /* Status Cards */
    .status-card {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        margin: 0.5rem 0;
    }
    
    .status-success {
        border-left: 4px solid var(--success-color);
    }
    
    .status-warning {
        border-left: 4px solid var(--warning-color);
    }
    
    .status-error {
        border-left: 4px solid var(--error-color);
    }
    
    /* Enhanced Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--dark-bg), #1e293b);
        border-right: 1px solid var(--border-color);
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-bg);
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-color: var(--primary-color);
    }
    
    /* Dataframe Styling */
    .dataframe {
        background: var(--card-bg);
        border-radius: 0.75rem;
        overflow: hidden;
    }
    
    /* Progress Bars */
    .progress-container {
        background: var(--border-color);
        border-radius: 1rem;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--success-color), var(--accent-color));
        border-radius: 1rem;
        transition: width 0.3s ease;
    }
    
    /* Achievement Badges */
    .achievement-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
        background: linear-gradient(135deg, var(--accent-color), #f97316);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid var(--border-color);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .metric-card h2 {
            font-size: 2rem;
        }
    }
    
    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background: var(--card-bg);
            color: var(--text-primary);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'match_data' not in st.session_state:
    st.session_state.match_data = load_match_data()

# Enhanced Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
        Deadshot Stats
    </h1>
    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
        Gaming Analytics Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation with enhanced styling
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Dashboard", "📊 Player Analysis", "👥 Team Analysis", "📈 Match History", 
     "🎮 Data Input", "🔧 Advanced Analytics", "📋 Leaderboards", "🎉 Fun Features", "🎛️ Interactive Dashboards"],
    help="Select a page to navigate to"
)

# Load data
df = st.session_state.match_data

# Dashboard Page
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">Deadshot Stats Dashboard</h1>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Charts", "📋 Player Stats", "📅 Match Timeline"])
    
    with tab1:
        # Overview cards
        overview_stats = create_overview_cards(df)
        
        # Main metrics row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Total Matches</h3>
                <h2>{overview_stats['total_matches']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💀 Total Kills</h3>
                <h2>{overview_stats['total_kills']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚖️ Avg K/D Ratio</h3>
                <h2>{overview_stats['avg_kd_ratio']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Secondary metrics row
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                total_score = int(df['score'].sum())
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 Total Score</h3>
                    <h2>{total_score:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎮 Game Modes</h3>
                    <h2>{len(get_unique_game_modes(df))}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity with enhanced styling
        st.markdown("### 📈 Recent Activity")
        recent_activity = get_recent_activity(df)
        
        if recent_activity:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="status-card status-success">
                    <h4>📊 Recent Matches</h4>
                    <h3>{recent_activity['recent_matches']}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="status-card status-success">
                    <h4>💀 Recent Kills</h4>
                    <h3>{recent_activity['recent_kills']}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                recent_score = recent_activity.get('recent_score', 0)
                st.markdown(f"""
                <div class="status-card status-success">
                    <h4>🏆 Recent Score</h4>
                    <h3>{recent_score:,}</h3>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📈 Performance Charts")
        
        # K/D Leaderboard
        st.write("**Top Players by K/D Ratio**")
        st.plotly_chart(create_kd_leaderboard_chart(df), use_container_width=True, key="kd_leaderboard_chart")
        
        # Weapon Usage
        st.write("**Weapon Usage Statistics**")
        st.plotly_chart(create_weapon_usage_chart(df), use_container_width=True, key="weapon_usage_chart")
    
    with tab3:
        st.subheader("📋 All Players Stats Table")
        players = get_unique_players(df)
        
        if players:
            # Get all player stats
            all_player_stats = []
            for player in players:
                player_stats = get_player_stats(df, player)
                if player_stats:
                    all_player_stats.append({
                        'Player': player,
                        'K/D Ratio': round(player_stats['kd_ratio'], 2),
                        'Win Rate (%)': round(player_stats['win_rate'], 1),
                        'Kills/Min': round(player_stats['kills_per_minute'], 2),
                        'Deaths/Min': round(player_stats['deaths_per_minute'], 2),
                        'Assists/Min': round(player_stats['assists_per_minute'], 2),
                        'Score/Min': round(player_stats['score_per_minute'], 2),
                        'Tags/Min': round(player_stats.get('tags_per_minute', 0), 2),
                        'Total Matches': player_stats['total_matches'],
                        'Total Kills': player_stats['total_kills'],
                        'Total Assists': player_stats['total_assists'],
                        'Total Score': player_stats['total_score'],
                        'Total Tags': player_stats.get('total_tags', 0),
                        'Wins': player_stats['wins'],
                        'Losses': player_stats['losses'],
                        'Total Time (min)': player_stats['total_minutes'],
                        'Best Match Kills': player_stats['best_match_kills'],
                        'Best Match Score': player_stats['best_match_score'],
                        'Best Match Tags': player_stats.get('best_match_tags', 0),
                        'Favorite Weapon': player_stats['favorite_weapon']
                    })
            
            # Create DataFrame and sort by K/D ratio
            player_df = pd.DataFrame(all_player_stats)
            player_df = player_df.sort_values('K/D Ratio', ascending=False)
            
            # Add rank column
            player_df.insert(0, 'Rank', range(1, len(player_df) + 1))
            
            # Display the table
            st.dataframe(player_df, use_container_width=True)
            
            # Add download button
            csv = player_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Player Stats as CSV",
                data=csv,
                file_name="player_stats.csv",
                mime="text/csv"
            )
        else:
            st.info("No player data available. Add some matches first!")
    
    with tab4:
        st.subheader("📅 Match Timeline")
        
        # Timeline type selection
        timeline_type = st.selectbox(
            "Select Timeline View",
            ["📈 Performance Timeline", "📊 Detailed Analysis"],
            help="Performance Timeline shows key metrics over time. Detailed Analysis provides comprehensive breakdown with trends."
        )
        
        if timeline_type == "📈 Performance Timeline":
            st.plotly_chart(create_match_timeline(df), use_container_width=True, key="match_timeline")
        else:
            st.plotly_chart(create_detailed_match_timeline(df), use_container_width=True, key="detailed_match_timeline")



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
                # Create tabs for player analysis
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Performance", "🎯 Details", "📊 Comparison"])
                
                with tab1:
                    st.markdown(f"### 📊 {selected_player} Overview")
                    
                    # Player stats cards with enhanced styling
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>⚖️ K/D Ratio</h3>
                            <h2>{player_stats['kd_ratio']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🏆 Win Rate</h3>
                            <h2>{player_stats['win_rate']:.1f}%</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>💀 Kills/Min</h3>
                            <h2>{player_stats['kills_per_minute']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🎮 Total Matches</h3>
                            <h2>{player_stats['total_matches']}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Secondary stats row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>💔 Deaths/Min</h3>
                            <h2>{player_stats['deaths_per_minute']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🤝 Assists/Min</h3>
                            <h2>{player_stats['assists_per_minute']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🏆 Score/Min</h3>
                            <h2>{player_stats['score_per_minute']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        tags_per_min = player_stats.get('tags_per_minute', 0)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🏷️ Tags/Min</h3>
                            <h2>{tags_per_min:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Performance trend with enhanced title
                    st.markdown("### 📈 Performance Over Time (Per-Minute)")
                    st.plotly_chart(create_player_performance_trend(df, selected_player), use_container_width=True, key="player_performance_trend")
                
                with tab2:
                    st.subheader("📈 Performance Metrics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Per-Minute Metrics:**")
                        st.write(f"• Kills per Minute: {player_stats['kills_per_minute']}")
                        st.write(f"• Deaths per Minute: {player_stats['deaths_per_minute']}")
                        st.write(f"• Assists per Minute: {player_stats['assists_per_minute']}")
                        st.write(f"• Score per Minute: {player_stats['score_per_minute']}")
                        st.write(f"• Tags per Minute: {player_stats.get('tags_per_minute', 0)}")
                    
                    with col2:
                        st.write("**Match Statistics:**")
                        st.write(f"• Wins: {player_stats['wins']}")
                        st.write(f"• Losses: {player_stats['losses']}")
                        st.write(f"• Total Time Played: {player_stats['total_minutes']} minutes")
                        st.write(f"• Total Coins: {player_stats['total_coins']}")
                        st.write(f"• Total Tags: {player_stats.get('total_tags', 0)}")
                
                with tab3:
                    st.subheader("🎯 Player Details")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Best Performances:**")
                        st.write(f"• Best Match Kills: {player_stats['best_match_kills']}")
                        st.write(f"• Best Match Score: {player_stats['best_match_score']}")
                        st.write(f"• Best Match Assists: {player_stats['best_match_assists']}")
                        st.write(f"• Best Match Tags: {player_stats.get('best_match_tags', 0)}")
                        st.write(f"• Favorite Weapon: {player_stats['favorite_weapon']}")
                    
                    with col2:
                        st.write("**Network & Technical:**")
                        if player_stats['avg_ping']:
                            st.write(f"• Average Ping: {player_stats['avg_ping']}ms")
                        st.write(f"• Total Matches: {player_stats['total_matches']}")
                        st.write(f"• Total Kills: {player_stats['total_kills']}")
                        st.write(f"• Total Assists: {player_stats['total_assists']}")
                        st.write(f"• Total Tags: {player_stats.get('total_tags', 0)}")
                
                with tab4:
                    st.subheader("📊 Player Comparison")
                    
                    # Compare with other players
                    other_players = [p for p in players if p != selected_player]
                    if other_players:
                        compare_player = st.selectbox("Compare with:", other_players, key="compare_player")
                        
                        if compare_player:
                            st.plotly_chart(create_player_comparison_radar(df, [selected_player, compare_player]), use_container_width=True, key="player_comparison_radar")
    else:
        st.info("No player data available. Add some matches first!")

# Team Analysis Page
elif page == "👥 Team Analysis":
    st.title("👥 Team Analysis")
    
    # Create tabs for team analysis
    tab1, tab2, tab3 = st.tabs(["🏆 Team Performance", "🔗 Team Dynamics", "📊 Team Details"])
    
    with tab1:
        st.subheader("🏆 Team Performance")
        team_stats = get_team_stats(df)
        
        if team_stats:
            # Team performance chart
            st.plotly_chart(create_team_performance_chart(df), use_container_width=True, key="team_performance_chart")
        else:
            st.info("No team data available. Team matches will appear here.")
    
    with tab2:
        st.subheader("🔗 Team Dynamics")
        
        # Team Chemistry Matrix
        st.write("**Team Chemistry Matrix**")
        st.write("Shows win rates when players team up together. Green = high win rate, Red = low win rate.")
        chemistry_fig = create_team_chemistry_heatmap(df)
        st.plotly_chart(chemistry_fig, use_container_width=True, key="team_chemistry_heatmap")
        
        # Role Analysis
        st.write("**Player Role Analysis**")
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
    
    with tab3:
        st.subheader("📊 Team Formation Performance")
        
        # Team Formation Performance
        st.write("**Team Formation Performance**")
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
        
        # Team details
        team_stats = get_team_stats(df)
        if team_stats:
            st.write("**Team Details:**")
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
    
    # Match timeline with options
    st.subheader("📈 Match Timeline")
    
    # Timeline type selection for filtered data
    filtered_timeline_type = st.selectbox(
        "Select Timeline View",
        ["📈 Performance Timeline", "📊 Detailed Analysis"],
        help="Performance Timeline shows key metrics over time. Detailed Analysis provides comprehensive breakdown with trends.",
        key="filtered_timeline_type"
    )
    
    if filtered_timeline_type == "📈 Performance Timeline":
        st.plotly_chart(create_match_timeline(filtered_df), use_container_width=True, key="filtered_match_timeline")
    else:
        st.plotly_chart(create_detailed_match_timeline(filtered_df), use_container_width=True, key="filtered_detailed_match_timeline")
    
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
        
        # Robust datetime parsing for the aggregated data
        try:
            recent_matches['Date'] = pd.to_datetime(recent_matches['Date'], format='mixed', errors='coerce')
        except Exception:
            recent_matches['Date'] = pd.to_datetime(recent_matches['Date'], errors='coerce')
        
        # Normalize 'Date' to tz-naive before sorting
        if hasattr(recent_matches['Date'].dt, 'tz_localize'):
            if recent_matches['Date'].dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in recent_matches['Date'] if pd.notnull(x)):
                recent_matches['Date'] = recent_matches['Date'].dt.tz_localize(None)
        
        recent_matches = recent_matches.sort_values('Date', ascending=False).head(10)
        
        st.dataframe(recent_matches, use_container_width=True)
    else:
        st.info("No matches found with the selected filters.")

# Data Input Page
elif page == "🎮 Data Input":
    st.title("🎮 Add Match Data")
    
    # Create tabs for different input methods
    input_tab1, input_tab2 = st.tabs(["📷 Image Upload", "✏️ Manual Input"])
    
    with input_tab1:
        st.markdown("### 📷 Upload Screenshot")
        st.markdown("""
        <div class="status-card status-success">
            <h4>🤖 AI-Powered Data Extraction</h4>
            <p>Upload a screenshot of your match results and let our AI automatically extract all the data for you!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check Gemini API configuration
        api_key = get_gemini_api_key()
        
        if not api_key:
            st.markdown("""
            <div class="status-card status-error">
                <h4>⚠️ Gemini API Not Configured</h4>
                <p>Please set up your Gemini API key to use the AI extraction feature.</p>
            </div>
            """, unsafe_allow_html=True)
            show_gemini_status()
        else:
            # File upload with enhanced styling
            st.markdown("""
            <div class="status-card status-success">
                <h4>📤 Ready to Upload</h4>
                <p>Supported formats: PNG, JPG, JPEG</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose a screenshot file", 
                type=['png', 'jpg', 'jpeg'],
                help="Upload a screenshot of the match results"
            )
            
            if uploaded_file is not None:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Screenshot", use_container_width=True)
                
                # Extract data button
                if st.button("🔍 Extract Data from Image", type="primary"):
                    with st.spinner("Analyzing image with AI..."):
                        extracted_data = extract_data_from_image(image, api_key)
                        
                        if "error" not in extracted_data:
                            # Validate extracted data
                            validation_errors = validate_extracted_data(extracted_data)
                            
                            if validation_errors:
                                st.error("❌ Data extraction issues:")
                                for error in validation_errors:
                                    st.error(f"• {error}")
                            else:
                                # Format data for display
                                formatted_data = format_extracted_data_for_display(extracted_data)
                                confidence = get_extraction_confidence(extracted_data)
                                
                                # Show confidence indicator
                                if confidence == "high":
                                    st.success("✅ High confidence extraction")
                                elif confidence == "medium":
                                    st.warning("⚠️ Medium confidence extraction")
                                else:
                                    st.info("ℹ️ Low confidence extraction")
                                
                                # Store extracted data in session state
                                st.session_state.extracted_data = formatted_data
                                st.session_state.extraction_success = True
                                
                                st.success("Data extracted successfully! Review and edit below.")
                                
                                # Debug: Show raw extracted data
                                with st.expander("🔍 Debug: Raw Extracted Data"):
                                    st.json(extracted_data)
                                
                                st.rerun()
                        else:
                            st.error(f"❌ Extraction failed: {extracted_data['error']}")
            
            # Show extracted data for review
            if hasattr(st.session_state, 'extraction_success') and st.session_state.extraction_success:
                st.subheader("📋 Review Extracted Data")
                
                extracted_data = st.session_state.extracted_data
                
                # Match metadata
                st.write("**Match Information:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    match_date = st.date_input("Match Date", value=datetime.now().date(), key="extracted_date")
                    match_time = st.time_input("Match Time", value=datetime.now().time(), key="extracted_time")
                    match_datetime = datetime.combine(match_date, match_time)
                
                with col2:
                    game_mode = st.selectbox("Game Mode", ["Team", "FFA", "Confirm", "Team Confirm"], 
                                   index=0 if extracted_data.get("game_mode") == "Team" else 
                                         1 if extracted_data.get("game_mode") == "FFA" else
                                         2 if extracted_data.get("game_mode") == "Confirm" else 3,
                                   key="extracted_game_mode")
                
                with col3:
                    maps = get_unique_maps(df)
                    if maps:
                        default_map = extracted_data.get("map_name") if extracted_data.get("map_name") in maps else maps[0]
                        map_name = st.selectbox("Map", maps, index=maps.index(default_map) if default_map in maps else 0, key="extracted_map")
                    else:
                        map_name = st.text_input("Map Name", value=extracted_data.get("map_name", "Refinery"), key="extracted_map")
                    
                    match_length = st.selectbox("Match Length (minutes)", [5, 10, 20], 
                                              index=[5, 10, 20].index(extracted_data.get("match_length", 10)) if extracted_data.get("match_length") in [5, 10, 20] else 1,
                                              key="extracted_match_length")
                
                # Player data review
                st.write("**Player Data:**")
                
                # Initialize player data from extracted data (only once)
                if 'extracted_player_data' not in st.session_state:
                    st.session_state.extracted_player_data = []
                    # Populate with extracted data only on first load
                    for player in extracted_data.get("players", []):
                        st.session_state.extracted_player_data.append({
                            'player_name': player.get('player_name', ''),
                            'original_name': player.get('player_name', ''),  # Store original name for reference
                            'kills': player.get('kills', 0),
                            'deaths': player.get('deaths', 0),
                            'assists': player.get('assists'),
                            'score': player.get('score', 0),
                            'weapon': player.get('weapon', 'AR'),
                            'ping': player.get('ping'),
                            'coins': player.get('coins', 0),
                            'team': player.get('team'),
                            'tags': player.get('tags', 0) if extracted_data.get("game_mode") in ["Confirm", "Team Confirm"] else None
                        })
                
                # Display and edit player data
                for i, player in enumerate(st.session_state.extracted_player_data):
                    with st.expander(f"Player {i+1}: {player['player_name']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            players = get_unique_players(df)
                            
                            # Create a more flexible player name input
                            st.write(f"**Player {i+1} Name:**")
                            
                            # Option 1: Dropdown for existing players
                            if players:
                                col_dropdown, col_text = st.columns([1, 1])
                                
                                with col_dropdown:
                                    st.write("**Existing Players:**")
                                    # Check if the extracted player name exists in the list
                                    current_player_name = player['player_name']
                                    if current_player_name and current_player_name in players:
                                        # Player exists, use their index + 1 (since "New Player" is at index 0)
                                        selected_index = players.index(current_player_name) + 1
                                    else:
                                        # Player doesn't exist, default to "New Player"
                                        selected_index = 0
                                    
                                    selected_player = st.selectbox(
                                        f"Select from existing players", 
                                        ["New Player"] + players,
                                        index=selected_index,
                                        key=f"extracted_player_dropdown_{i}"
                                    )
                                
                                with col_text:
                                    st.write("**Or type custom name:**")
                                    custom_name = st.text_input(
                                        f"Custom player name", 
                                        value=player['player_name'] if player['player_name'] not in players else "",
                                        key=f"extracted_player_text_{i}"
                                    )
                                
                                # Use custom name if provided, otherwise use dropdown selection
                                if custom_name and custom_name.strip():
                                    player['player_name'] = custom_name.strip()
                                else:
                                    player['player_name'] = selected_player
                                
                                # Show AI detection hint
                                if player.get('original_name') and player['player_name'] == "New Player":
                                    st.info(f"💡 AI detected: '{player.get('original_name')}'. Type it above if correct.")
                            else:
                                # No existing players, just use text input
                                player['player_name'] = st.text_input(f"Player Name {i+1}", value=player['player_name'], key=f"extracted_player_name_{i}")
                            
                            player['kills'] = st.number_input(f"Kills {i+1}", min_value=0, value=player['kills'], key=f"extracted_kills_{i}")
                            player['deaths'] = st.number_input(f"Deaths {i+1}", min_value=0, value=player['deaths'], key=f"extracted_deaths_{i}")
                        
                        with col2:
                            if game_mode in ["Team", "Team Confirm"]:
                                player['assists'] = st.number_input(f"Assists {i+1}", min_value=0, value=player['assists'] or 0, key=f"extracted_assists_{i}")
                                player['team'] = st.selectbox(f"Team {i+1}", ["Team1", "Team2"], 
                                                           index=0 if player.get('team') == "Team1" else 1,
                                                           key=f"extracted_team_{i}")
                            else:
                                player['assists'] = None
                                player['team'] = None
                            
                            player['score'] = st.number_input(f"Score {i+1}", min_value=0, value=player['score'], key=f"extracted_score_{i}")
                        
                        with col3:
                            weapons = get_unique_weapons(df)
                            if weapons:
                                default_weapon = player['weapon'] if player['weapon'] in weapons else weapons[0]
                                player['weapon'] = st.selectbox(f"Weapon {i+1}", weapons, 
                                                             index=weapons.index(default_weapon) if default_weapon in weapons else 0,
                                                             key=f"extracted_weapon_{i}")
                            else:
                                player['weapon'] = st.text_input(f"Weapon {i+1}", value=player['weapon'], key=f"extracted_weapon_{i}")
                            
                            player['ping'] = st.number_input(f"Ping {i+1}", min_value=0, value=player['ping'] or 50, key=f"extracted_ping_{i}")
                            player['coins'] = st.number_input(f"Coins {i+1}", min_value=0, value=player['coins'], key=f"extracted_coins_{i}")
                            
                            # Add tags field for Confirm and Team Confirm modes
                            if game_mode in ["Confirm", "Team Confirm"]:
                                player['tags'] = st.number_input(f"Tags {i+1}", min_value=0, value=player.get('tags', 0), key=f"extracted_tags_{i}")
                            else:
                                player['tags'] = None
                        
                        # Remove player button - placed after the columns for better layout
                        st.markdown("---")
                        col_remove1, col_remove2, col_remove3 = st.columns([1, 1, 1])
                        with col_remove2:
                            if st.button(f"❌ Remove Player {i+1}", key=f"extracted_remove_{i}", type="secondary"):
                                if 'extracted_player_data' in st.session_state and len(st.session_state.extracted_player_data) > 1:
                                    st.session_state.extracted_player_data.pop(i)
                                    st.rerun()
                                else:
                                    st.error("Cannot remove the last player. At least one player is required.")
                
                # Debug info (can be removed later)
                if st.checkbox("Show Debug Info", key="extracted_debug"):
                    st.write(f"Current players: {len(st.session_state.extracted_player_data)}")
                    st.write(f"Player data: {st.session_state.extracted_player_data}")
                
                # Add new player button
                if st.button("➕ Add Player", key="extracted_add_player"):
                    st.session_state.extracted_player_data.append({
                        'player_name': '',
                        'original_name': '',
                        'kills': 0,
                        'deaths': 0,
                        'assists': 0,
                        'score': 0,
                        'weapon': 'AR',
                        'ping': None,
                        'coins': 0,
                        'team': None,
                        'tags': 0
                    })
                    st.rerun()
                
                # Save match button
                if st.button("💾 Save Match", key="extracted_save_match") and st.session_state.extracted_player_data:
                    # Prepare match data
                    match_id = get_next_match_id(df)
                    match_data = []
                    
                    valid_players = 0
                    for player in st.session_state.extracted_player_data:
                        if player['player_name'] and player['player_name'] != "New Player":
                            player_data = player.copy()
                            # Remove the original_name field as it's not part of the data schema
                            if 'original_name' in player_data:
                                del player_data['original_name']
                            player_data['match_id'] = match_id
                            player_data['datetime'] = match_datetime
                            player_data['game_mode'] = game_mode
                            player_data['map_name'] = map_name
                            player_data['match_length'] = match_length
                            match_data.append(player_data)
                            valid_players += 1
                    
                    if valid_players == 0:
                        st.error("❌ No valid players found. Please ensure at least one player has a valid name.")
                    else:
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
                            st.session_state.extracted_player_data = []
                            st.session_state.extraction_success = False
                            if 'extracted_data' in st.session_state:
                                del st.session_state.extracted_data
                            st.success(f"✅ Match saved successfully! {valid_players} players added.")
                            st.rerun()
    
    with input_tab2:
        st.subheader("✏️ Manual Data Entry")
        st.write("Enter match data manually.")
        
        # Match metadata
        st.write("**Match Information:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Use date and time inputs separately since datetime_input doesn't exist
            match_date = st.date_input("Match Date", value=datetime.now().date(), key="manual_date")
            match_time = st.time_input("Match Time", value=datetime.now().time(), key="manual_time")
            match_datetime = datetime.combine(match_date, match_time)
        
        with col2:
            game_mode = st.selectbox("Game Mode", ["Team", "FFA", "Confirm", "Team Confirm"], key="manual_game_mode")
        
        with col3:
            maps = get_unique_maps(df)
            if maps:
                map_name = st.selectbox("Map", maps, key="manual_map")
            else:
                map_name = st.text_input("Map Name", "Refinery", key="manual_map")
            match_length = st.selectbox("Match Length (minutes)", [5, 10, 20], index=1, key="manual_match_length")
        
        # Player data input
        st.subheader("Player Data")
        
        # Initialize player data for manual input
        if 'manual_player_data' not in st.session_state:
            st.session_state.manual_player_data = []
        
        # Add new player button
        if st.button("➕ Add Player", key="manual_add_player"):
            st.session_state.manual_player_data.append({
                'player_name': '',
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'score': 0,
                'weapon': 'AR',
                'ping': None,
                'coins': 0,
                'team': None,
                'tags': 0
            })
        
        # Display and edit player data
        for i, player in enumerate(st.session_state.manual_player_data):
            with st.expander(f"Player {i+1}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    players = get_unique_players(df)
                    
                    # Create a more flexible player name input for manual entry
                    st.write(f"**Player {i+1} Name:**")
                    
                    if players:
                        col_dropdown, col_text = st.columns([1, 1])
                        
                        with col_dropdown:
                            st.write("**Existing Players:**")
                            selected_player = st.selectbox(
                                f"Select from existing players", 
                                ["New Player"] + players,
                                key=f"manual_player_dropdown_{i}"
                            )
                        
                        with col_text:
                            st.write("**Or type custom name:**")
                            custom_name = st.text_input(
                                f"Custom player name", 
                                key=f"manual_player_text_{i}"
                            )
                        
                        # Use custom name if provided, otherwise use dropdown selection
                        if custom_name and custom_name.strip():
                            player['player_name'] = custom_name.strip()
                        else:
                            player['player_name'] = selected_player
                    else:
                        # No existing players, just use text input
                        player['player_name'] = st.text_input(f"Player Name {i+1}", key=f"manual_player_name_{i}")
                    
                    player['kills'] = st.number_input(f"Kills {i+1}", min_value=0, value=player['kills'], key=f"manual_kills_{i}")
                    player['deaths'] = st.number_input(f"Deaths {i+1}", min_value=0, value=player['deaths'], key=f"manual_deaths_{i}")
                
                with col2:
                    if game_mode in ["Team", "Team Confirm"]:
                        player['assists'] = st.number_input(f"Assists {i+1}", min_value=0, value=player['assists'], key=f"manual_assists_{i}")
                        player['team'] = st.selectbox(f"Team {i+1}", ["Team1", "Team2"], key=f"manual_team_{i}")
                    else:
                        player['assists'] = None
                        player['team'] = None
                    
                    player['score'] = st.number_input(f"Score {i+1}", min_value=0, value=player['score'], key=f"manual_score_{i}")
                
                with col3:
                    weapons = get_unique_weapons(df)
                    if weapons:
                        player['weapon'] = st.selectbox(f"Weapon {i+1}", weapons, key=f"manual_weapon_{i}")
                    else:
                        player['weapon'] = st.text_input(f"Weapon {i+1}", value=player['weapon'], key=f"manual_weapon_{i}")
                    
                    player['ping'] = st.number_input(f"Ping {i+1}", min_value=0, value=player['ping'] or 50, key=f"manual_ping_{i}")
                    player['coins'] = st.number_input(f"Coins {i+1}", min_value=0, value=player['coins'], key=f"manual_coins_{i}")
                    
                    # Add tags field for Confirm and Team Confirm modes
                    if game_mode in ["Confirm", "Team Confirm"]:
                        player['tags'] = st.number_input(f"Tags {i+1}", min_value=0, value=player.get('tags', 0), key=f"manual_tags_{i}")
                    else:
                        player['tags'] = None
                
                # Remove player button
                if st.button(f"❌ Remove Player {i+1}", key=f"manual_remove_{i}"):
                    st.session_state.manual_player_data.pop(i)
                    st.rerun()
        
        # Save match button
        if st.button("💾 Save Match", key="manual_save_match") and st.session_state.manual_player_data:
            # Prepare match data
            match_id = get_next_match_id(df)
            match_data = []
            
            for player in st.session_state.manual_player_data:
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
                st.session_state.manual_player_data = []
                st.success("Match saved successfully!")
                st.rerun()

# Advanced Analytics Page
elif page == "🔧 Advanced Analytics":
    st.title("🔧 Advanced Analytics")
    
    # Create tabs for advanced analytics
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Player Analytics", "🎮 Game Analysis", "👥 Player Comparison", "📊 Meta Analysis"])
    
    with tab1:
        st.header("📈 Player Analytics")
        
        # Get unique players
        players = get_unique_players(df)
        
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
    
    with tab2:
        st.header("🎮 Game Analysis")
        
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
    
    with tab3:
        st.header("👥 Player Comparison")
        
        # Player comparison
        players = get_unique_players(df)
        if len(players) >= 2:
            selected_players = st.multiselect("Select Players to Compare", players, max_selections=5)
            if len(selected_players) >= 2:
                st.plotly_chart(create_player_comparison_radar(df, selected_players), use_container_width=True, key="player_comparison_radar")
        
        # Ping impact analysis
        st.subheader("📡 Ping Impact Analysis")
        st.plotly_chart(create_ping_impact_chart(df), use_container_width=True, key="ping_impact_chart")
    
    with tab4:
        st.header("📊 Meta Analysis")
        
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
        ["K/D Ratio", "Total Kills", "Avg Kills per Match", "Total Score", "Total Coins", "Total Assists", "Win Rate", "Total Tags", "Avg Tags per Match"]
    )
    
    # Get leaderboard data
    metric_map = {
        "K/D Ratio": "kd_ratio",
        "Total Kills": "total_kills",
        "Avg Kills per Match": "avg_kills_per_match",
        "Total Score": "total_score",
        "Total Coins": "total_coins",
        "Total Assists": "total_assists",
        "Win Rate": "win_rate",
        "Total Tags": "total_tags",
        "Avg Tags per Match": "avg_tags_per_match"
    }
    
    leaderboard_df = get_leaderboard_data(df, metric_map[leaderboard_type])
    
    if not leaderboard_df.empty:
        # Display leaderboard with enhanced styling
        st.markdown(f"### 🏆 Top Players by {leaderboard_type}")
        
        # Format the display
        display_df = leaderboard_df.copy()
        display_df = display_df.round(2)
        
        # Add rank column with emojis
        ranks = []
        for i in range(1, len(display_df) + 1):
            if i == 1:
                ranks.append("🥇")
            elif i == 2:
                ranks.append("🥈")
            elif i == 3:
                ranks.append("🥉")
            else:
                ranks.append(f"#{i}")
        
        display_df.insert(0, 'Rank', ranks)
        
        # Display top 3 with special styling
        if len(display_df) >= 3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🥇 1st Place</h3>
                    <h2>{display_df.iloc[0]['player_name']}</h2>
                    <p>{display_df.iloc[0][metric_map[leaderboard_type]]:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🥈 2nd Place</h3>
                    <h2>{display_df.iloc[1]['player_name']}</h2>
                    <p>{display_df.iloc[1][metric_map[leaderboard_type]]:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🥉 3rd Place</h3>
                    <h2>{display_df.iloc[2]['player_name']}</h2>
                    <p>{display_df.iloc[2][metric_map[leaderboard_type]]:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Full leaderboard table
        st.markdown("### 📋 Complete Leaderboard")
        st.dataframe(display_df, use_container_width=True)
        
        # Create enhanced chart
        fig = go.Figure(data=[
            go.Bar(
                x=leaderboard_df['player_name'].head(10),
                y=leaderboard_df[metric_map[leaderboard_type]].head(10),
                text=leaderboard_df[metric_map[leaderboard_type]].head(10),
                textposition='auto',
                marker=dict(
                    color=['#FFD700', '#C0C0C0', '#CD7F32'] + ['#6366f1'] * 7,
                    line=dict(color='#1e293b', width=1)
                )
            )
        ])
        
        fig.update_layout(
            title=f'🏆 Top 10 Players by {leaderboard_type}',
            xaxis_title='Player',
            yaxis_title=leaderboard_type,
            showlegend=False,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for leaderboards.")

# Fun Features Page
elif page == "🎉 Fun Features":
    st.title("🎉 Fun & Engaging Features")
    
    # Create tabs for fun features
    tab1, tab2, tab3 = st.tabs(["🏆 Rankings", "🏅 Achievements", "🎮 Sessions"])
    
    with tab1:
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
    
    with tab2:
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
    
    with tab3:
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

# Interactive Dashboards Page
elif page == "🎛️ Interactive Dashboards":
    st.title("🎛️ Interactive Dashboards")
    
    # Create tabs for interactive dashboards
    tab1, tab2 = st.tabs(["⚔️ Player Comparison", "🎯 Scenario Simulator"])
    
    with tab1:
        st.header("⚔️ Player Comparison Tool")
        st.write("Compare two players side-by-side with interactive sliders and detailed metrics.")
        
        players = get_unique_players(df)
        if len(players) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                player1 = st.selectbox("Select Player 1", players, key="comparison_player1")
            
            with col2:
                player2 = st.selectbox("Select Player 2", players, key="comparison_player2")
            
            if player1 and player2 and player1 != player2:
                # Create comparison chart
                comparison_fig = create_player_comparison_chart(df, player1, player2)
                st.plotly_chart(comparison_fig, use_container_width=True, key="player_comparison_chart")
                
                # Show detailed comparison
                comparison_data = get_player_comparison_data(df, player1, player2)
                if comparison_data:
                    st.write("**Detailed Comparison:**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**K/D Ratio:**")
                        winner = comparison_data['winners']['kd_ratio']
                        diff = comparison_data['comparison']['kd_ratio_diff']
                        st.write(f"{winner} wins by {abs(diff):.2f}")
                    
                    with col2:
                        st.write("**Win Rate:**")
                        winner = comparison_data['winners']['win_rate']
                        diff = comparison_data['comparison']['win_rate_diff']
                        st.write(f"{winner} wins by {abs(diff):.1f}%")
                    
                    with col3:
                        st.write("**Kills per Minute:**")
                        winner = comparison_data['winners']['kills_per_min']
                        diff = comparison_data['comparison']['kills_per_min_diff']
                        st.write(f"{winner} wins by {abs(diff):.2f}")
                    
                    # Interactive sliders for custom scenarios
                    st.subheader("🎛️ Custom Scenario Sliders")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Player 1 Adjustments:**")
                        p1_kd_boost = st.slider(f"{player1} K/D Boost", -1.0, 2.0, 0.0, 0.1, key="p1_kd_boost")
                        p1_win_boost = st.slider(f"{player1} Win Rate Boost", -20, 30, 0, 1, key="p1_win_boost")
                    
                    with col2:
                        st.write("**Player 2 Adjustments:**")
                        p2_kd_boost = st.slider(f"{player2} K/D Boost", -1.0, 2.0, 0.0, 0.1, key="p2_kd_boost")
                        p2_win_boost = st.slider(f"{player2} Win Rate Boost", -20, 30, 0, 1, key="p2_win_boost")
                    
                    # Show adjusted comparison
                    if p1_kd_boost != 0 or p1_win_boost != 0 or p2_kd_boost != 0 or p2_win_boost != 0:
                        st.write("**Adjusted Comparison:**")
                        adjusted_p1_kd = comparison_data['player1']['stats']['kd_ratio'] + p1_kd_boost
                        adjusted_p1_win = comparison_data['player1']['stats']['win_rate'] + p1_win_boost
                        adjusted_p2_kd = comparison_data['player2']['stats']['kd_ratio'] + p2_kd_boost
                        adjusted_p2_win = comparison_data['player2']['stats']['win_rate'] + p2_win_boost
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(f"{player1} Adjusted K/D", f"{adjusted_p1_kd:.2f}", f"{p1_kd_boost:+.2f}")
                            st.metric(f"{player1} Adjusted Win Rate", f"{adjusted_p1_win:.1f}%", f"{p1_win_boost:+.1f}%")
                        
                        with col2:
                            st.metric(f"{player2} Adjusted K/D", f"{adjusted_p2_kd:.2f}", f"{p2_kd_boost:+.2f}")
                            st.metric(f"{player2} Adjusted Win Rate", f"{adjusted_p2_win:.1f}%", f"{p2_win_boost:+.1f}%")
    
    with tab2:
        st.header("🎯 Scenario Simulator")
        st.write("Simulate different team compositions and predict outcomes.")
        
        if len(players) >= 3:
            # Team composition selection
            st.subheader("Team Composition")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Your Team:**")
                team_size = st.slider("Team Size", 2, 5, 3, key="team_size")
                team_players = st.multiselect("Select Team Players", players, max_selections=team_size, key="team_players")
            
            with col2:
                st.write("**Opponent Team (Optional):**")
                opponent_players = st.multiselect("Select Opponent Players", players, max_selections=team_size, key="opponent_players")
            
            if team_players:
                # Simulate team scenario
                scenario_fig = create_scenario_simulation_chart(df, team_players, opponent_players if opponent_players else None)
                st.plotly_chart(scenario_fig, use_container_width=True, key="scenario_simulation_chart")
                
                # Show simulation results
                team_performance = simulate_team_scenario(df, team_players, opponent_players if opponent_players else None)
                if team_performance:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Predicted Win Rate", f"{team_performance['predicted_win_rate']:.1f}%")
                        st.metric("Avg K/D Ratio", f"{team_performance['avg_kd_ratio']:.2f}")
                    
                    with col2:
                        st.metric("Synergy Score", f"{team_performance['synergy_score']:.1f}")
                        st.metric("Total Kills/Min", f"{team_performance['total_kills_per_min']:.2f}")
                    
                    with col3:
                        if opponent_players and 'head_to_head_win_rate' in team_performance:
                            st.metric("Head-to-Head Win Rate", f"{team_performance['head_to_head_win_rate']:.1f}%")
                        st.metric("Team Size", team_performance['team_size'])
            
            # Optimal team finder
            st.subheader("🎯 Optimal Team Finder")
            st.write("Find the best team composition from available players.")
            
            available_players = st.multiselect("Select Available Players", players, default=players[:min(6, len(players))], key="available_players")
            optimal_team_size = st.slider("Optimal Team Size", 2, 5, 3, key="optimal_team_size")
            
            if len(available_players) >= optimal_team_size:
                if st.button("Find Optimal Team"):
                    optimal_data = get_optimal_team_composition(df, available_players, optimal_team_size)
                    
                    if optimal_data and optimal_data['best_team']:
                        st.success(f"🏆 Best Team: {' + '.join(optimal_data['best_team'])}")
                        st.metric("Team Score", f"{optimal_data['best_score']:.1f}")
                        
                        # Show optimal team chart
                        optimal_fig = create_optimal_team_chart(df, available_players, optimal_team_size)
                        st.plotly_chart(optimal_fig, use_container_width=True, key="optimal_team_chart")
                        
                        # Show top teams
                        st.write("**Top Team Combinations:**")
                        sorted_teams = sorted(optimal_data['all_teams'].items(), key=lambda x: x[1]['score'], reverse=True)[:5]
                        
                        for i, (team, data) in enumerate(sorted_teams):
                            with st.expander(f"#{i+1}: {' + '.join(team)}"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Score", f"{data['score']:.1f}")
                                    st.metric("Win Rate", f"{data['performance']['predicted_win_rate']:.1f}%")
                                with col2:
                                    st.metric("Synergy", f"{data['performance']['synergy_score']:.1f}")
                                    st.metric("Avg K/D", f"{data['performance']['avg_kd_ratio']:.2f}")
                                with col3:
                                    st.metric("Kills/Min", f"{data['performance']['total_kills_per_min']:.2f}")
                                    st.metric("Assists/Min", f"{data['performance']['total_assists_per_min']:.2f}")
        else:
            st.info("Need at least 3 players for scenario simulation.")

# Enhanced Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h4 style="color: #f8fafc; margin: 0;">📊 Data Summary</h4>
</div>
""", unsafe_allow_html=True)

# Data info with enhanced styling
if not df.empty:
    total_matches = len(df['match_id'].unique())
    total_kills = df['kills'].sum()
    
    st.sidebar.markdown(f"""
    <div class="status-card status-success">
        <h4>🎮 {total_matches} Matches</h4>
        <h4>💀 {total_kills:,} Kills</h4>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="status-card status-warning">
        <h4>📝 No Data Yet</h4>
        <p>Add some matches to see your stats!</p>
    </div>
    """, unsafe_allow_html=True)

# App Information
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 App Information**")

# Feature explanations
with st.sidebar.expander("🏆 Achievement Requirements"):
    st.markdown("""
    **Sharpshooter**: K/D ratio above 2.0\n
    **Kill Master**: 100+ total kills\n
    **Survivor**: Less than 0.3 deaths per minute\n
    **Support Hero**: 0.5+ assists per minute\n
    **Winner**: 70%+ win rate\n
    **Veteran**: 20+ matches played\n
    **Speed Demon**: 1.0+ kills per minute\n
    **Consistent**: 10+ matches played\n
    **Elite**: Elite tier ranking\n
    **Champion**: Champion tier ranking\n
    """)

with st.sidebar.expander("📊 Player Analysis Features"):
    st.markdown("""
    **K/D Ratio**: Kills ÷ Deaths\n
    **Win Rate**: (Wins ÷ Total Matches) × 100\n
    **Per-Minute Metrics**: Normalized by match length to avoid bias\n
    **Player Evolution**: Moving averages over time\n
    **Performance Clusters**: Machine learning grouping by play style\n
    **Streak Analysis**: Win/loss patterns and trends\n
    """)

with st.sidebar.expander("👥 Team Analysis Features"):
    st.markdown("""
    **Team Chemistry**: Win rates when players team up\n
    **Player Roles**: Killer, Support, Aggressive, Leader, Balanced\n
    **Team Formation**: Performance of different combinations\n
    **Synergy Score**: Based on role diversity and combinations\n
    **Win Prediction**: Based on team stats and synergy\n
    """)

with st.sidebar.expander("🎯 Battle Royale Rankings"):
    st.markdown("""
    **Ranking Score**: Weighted combination of:
    • K/D ratio (30%)
    • Win rate (30%)
    • Kills per minute (20%)
    • Matches played (10%) 
    • Assists per minute (10%)
    
    **Tiers**: Champion, Elite, Veteran, Rookie, Novice
    """)

with st.sidebar.expander("🎛️ Interactive Features"):
    st.markdown("""
    **Player Comparison**: Side-by-side stats with sliders\n
    **Scenario Simulator**: "What if" team compositions\n
    **Optimal Team Finder**: Best combinations from available players\n
    **Custom Scenarios**: Adjust player stats to see impact\n
    """)

with st.sidebar.expander("📈 Advanced Analytics"):
    st.markdown("""
    **Player Evolution**: Performance trends over time\n
    **Performance Clusters**: ML-based player grouping\n
    **Streak Analysis**: Win/loss patterns\n
    **Mode Analysis**: Team vs FFA performance\n
    **Map Analysis**: Performance across different maps\n
    **Weapon-Map Analysis**: Weapon effectiveness by map\n
    """)

with st.sidebar.expander("🎮 Gaming Session Analysis"):
    st.markdown("""
    **Daily Performance**: K/D trends over time\n
    **Hourly Performance**: Best gaming hours\n
    **Session Duration**: Gaming session patterns\n
    **Session Performance**: Compare different sessions\n
    **Peak Performance**: Optimal gaming periods\n
    """)

with st.sidebar.expander("📋 Data Input Guide"):
    st.markdown("""
    **Match Length**: 5, 10, or 20 minutes\n
    **Game Modes**: 
    • Team: Team-based with assists and team assignments
    • FFA: Individual performance only
    • Confirm: Tag collection mode - players drop tags when killed, winner has most tags
    • Team Confirm: Team tag collection mode - teams compete for most tags
    **Weapons**: Track weapon usage per match\n
    **Ping**: Optional network performance\n
    **Coins**: Optional currency tracking\n
    **Tags**: Required for Confirm/Team Confirm modes - number of tags collected
    """)

with st.sidebar.expander("🔧 Technical Details"):
    st.markdown("""
    **Data Storage**: CSV format for persistence\n
    **Normalization**: All stats normalized by match length\n
    **Win Calculation**: \n
    • Team: Highest team score wins\n
    • FFA: Highest individual score wins\n
    **Role Classification**: Based on K/D, kills/min, assists/min\n
    **Synergy Calculation**: Role diversity + specific combinations\n
    """)

# Tips and tricks
with st.sidebar.expander("💡 Tips & Tricks"):
    st.markdown("""
    **📊 Dashboard**: Quick overview with player stats table\n
    **📈 Match History**: Filter by date, players, or game mode\n
    **🎛️ Interactive**: Test different team compositions\n
    **🏆 Fun Features**: Track achievements and rankings\n
    **📥 Export**: Download data for external analysis\n
    """) 