import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from utils.calculations import get_player_stats, get_weapon_stats, get_map_stats, get_performance_clusters, get_player_streaks, get_player_evolution_timeline

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

def create_kd_leaderboard_chart(df, top_n=10):
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
    """Create match timeline chart"""
    if df.empty:
        return go.Figure()
    
    match_summaries = df.groupby('match_id').agg({
        'datetime': 'first',
        'game_mode': 'first',
        'map_name': 'first',
        'kills': 'sum',
        'deaths': 'sum',
        'score': 'sum',
        'match_length': 'first' # Add match_length here
    }).reset_index()
    
    match_summaries['kills_per_minute'] = match_summaries['kills'] / match_summaries['match_length']
    match_summaries['deaths_per_minute'] = match_summaries['deaths'] / match_summaries['match_length']
    match_summaries['score_per_minute'] = match_summaries['score'] / match_summaries['match_length']
    
    fig = go.Figure(data=[
        go.Scatter(
            x=match_summaries['datetime'],
            y=match_summaries['kills_per_minute'],
            mode='markers',
            marker=dict(
                size=match_summaries['score_per_minute'] * 10, # Scale size by score per minute
                color=match_summaries['deaths_per_minute'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Deaths/Min')
            ),
            text=[f"Match {row['match_id']}<br>{row['game_mode']} - {row['map_name']}<br>Kills: {row['kills']}<br>Score: {row['score']}" 
                  for _, row in match_summaries.iterrows()],
            hovertemplate='%{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Match Timeline (Per-Minute)',
        xaxis_title='Date',
        yaxis_title='Kills/Deaths/Score/Kills/Min',
        height=400
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