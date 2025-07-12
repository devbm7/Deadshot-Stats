import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from utils.calculations import get_player_stats, get_weapon_stats, get_map_stats, get_performance_clusters, get_player_streaks, get_player_evolution_timeline,  get_team_chemistry_matrix, get_player_role_analysis, get_team_formation_performance, get_battle_royale_rankings, get_achievement_badges, get_gaming_session_analysis, get_player_comparison_data, simulate_team_scenario, get_optimal_team_composition

def create_overview_cards(df):
    """Create overview statistics cards"""
    if df.empty:
        return {
            'total_matches': 0,
            'total_kills': 0,
            'avg_kd_ratio': 0
        }
    
    total_matches = len(df['match_id'].unique())
    total_kills = int(df['kills'].sum())
    
    # Calculate average K/D ratio
    total_deaths = df['deaths'].sum()
    avg_kd_ratio = round(total_kills / total_deaths, 2) if total_deaths > 0 else 0
    
    return {
        'total_matches': total_matches,
        'total_kills': total_kills,
        'avg_kd_ratio': avg_kd_ratio
    }

def create_mode_wise_analysis(df):
    """Create mode-wise performance analysis"""
    if df.empty:
        return go.Figure()
    
    # Group by game mode and calculate stats
    mode_stats = df.groupby('game_mode').agg({
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_id': 'nunique',
        'player_name': 'nunique',
        'match_length': 'sum'  # Total minutes played
    }).reset_index()
    
    # Normalize by match length (per minute metrics)
    mode_stats['kd_ratio'] = mode_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    mode_stats['kills_per_minute'] = mode_stats['kills'] / mode_stats['match_length']
    mode_stats['score_per_minute'] = mode_stats['score'] / mode_stats['match_length']
    mode_stats['matches_per_player'] = mode_stats['match_id'] / mode_stats['player_name']
    
    fig = go.Figure()
    
    # Create subplots
    fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=('Matches per Player', 'K/D Ratio', 'Kills per Minute', 'Score per Minute'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Matches per player
    fig.add_trace(
        go.Bar(x=mode_stats['game_mode'], y=mode_stats['matches_per_player'], name='Matches/Player', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # K/D ratio
    fig.add_trace(
        go.Bar(x=mode_stats['game_mode'], y=mode_stats['kd_ratio'], name='K/D Ratio', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # Kills per minute
    fig.add_trace(
        go.Bar(x=mode_stats['game_mode'], y=mode_stats['kills_per_minute'], name='Kills/Min', marker_color='#2ca02c'),
        row=2, col=1
    )
    
    # Score per minute
    fig.add_trace(
        go.Bar(x=mode_stats['game_mode'], y=mode_stats['score_per_minute'], name='Score/Min', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(
        title='Game Mode Analysis (Normalized by Match Length)',
        height=600,
        showlegend=False
    )
    
    return fig

def create_map_wise_analysis(df):
    """Create map-wise performance analysis"""
    if df.empty:
        return go.Figure()
    
    # Group by map and calculate stats
    map_stats = df.groupby('map_name').agg({
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_id': 'nunique',
        'player_name': 'nunique',
        'match_length': 'sum'  # Total minutes played
    }).reset_index()
    
    # Normalize by match length
    map_stats['kd_ratio'] = map_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    map_stats['kills_per_minute'] = map_stats['kills'] / map_stats['match_length']
    map_stats['score_per_minute'] = map_stats['score'] / map_stats['match_length']
    map_stats['avg_match_length'] = map_stats['match_length'] / map_stats['match_id']
    
    # Create heatmap data with normalized metrics
    heatmap_data = map_stats[['map_name', 'kd_ratio', 'kills_per_minute', 'score_per_minute']].set_index('map_name')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        text=heatmap_data.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Map Performance Heatmap (Per-Minute Metrics)',
        xaxis_title='Metrics',
        yaxis_title='Maps',
        height=400
    )
    
    return fig

def create_weapon_map_analysis(df):
    """Create weapon-map combination analysis"""
    if df.empty:
        return go.Figure()
    
    # Group by weapon and map
    weapon_map_stats = df.groupby(['weapon', 'map_name']).agg({
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_id': 'nunique',
        'match_length': 'sum'  # Total minutes played
    }).reset_index()
    
    # Normalize by match length
    weapon_map_stats['kd_ratio'] = weapon_map_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    weapon_map_stats['kills_per_minute'] = weapon_map_stats['kills'] / weapon_map_stats['match_length']
    weapon_map_stats['score_per_minute'] = weapon_map_stats['score'] / weapon_map_stats['match_length']
    
    # Create pivot table for heatmap
    pivot_kd = weapon_map_stats.pivot(index='map_name', columns='weapon', values='kd_ratio').fillna(0)
    pivot_kills_per_min = weapon_map_stats.pivot(index='map_name', columns='weapon', values='kills_per_minute').fillna(0)
    
    # Create subplots
    fig = sp.make_subplots(
        rows=1, cols=2,
        subplot_titles=('K/D Ratio by Weapon-Map', 'Kills per Minute by Weapon-Map'),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}]]
    )
    
    # K/D ratio heatmap
    fig.add_trace(
        go.Heatmap(
            z=pivot_kd.values,
            x=pivot_kd.columns,
            y=pivot_kd.index,
            colorscale='Reds',
            name='K/D Ratio',
            text=pivot_kd.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 10}
        ),
        row=1, col=1
    )
    
    # Kills per minute heatmap
    fig.add_trace(
        go.Heatmap(
            z=pivot_kills_per_min.values,
            x=pivot_kills_per_min.columns,
            y=pivot_kills_per_min.index,
            colorscale='Blues',
            name='Kills/Min',
            text=pivot_kills_per_min.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 10}
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title='Weapon-Map Effectiveness Analysis (Per-Minute Metrics)',
        height=500
    )
    
    return fig

def create_kd_leaderboard_chart(df, top_n=5):
    """Create K/D ratio leaderboard chart"""
    if df.empty:
        return go.Figure()
    
    leaderboard_data = []
    players = df['player_name'].unique()
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            leaderboard_data.append({
                'player': player,
                'kd_ratio': player_stats['kd_ratio'],
                'total_kills': player_stats['total_kills']
            })
    
    if not leaderboard_data:
        return go.Figure()
    
    leaderboard_df = pd.DataFrame(leaderboard_data)
    leaderboard_df = leaderboard_df.sort_values('kd_ratio', ascending=False).head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(
            x=leaderboard_df['player'],
            y=leaderboard_df['kd_ratio'],
            text=leaderboard_df['kd_ratio'],
            textposition='auto',
            marker_color='#1f77b4'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Players by K/D Ratio',
        xaxis_title='Player',
        yaxis_title='K/D Ratio',
        showlegend=False,
        height=400
    )
    
    return fig

def create_player_performance_trend(df, player_name):
    """Create player performance trend over time"""
    if df.empty or not player_name:
        return go.Figure()
    
    player_data = df[df['player_name'] == player_name].copy()
    if player_data.empty:
        return go.Figure()
    
    # Group by match and calculate stats
    match_stats = player_data.groupby('match_id').agg({
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'score': 'sum',
        'datetime': 'first',
        'match_length': 'first' # Add match_length here
    }).reset_index()
    
    match_stats['kd_ratio'] = match_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    match_stats['kills_per_minute'] = match_stats['kills'] / match_stats['match_length']
    match_stats['deaths_per_minute'] = match_stats['deaths'] / match_stats['match_length']
    match_stats['assists_per_minute'] = match_stats['assists'] / match_stats['match_length']
    match_stats['score_per_minute'] = match_stats['score'] / match_stats['match_length']
    
    fig = go.Figure()
    
    # Add traces for different metrics
    fig.add_trace(go.Scatter(
        x=match_stats['datetime'],
        y=match_stats['kills_per_minute'],
        mode='lines+markers',
        name='Kills/Min',
        line=dict(color='#ff7f0e')
    ))
    
    fig.add_trace(go.Scatter(
        x=match_stats['datetime'],
        y=match_stats['deaths_per_minute'],
        mode='lines+markers',
        name='Deaths/Min',
        line=dict(color='#d62728')
    ))
    
    # Add assists trace if assists data exists
    if 'assists' in match_stats.columns and not match_stats['assists'].isna().all():
        fig.add_trace(go.Scatter(
            x=match_stats['datetime'],
            y=match_stats['assists_per_minute'],
            mode='lines+markers',
            name='Assists/Min',
            line=dict(color='#9467bd')
        ))
    
    fig.add_trace(go.Scatter(
        x=match_stats['datetime'],
        y=match_stats['kd_ratio'],
        mode='lines+markers',
        name='K/D Ratio',
        line=dict(color='#2ca02c'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=f'{player_name} Performance Over Time (Per-Minute)',
        xaxis_title='Date',
        yaxis_title='Kills/Deaths/Assists/Score/K/D Ratio',
        yaxis2=dict(
            title='K/D Ratio',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig

def create_weapon_usage_chart(df):
    """Create weapon usage and performance chart"""
    if df.empty:
        return go.Figure()
    
    weapon_stats = get_weapon_stats(df)
    if not weapon_stats:
        return go.Figure()
    
    weapons = list(weapon_stats.keys())
    usage_counts = [weapon_stats[w]['usage_count'] for w in weapons]
    kd_ratios = [weapon_stats[w]['kd_ratio'] for w in weapons]
    
    fig = go.Figure(data=[
        go.Bar(
            x=weapons,
            y=usage_counts,
            name='Usage Count',
            yaxis='y'
        ),
        go.Scatter(
            x=weapons,
            y=kd_ratios,
            name='K/D Ratio',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red')
        )
    ])
    
    fig.update_layout(
        title='Weapon Usage and Performance',
        xaxis_title='Weapon',
        yaxis_title='Usage Count',
        yaxis2=dict(
            title='K/D Ratio',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig

def create_map_performance_chart(df):
    """Create map performance chart"""
    if df.empty:
        return go.Figure()
    
    map_stats = get_map_stats(df)
    if not map_stats:
        return go.Figure()
    
    maps = list(map_stats.keys())
    matches_played = [map_stats[m]['matches_played'] for m in maps]
    avg_kills = [map_stats[m]['avg_kills_per_match'] for m in maps]
    
    fig = go.Figure(data=[
        go.Bar(
            x=maps,
            y=matches_played,
            name='Matches Played',
            yaxis='y'
        ),
        go.Scatter(
            x=maps,
            y=avg_kills,
            name='Avg Kills per Match',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='orange')
        )
    ])
    
    fig.update_layout(
        title='Map Performance',
        xaxis_title='Map',
        yaxis_title='Matches Played',
        yaxis2=dict(
            title='Avg Kills per Match',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig

def create_team_performance_chart(df):
    """Create team performance chart"""
    if df.empty:
        return go.Figure()
    
    team_df = df[df['team'].notna()]
    if team_df.empty:
        return go.Figure()
    
    team_stats = {}
    for team in team_df['team'].unique():
        team_data = team_df[team_df['team'] == team]
        matches = team_data['match_id'].unique()
        
        wins = 0
        losses = 0
        
        for match_id in matches:
            match_data = team_data[team_data['match_id'] == match_id]
            other_teams = team_df[(team_df['match_id'] == match_id) & (team_df['team'] != team)]
            
            if not other_teams.empty:
                team_score = match_data['score'].sum()
                other_team_scores = other_teams.groupby('team')['score'].sum()
                max_other_score = other_team_scores.max()
                
                if team_score > max_other_score:
                    wins += 1
                elif team_score < max_other_score:
                    losses += 1
        
        team_stats[team] = {'wins': wins, 'losses': losses}
    
    if not team_stats:
        return go.Figure()
    
    teams = list(team_stats.keys())
    wins = [team_stats[t]['wins'] for t in teams]
    losses = [team_stats[t]['losses'] for t in teams]
    
    fig = go.Figure(data=[
        go.Bar(name='Wins', x=teams, y=wins, marker_color='green'),
        go.Bar(name='Losses', x=teams, y=losses, marker_color='red')
    ])
    
    fig.update_layout(
        title='Team Performance',
        xaxis_title='Team',
        yaxis_title='Matches',
        barmode='group',
        height=400
    )
    
    return fig

def create_player_comparison_radar(df, players):
    """Create radar chart comparing multiple players"""
    if df.empty or len(players) < 2:
        return go.Figure()
    
    categories = ['K/D Ratio', 'Win Rate', 'Avg Kills/Match', 'Avg Assists/Match', 'Total Score']
    
    fig = go.Figure()
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            values = [
                player_stats['kd_ratio'],
                player_stats['win_rate'],
                player_stats['avg_kills_per_match'],
                player_stats['avg_assists_per_match'],
                player_stats['total_score'] / 1000,  # Scale down for radar
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=player
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([get_player_stats(df, p).get('kd_ratio', 0) for p in players])]
            )),
        showlegend=True,
        title='Player Comparison',
        height=500
    )
    
    return fig

def create_match_timeline(df):
    """Create an improved match timeline chart with multiple metrics and trend analysis"""
    if df.empty:
        return go.Figure()
    
    # Group by match and calculate comprehensive stats
    agg_dict = {
        'datetime': 'first',
        'game_mode': 'first',
        'map_name': 'first',
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_length': 'first',
        'player_name': 'nunique'  # Number of players in match
    }
    
    # Add assists if the column exists
    if 'assists' in df.columns:
        agg_dict['assists'] = 'sum'
    
    match_summaries = df.groupby('match_id').agg(agg_dict).reset_index()
    
    # Calculate per-minute metrics
    match_summaries['kills_per_minute'] = match_summaries['kills'] / match_summaries['match_length']
    match_summaries['deaths_per_minute'] = match_summaries['deaths'] / match_summaries['match_length']
    match_summaries['score_per_minute'] = match_summaries['score'] / match_summaries['match_length']
    match_summaries['kd_ratio'] = match_summaries.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    
    # Normalize datetime to timezone-naive for consistent sorting
    match_summaries['datetime'] = pd.to_datetime(match_summaries['datetime'], errors='coerce')
    if hasattr(match_summaries['datetime'].dt, 'tz_localize'):
        if match_summaries['datetime'].dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in match_summaries['datetime'] if pd.notnull(x)):
            match_summaries['datetime'] = match_summaries['datetime'].dt.tz_localize(None)
    
    # Sort by datetime for proper timeline
    match_summaries = match_summaries.sort_values('datetime')
    
    # Create subplots for better organization
    fig = go.Figure()
    
    # Add multiple traces for different metrics
    # 1. Kills per minute (primary metric)
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['kills_per_minute'],
        mode='lines+markers',
        name='Kills/Min',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8, color='#1f77b4'),
        hovertemplate='<b>Match %{customdata[0]}</b><br>' +
                     'Kills/Min: %{y:.2f}<br>' +
                     'Mode: %{customdata[1]}<br>' +
                     'Map: %{customdata[2]}<br>' +
                     'Players: %{customdata[3]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name'],
                           match_summaries['player_name']))
    ))
    
    # 2. K/D Ratio (secondary metric on right y-axis)
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['kd_ratio'],
        mode='lines+markers',
        name='K/D Ratio',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=8, color='#ff7f0e'),
        yaxis='y2',
        hovertemplate='<b>Match %{customdata[0]}</b><br>' +
                     'K/D Ratio: %{y:.2f}<br>' +
                     'Mode: %{customdata[1]}<br>' +
                     'Map: %{customdata[2]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name']))
    ))
    
    # 3. Score per minute (tertiary metric)
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['score_per_minute'],
        mode='lines+markers',
        name='Score/Min',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=8, color='#2ca02c'),
        yaxis='y3',
        hovertemplate='<b>Match %{customdata[0]}</b><br>' +
                     'Score/Min: %{y:.1f}<br>' +
                     'Mode: %{customdata[1]}<br>' +
                     'Map: %{customdata[2]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name']))
    ))
    
    # Add trend lines using rolling averages
    if len(match_summaries) > 3:
        # Calculate rolling averages for trend lines
        window_size = min(5, len(match_summaries) // 2)
        
        # Kills per minute trend
        kills_trend = match_summaries['kills_per_minute'].rolling(window=window_size, center=True).mean()
        fig.add_trace(go.Scatter(
            x=match_summaries['datetime'],
            y=kills_trend,
            mode='lines',
            name=f'Kills/Min Trend ({window_size}-match avg)',
            line=dict(color='#1f77b4', width=3, dash='dash'),
            showlegend=True
        ))
        
        # K/D ratio trend
        kd_trend = match_summaries['kd_ratio'].rolling(window=window_size, center=True).mean()
        fig.add_trace(go.Scatter(
            x=match_summaries['datetime'],
            y=kd_trend,
            mode='lines',
            name=f'K/D Trend ({window_size}-match avg)',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            yaxis='y2',
            showlegend=True
        ))
    
    # Add performance zones (background coloring)
    if len(match_summaries) > 0:
        # Calculate performance thresholds
        avg_kills = match_summaries['kills_per_minute'].mean()
        avg_kd = match_summaries['kd_ratio'].mean()
        
        # Add performance zone annotations
        fig.add_annotation(
            x=match_summaries['datetime'].iloc[-1],
            y=avg_kills * 1.2,
            text="Above Avg",
            showarrow=False,
            bgcolor="rgba(0,255,0,0.3)",
            bordercolor="green",
            borderwidth=1
        )
        
        fig.add_annotation(
            x=match_summaries['datetime'].iloc[-1],
            y=avg_kills * 0.8,
            text="Below Avg",
            showarrow=False,
            bgcolor="rgba(255,0,0,0.3)",
            bordercolor="red",
            borderwidth=1
        )
    
    # Update layout with multiple y-axes and better styling
    fig.update_layout(
        title={
            'text': '📈 Match Performance Timeline',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Date',
        yaxis_title='Kills per Minute',
        yaxis2=dict(
            title='K/D Ratio',
            overlaying='y',
            side='right',
            range=[0, max(match_summaries['kd_ratio']) * 1.1]
        ),
        yaxis3=dict(
            title='Score per Minute',
            overlaying='y',
            side='right',
            position=0.95,
            range=[0, max(match_summaries['score_per_minute']) * 1.1]
        ),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='closest',
        # Add grid for better readability
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    # Add summary statistics in the corner
    if len(match_summaries) > 0:
        total_matches = len(match_summaries)
        avg_kills_per_min = match_summaries['kills_per_minute'].mean()
        avg_kd = match_summaries['kd_ratio'].mean()
        best_match = match_summaries.loc[match_summaries['kills_per_minute'].idxmax()]
        
        fig.add_annotation(
            x=0.02,
            y=0.98,
            xref='paper',
            yref='paper',
            text=f"📊 Summary:<br>Matches: {total_matches}<br>Avg Kills/Min: {avg_kills_per_min:.2f}<br>Avg K/D: {avg_kd:.2f}",
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
            align="left"
        )
    
    return fig

def create_detailed_match_timeline(df):
    """Create a detailed match timeline with individual match breakdowns and performance insights"""
    if df.empty:
        return go.Figure()
    
    # Group by match and calculate comprehensive stats
    agg_dict = {
        'datetime': 'first',
        'game_mode': 'first',
        'map_name': 'first',
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_length': 'first',
        'player_name': 'nunique',
        'weapon': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
    }
    
    # Add assists if the column exists
    if 'assists' in df.columns:
        agg_dict['assists'] = 'sum'
    
    match_summaries = df.groupby('match_id').agg(agg_dict).reset_index()
    
    # Calculate metrics
    match_summaries['kills_per_minute'] = match_summaries['kills'] / match_summaries['match_length']
    match_summaries['deaths_per_minute'] = match_summaries['deaths'] / match_summaries['match_length']
    match_summaries['score_per_minute'] = match_summaries['score'] / match_summaries['match_length']
    match_summaries['kd_ratio'] = match_summaries.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    match_summaries['efficiency'] = match_summaries['score'] / (match_summaries['kills'] + match_summaries['deaths']).replace(0, 1)
    
    # Normalize datetime to timezone-naive for consistent sorting
    match_summaries['datetime'] = pd.to_datetime(match_summaries['datetime'], errors='coerce')
    if hasattr(match_summaries['datetime'].dt, 'tz_localize'):
        if match_summaries['datetime'].dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in match_summaries['datetime'] if pd.notnull(x)):
            match_summaries['datetime'] = match_summaries['datetime'].dt.tz_localize(None)
    
    # Sort by datetime
    match_summaries = match_summaries.sort_values('datetime')
    
    # Create subplots for different aspects
    fig = sp.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Performance Metrics', 'Match Details', 'Performance Trends'),
        specs=[[{"type": "scatter"}],
               [{"type": "bar"}],
               [{"type": "scatter"}]],
        vertical_spacing=0.1,
        row_heights=[0.4, 0.3, 0.3]
    )
    
    # Subplot 1: Performance Metrics (Kills/Min, K/D Ratio, Score/Min)
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['kills_per_minute'],
        mode='lines+markers',
        name='Kills/Min',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8),
        hovertemplate='<b>Match %{customdata[0]}</b><br>Kills/Min: %{y:.2f}<br>Mode: %{customdata[1]}<br>Map: %{customdata[2]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name']))
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['kd_ratio'],
        mode='lines+markers',
        name='K/D Ratio',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='<b>Match %{customdata[0]}</b><br>K/D Ratio: %{y:.2f}<br>Mode: %{customdata[1]}<br>Map: %{customdata[2]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name']))
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=match_summaries['datetime'],
        y=match_summaries['score_per_minute'],
        mode='lines+markers',
        name='Score/Min',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=8),
        yaxis='y3',
        hovertemplate='<b>Match %{customdata[0]}</b><br>Score/Min: %{y:.1f}<br>Mode: %{customdata[1]}<br>Map: %{customdata[2]}<extra></extra>',
        customdata=list(zip(match_summaries['match_id'], 
                           match_summaries['game_mode'], 
                           match_summaries['map_name']))
    ), row=1, col=1)
    
    # Subplot 2: Match Details (Game Mode, Map, Players)
    # Create color mapping for game modes
    game_modes = match_summaries['game_mode'].unique()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    mode_colors = {mode: colors[i % len(colors)] for i, mode in enumerate(game_modes)}
    
    for mode in game_modes:
        mode_data = match_summaries[match_summaries['game_mode'] == mode]
        fig.add_trace(go.Bar(
            x=mode_data['datetime'],
            y=mode_data['player_name'],
            name=f'{mode} Players',
            marker_color=mode_colors[mode],
            opacity=0.7,
            hovertemplate='<b>Match %{customdata[0]}</b><br>Players: %{y}<br>Mode: %{customdata[1]}<br>Map: %{customdata[2]}<extra></extra>',
            customdata=list(zip(mode_data['match_id'], 
                               mode_data['game_mode'], 
                               mode_data['map_name']))
        ), row=2, col=1)
    
    # Subplot 3: Performance Trends with rolling averages
    if len(match_summaries) > 3:
        window_size = min(5, len(match_summaries) // 2)
        
        # Rolling averages
        kills_trend = match_summaries['kills_per_minute'].rolling(window=window_size, center=True).mean()
        kd_trend = match_summaries['kd_ratio'].rolling(window=window_size, center=True).mean()
        
        fig.add_trace(go.Scatter(
            x=match_summaries['datetime'],
            y=kills_trend,
            mode='lines',
            name=f'Kills/Min Trend ({window_size}-match avg)',
            line=dict(color='#1f77b4', width=3, dash='dash')
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=match_summaries['datetime'],
            y=kd_trend,
            mode='lines',
            name=f'K/D Trend ({window_size}-match avg)',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            yaxis='y6'
        ), row=3, col=1)
    
    # Update layout
    fig.update_layout(
        title={
            'text': '📊 Detailed Match Timeline Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        # Multiple y-axes for different metrics
        yaxis=dict(title='Kills per Minute'),
        yaxis2=dict(title='K/D Ratio', overlaying='y', side='right'),
        yaxis3=dict(title='Score per Minute', overlaying='y', side='right', position=0.95),
        yaxis4=dict(title='Number of Players', domain=[0.35, 0.65]),
        yaxis5=dict(title='Kills per Minute', domain=[0, 0.25]),
        yaxis6=dict(title='K/D Ratio', overlaying='y5', side='right', domain=[0, 0.25])
    )
    
    # Add performance insights
    if len(match_summaries) > 0:
        best_match = match_summaries.loc[match_summaries['kills_per_minute'].idxmax()]
        worst_match = match_summaries.loc[match_summaries['kills_per_minute'].idxmin()]
        avg_kills = match_summaries['kills_per_minute'].mean()
        avg_kd = match_summaries['kd_ratio'].mean()
        
        # Add insights as annotations
        fig.add_annotation(
            x=0.02,
            y=0.98,
            xref='paper',
            yref='paper',
            text=f"🏆 Best Match: {best_match['kills_per_minute']:.2f} kills/min<br>📉 Worst Match: {worst_match['kills_per_minute']:.2f} kills/min<br>📊 Avg Kills/Min: {avg_kills:.2f}<br>📊 Avg K/D: {avg_kd:.2f}",
            showarrow=False,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="black",
            borderwidth=1,
            align="left"
        )
    
    return fig

def create_ping_impact_chart(df):
    """Create ping impact on performance chart"""
    if df.empty or 'ping' not in df.columns:
        return go.Figure()
    
    ping_data = df[df['ping'].notna()].copy()
    if ping_data.empty:
        return go.Figure()
    
    # Create ping bins
    ping_data['ping_bin'] = pd.cut(ping_data['ping'], bins=5)
    ping_stats = ping_data.groupby('ping_bin').agg({
        'kills': 'mean',
        'deaths': 'mean',
        'score': 'mean',
        'match_length': 'sum' # Total minutes played
    }).reset_index()
    
    # Normalize by match length
    ping_stats['kd_ratio'] = ping_stats['kills'] / ping_stats['deaths'].replace(0, 1)
    ping_stats['kills_per_minute'] = ping_stats['kills'] / ping_stats['match_length']
    ping_stats['score_per_minute'] = ping_stats['score'] / ping_stats['match_length']
    
    fig = go.Figure(data=[
        go.Scatter(
            x=ping_stats['ping_bin'].astype(str),
            y=ping_stats['kd_ratio'],
            mode='lines+markers',
            name='K/D Ratio',
            line=dict(color='blue')
        ),
        go.Scatter(
            x=ping_stats['ping_bin'].astype(str),
            y=ping_stats['score_per_minute'],
            mode='lines+markers',
            name='Avg Score/Min',
            yaxis='y2',
            line=dict(color='red')
        )
    ])
    
    fig.update_layout(
        title='Ping Impact on Performance (Per-Minute)',
        xaxis_title='Ping Range',
        yaxis_title='K/D Ratio',
        yaxis2=dict(
            title='Avg Score/Min',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig 

def create_player_evolution_chart(df, player_name):
    """Create player evolution timeline with trend lines"""
    if df.empty or not player_name:
        return go.Figure()
    
    evolution_data = get_player_evolution_timeline(df, player_name)
    if not evolution_data:
        return go.Figure()
    
    # Convert to DataFrame for easier plotting
    evolution_df = pd.DataFrame(evolution_data)
    
    fig = go.Figure()
    
    # Add actual performance lines
    fig.add_trace(go.Scatter(
        x=evolution_df['datetime'],
        y=evolution_df['kd_ratio'],
        mode='markers',
        name='K/D Ratio',
        marker=dict(color='#1f77b4', size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=evolution_df['datetime'],
        y=evolution_df['kills_per_minute'],
        mode='markers',
        name='Kills/Min',
        marker=dict(color='#ff7f0e', size=8),
        yaxis='y2'
    ))
    
    # Add trend lines
    fig.add_trace(go.Scatter(
        x=evolution_df['datetime'],
        y=evolution_df['kd_trend'],
        mode='lines',
        name='K/D Trend',
        line=dict(color='#1f77b4', width=3, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=evolution_df['datetime'],
        y=evolution_df['kills_trend'],
        mode='lines',
        name='Kills/Min Trend',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=f'{player_name} Evolution Timeline',
        xaxis_title='Date',
        yaxis_title='K/D Ratio',
        yaxis2=dict(
            title='Kills per Minute',
            overlaying='y',
            side='right'
        ),
        height=500,
        showlegend=True
    )
    
    return fig

def create_performance_clusters_chart(df):
    """Create performance clusters visualization"""
    if df.empty:
        return go.Figure()
    
    cluster_stats = get_performance_clusters(df)
    if not cluster_stats:
        return go.Figure()
    
    # Create scatter plot of clusters
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for cluster_id, stats in cluster_stats.items():
        if stats['players']:
            fig.add_trace(go.Scatter(
                x=[stats['avg_kd_ratio']] * len(stats['players']),
                y=[stats['avg_kills_per_min']] * len(stats['players']),
                mode='markers',
                name=f'Cluster {cluster_id + 1}',
                text=stats['players'],
                marker=dict(
                    size=15,
                    color=colors[cluster_id % len(colors)],
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>K/D: %{x}<br>Kills/Min: %{y}<extra></extra>'
            ))
    
    fig.update_layout(
        title='Player Performance Clusters',
        xaxis_title='Average K/D Ratio',
        yaxis_title='Average Kills per Minute',
        height=500,
        showlegend=True
    )
    
    return fig

def create_streak_analysis_chart(df, player_name):
    """Create streak analysis visualization"""
    if df.empty or not player_name:
        return go.Figure()
    
    streak_data = get_player_streaks(df, player_name)
    if not streak_data:
        return go.Figure()
    
    # Create bar chart for streak analysis
    categories = ['Current Streak', 'Max Win Streak', 'Max Loss Streak']
    values = [streak_data['current_streak'], streak_data['max_win_streak'], streak_data['max_loss_streak']]
    colors = ['#2ca02c' if streak_data['current_streak'] > 0 else '#d62728', '#2ca02c', '#d62728']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=f'{player_name} Streak Analysis',
        xaxis_title='Streak Type',
        yaxis_title='Number of Matches',
        height=400,
        showlegend=False
    )
    
    return fig 

def create_team_chemistry_heatmap(df):
    """Create heatmap showing team chemistry between players"""
    if df.empty:
        return go.Figure()
    
    chemistry_matrix = get_team_chemistry_matrix(df)
    if not chemistry_matrix:
        return go.Figure()
    
    # Prepare data for heatmap
    players = list(chemistry_matrix.keys())
    z_data = []
    text_data = []
    
    for player1 in players:
        row = []
        text_row = []
        for player2 in players:
            if player1 == player2:
                row.append(None)  # Diagonal
                text_row.append("")
            elif chemistry_matrix[player1][player2]:
                row.append(chemistry_matrix[player1][player2]['chemistry_score'])
                text_row.append(f"{chemistry_matrix[player1][player2]['win_rate']:.1f}%")
            else:
                row.append(None)  # No data
                text_row.append("")
        z_data.append(row)
        text_data.append(text_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=players,
        y=players,
        colorscale='RdYlGn',
        zmid=0.5,
        text=text_data,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Team Chemistry Matrix (Win Rate %)',
        xaxis_title='Player',
        yaxis_title='Player',
        height=500,
        width=500
    )
    
    return fig

def create_role_analysis_chart(df):
    """Create radar chart showing player roles and strengths"""
    if df.empty:
        return go.Figure()
    
    role_analysis = get_player_role_analysis(df)
    if not role_analysis:
        return go.Figure()
    
    # Get unique roles
    roles = list(set([analysis['primary_role'] for analysis in role_analysis.values()]))
    role_colors = {
        'Killer': '#d62728',
        'Support': '#2ca02c',
        'Aggressive': '#ff7f0e',
        'Leader': '#1f77b4',
        'Balanced': '#9467bd'
    }
    
    fig = go.Figure()
    
    for player, analysis in role_analysis.items():
        role = analysis['primary_role']
        strengths = analysis['role_strengths']
        
        # Create radar chart data
        categories = ['Killing Power', 'Support Value', 'Survival Rate', 'Winning Ability', 'Consistency']
        values = [strengths['killing_power'], strengths['support_value'], strengths['survival_rate'], 
                 strengths['winning_ability'], strengths['consistency']]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=f"{player} ({role})",
            line_color=role_colors.get(role, '#666666'),
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Player Role Analysis",
        height=500
    )
    
    return fig

def create_team_formation_chart(df):
    """Create chart showing team formation performance"""
    if df.empty:
        return go.Figure()
    
    formation_stats = get_team_formation_performance(df)
    if not formation_stats:
        return go.Figure()
    
    # Prepare data for visualization
    formations = []
    win_rates = []
    match_counts = []
    avg_kills = []
    
    for formation_key, stats in formation_stats.items():
        formation_name = " + ".join(stats['players'])
        formations.append(formation_name)
        win_rates.append(stats['win_rate'])
        match_counts.append(stats['matches'])
        avg_kills.append(stats['avg_kills_per_match'])
    
    # Create bubble chart
    fig = go.Figure(data=[
        go.Scatter(
            x=win_rates,
            y=avg_kills,
            mode='markers',
            marker=dict(
                size=[count * 5 for count in match_counts],  # Size based on match count
                color=win_rates,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Win Rate %")
            ),
            text=formations,
            hovertemplate='<b>%{text}</b><br>Win Rate: %{x:.1f}%<br>Avg Kills: %{y:.1f}<br>Matches: %{marker.size}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Team Formation Performance',
        xaxis_title='Win Rate (%)',
        yaxis_title='Average Kills per Match',
        height=500,
        showlegend=False
    )
    
    return fig 

def create_battle_royale_rankings_chart(df):
    """Create battle royale style tournament bracket visualization"""
    if df.empty:
        return go.Figure()
    
    rankings_data = get_battle_royale_rankings(df)
    if not rankings_data:
        return go.Figure()
    
    tiers = rankings_data['tiers']
    tier_colors = {
        'Champion': '#FFD700',  # Gold
        'Elite': '#C0C0C0',     # Silver
        'Veteran': '#CD7F32',   # Bronze
        'Rookie': '#4CAF50',    # Green
        'Novice': '#2196F3'     # Blue
    }
    
    fig = go.Figure()
    
    # Create tier visualization
    y_positions = {'Champion': 5, 'Elite': 4, 'Veteran': 3, 'Rookie': 2, 'Novice': 1}
    
    for tier_name, players in tiers.items():
        if players:
            x_positions = list(range(len(players)))
            y_pos = [y_positions[tier_name]] * len(players)
            
            fig.add_trace(go.Scatter(
                x=x_positions,
                y=y_pos,
                mode='markers+text',
                marker=dict(
                    size=20,
                    color=tier_colors[tier_name],
                    symbol='diamond'
                ),
                text=[p['player_name'] for p in players],
                textposition='middle center',
                name=tier_name,
                hovertemplate='<b>%{text}</b><br>Ranking Score: %{customdata}<br>Tier: ' + tier_name + '<extra></extra>',
                customdata=[f"{p['ranking_score']:.1f}" for p in players]
            ))
    
    fig.update_layout(
        title='🏆 Battle Royale Rankings',
        xaxis_title='Player Position',
        yaxis_title='Tier',
        yaxis=dict(
            tickmode='array',
            tickvals=list(y_positions.values()),
            ticktext=list(y_positions.keys()),
            range=[0.5, 5.5]
        ),
        height=400,
        showlegend=True
    )
    
    return fig

def create_achievement_badges_chart(df):
    """Create achievement badges visualization"""
    if df.empty:
        return go.Figure()
    
    achievements_data = get_achievement_badges(df)
    if not achievements_data:
        return go.Figure()
    
    # Prepare data for visualization
    players = list(achievements_data.keys())
    unlocked_counts = [achievements_data[p]['unlocked_count'] for p in players]
    total_achievements = achievements_data[players[0]]['total_achievements']
    
    fig = go.Figure(data=[
        go.Bar(
            x=players,
            y=unlocked_counts,
            marker_color=['#4CAF50' if count == total_achievements else '#FFC107' if count > total_achievements/2 else '#F44336' for count in unlocked_counts],
            text=unlocked_counts,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Achievements: %{y}/' + str(total_achievements) + '<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='🏅 Achievement Badges Progress',
        xaxis_title='Player',
        yaxis_title='Achievements Unlocked',
        height=400,
        showlegend=False
    )
    
    return fig

def create_gaming_session_analysis_chart(df):
    """Create gaming session analysis visualization"""
    if df.empty:
        return go.Figure()
    
    session_data = get_gaming_session_analysis(df)
    if not session_data:
        return go.Figure()
    
    # Create subplots for different analyses
    fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Performance', 'Hourly Performance', 'Session Duration', 'Session Performance'),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Daily performance
    daily_stats = session_data['daily_stats']
    if daily_stats:
        dates = [d['date'] for d in daily_stats]
        kd_ratios = [d['kd_ratio'] for d in daily_stats]
        
        fig.add_trace(
            go.Scatter(x=dates, y=kd_ratios, mode='lines+markers', name='Daily K/D', line=dict(color='#1f77b4')),
            row=1, col=1
        )
    
    # Hourly performance
    hourly_data = session_data['hourly_performance']
    if hourly_data:
        hours = [h['hour'] for h in hourly_data]
        avg_kills = [h['kills'] for h in hourly_data]
        
        fig.add_trace(
            go.Bar(x=hours, y=avg_kills, name='Avg Kills/Hour', marker_color='#ff7f0e'),
            row=1, col=2
        )
    
    # Session duration
    session_analysis = session_data['session_analysis']
    if session_analysis:
        session_ids = list(session_analysis.keys())
        durations = [session_analysis[sid]['duration_days'] for sid in session_ids]
        
        fig.add_trace(
            go.Bar(x=[f"Session {sid}" for sid in session_ids], y=durations, name='Session Duration', marker_color='#2ca02c'),
            row=2, col=1
        )
    
    # Session performance
    if session_analysis:
        session_ids = list(session_analysis.keys())
        avg_kd_ratios = [session_analysis[sid]['avg_kd_ratio'] for sid in session_ids]
        
        fig.add_trace(
            go.Scatter(x=[f"Session {sid}" for sid in session_ids], y=avg_kd_ratios, mode='markers', name='Session K/D', marker=dict(size=10, color='#d62728')),
            row=2, col=2
        )
    
    fig.update_layout(
        title='🎮 Gaming Session Analysis',
        height=600,
        showlegend=True
    )
    
    return fig

def create_achievement_details(df, player_name):
    """Create detailed achievement progress for a specific player"""
    if df.empty or not player_name:
        return go.Figure()
    
    achievements_data = get_achievement_badges(df)
    if not achievements_data or player_name not in achievements_data:
        return go.Figure()
    
    player_achievements = achievements_data[player_name]['achievements']
    
    # Prepare data for visualization
    badge_names = [a['name'] for a in player_achievements]
    progress_values = [a['progress'] for a in player_achievements]
    unlocked = [a['unlocked'] for a in player_achievements]
    
    # Color coding
    colors = ['#4CAF50' if unlocked else '#FFC107' for unlocked in unlocked]
    
    fig = go.Figure(data=[
        go.Bar(
            x=badge_names,
            y=progress_values,
            marker_color=colors,
            text=[f"{p:.0f}%" for p in progress_values],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Progress: %{y:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'🏅 {player_name} Achievement Progress',
        xaxis_title='Achievement',
        yaxis_title='Progress (%)',
        height=400,
        showlegend=False,
        yaxis=dict(range=[0, 100])
    )
    
    return fig 

def create_player_comparison_chart(df, player1, player2):
    """Create side-by-side comparison chart for two players"""
    if df.empty or not player1 or not player2:
        return go.Figure()
    
    comparison_data = get_player_comparison_data(df, player1, player2)
    if not comparison_data:
        return go.Figure()
    
    # Prepare data for comparison
    metrics = ['K/D Ratio', 'Win Rate (%)', 'Kills/Min', 'Assists/Min', 'Total Matches', 'Total Kills']
    player1_values = [
        comparison_data['player1']['stats']['kd_ratio'],
        comparison_data['player1']['stats']['win_rate'],
        comparison_data['player1']['stats']['kills_per_minute'],
        comparison_data['player1']['stats']['assists_per_minute'],
        comparison_data['player1']['stats']['total_matches'],
        comparison_data['player1']['stats']['total_kills']
    ]
    player2_values = [
        comparison_data['player2']['stats']['kd_ratio'],
        comparison_data['player2']['stats']['win_rate'],
        comparison_data['player2']['stats']['kills_per_minute'],
        comparison_data['player2']['stats']['assists_per_minute'],
        comparison_data['player2']['stats']['total_matches'],
        comparison_data['player2']['stats']['total_kills']
    ]
    
    fig = go.Figure()
    
    # Add bars for player 1
    fig.add_trace(go.Bar(
        name=player1,
        x=metrics,
        y=player1_values,
        marker_color='#1f77b4',
        text=[f"{v:.2f}" if isinstance(v, float) else str(v) for v in player1_values],
        textposition='auto'
    ))
    
    # Add bars for player 2
    fig.add_trace(go.Bar(
        name=player2,
        x=metrics,
        y=player2_values,
        marker_color='#ff7f0e',
        text=[f"{v:.2f}" if isinstance(v, float) else str(v) for v in player2_values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title=f'Player Comparison: {player1} vs {player2}',
        xaxis_title='Metrics',
        yaxis_title='Values',
        barmode='group',
        height=500,
        showlegend=True
    )
    
    return fig

def create_scenario_simulation_chart(df, team_composition, opponent_composition=None):
    """Create scenario simulation visualization"""
    if df.empty or not team_composition:
        return go.Figure()
    
    team_performance = simulate_team_scenario(df, team_composition, opponent_composition)
    if not team_performance:
        return go.Figure()
    
    # Create radar chart for team performance
    categories = ['Avg K/D Ratio', 'Win Rate', 'Kills/Min', 'Assists/Min', 'Synergy Score']
    values = [
        team_performance['avg_kd_ratio'],
        team_performance['predicted_win_rate'],
        team_performance['total_kills_per_min'],
        team_performance['total_assists_per_min'],
        team_performance['synergy_score']
    ]
    
    # Normalize values for radar chart (0-1 scale)
    max_values = [3.0, 100, 2.0, 1.0, 100]  # Expected maximums
    normalized_values = [min(v / max_val, 1.0) for v, max_val in zip(values, max_values)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=categories,
        fill='toself',
        name='Team Performance',
        line_color='#1f77b4'
    ))
    
    # If opponent is provided, add comparison
    if opponent_composition and 'head_to_head_win_rate' in team_performance:
        opponent_performance = simulate_team_scenario(df, opponent_composition)
        if opponent_performance:
            opponent_values = [
                opponent_performance['avg_kd_ratio'],
                opponent_performance['predicted_win_rate'],
                opponent_performance['total_kills_per_min'],
                opponent_performance['total_assists_per_min'],
                opponent_performance['synergy_score']
            ]
            opponent_normalized = [min(v / max_val, 1.0) for v, max_val in zip(opponent_values, max_values)]
            
            fig.add_trace(go.Scatterpolar(
                r=opponent_normalized,
                theta=categories,
                fill='toself',
                name='Opponent Performance',
                line_color='#ff7f0e'
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title='Team Scenario Simulation',
        height=500
    )
    
    return fig

def create_optimal_team_chart(df, available_players, team_size=3):
    """Create visualization for optimal team composition"""
    if df.empty or len(available_players) < team_size:
        return go.Figure()
    
    optimal_data = get_optimal_team_composition(df, available_players, team_size)
    if not optimal_data:
        return go.Figure()
    
    # Get top 10 teams by score
    sorted_teams = sorted(optimal_data['all_teams'].items(), key=lambda x: x[1]['score'], reverse=True)[:10]
    
    team_names = [f"Team {i+1}" for i in range(len(sorted_teams))]
    team_scores = [team[1]['score'] for team in sorted_teams]
    win_rates = [team[1]['performance']['predicted_win_rate'] for team in sorted_teams]
    synergy_scores = [team[1]['performance']['synergy_score'] for team in sorted_teams]
    
    fig = go.Figure()
    
    # Create bubble chart
    fig.add_trace(go.Scatter(
        x=win_rates,
        y=synergy_scores,
        mode='markers',
        marker=dict(
            size=[score * 2 for score in team_scores],  # Size based on overall score
            color=team_scores,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Team Score")
        ),
        text=team_names,
        hovertemplate='<b>%{text}</b><br>Win Rate: %{x:.1f}%<br>Synergy: %{y:.1f}<br>Score: %{marker.color:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Optimal Team Compositions',
        xaxis_title='Predicted Win Rate (%)',
        yaxis_title='Synergy Score',
        height=500,
        showlegend=False
    )
    
    return fig 