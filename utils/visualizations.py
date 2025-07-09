import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from utils.calculations import get_player_stats, get_weapon_stats, get_map_stats

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
        'datetime': 'first'
    }).reset_index()
    
    match_stats['kd_ratio'] = match_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    
    fig = go.Figure()
    
    # Add traces for different metrics
    fig.add_trace(go.Scatter(
        x=match_stats['datetime'],
        y=match_stats['kills'],
        mode='lines+markers',
        name='Kills',
        line=dict(color='#ff7f0e')
    ))
    
    fig.add_trace(go.Scatter(
        x=match_stats['datetime'],
        y=match_stats['deaths'],
        mode='lines+markers',
        name='Deaths',
        line=dict(color='#d62728')
    ))
    
    # Add assists trace if assists data exists
    if 'assists' in match_stats.columns and not match_stats['assists'].isna().all():
        fig.add_trace(go.Scatter(
            x=match_stats['datetime'],
            y=match_stats['assists'],
            mode='lines+markers',
            name='Assists',
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
        title=f'{player_name} Performance Over Time',
        xaxis_title='Date',
        yaxis_title='Kills/Deaths/Assists',
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
                other_score = other_teams['score'].sum()
                
                if team_score > other_score:
                    wins += 1
                else:
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
    
    categories = ['K/D Ratio', 'Avg Kills/Match', 'Avg Assists/Match', 'Total Score', 'Total Matches']
    
    fig = go.Figure()
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            values = [
                player_stats['kd_ratio'],
                player_stats['avg_kills_per_match'],
                player_stats['avg_assists_per_match'],
                player_stats['total_score'] / 1000,  # Scale down for radar
                player_stats['total_matches']
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
        'score': 'sum'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Scatter(
            x=match_summaries['datetime'],
            y=match_summaries['kills'],
            mode='markers',
            marker=dict(
                size=match_summaries['score'] / 100,
                color=match_summaries['deaths'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Deaths')
            ),
            text=[f"Match {row['match_id']}<br>{row['game_mode']} - {row['map_name']}<br>Kills: {row['kills']}<br>Score: {row['score']}" 
                  for _, row in match_summaries.iterrows()],
            hovertemplate='%{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Match Timeline',
        xaxis_title='Date',
        yaxis_title='Total Kills',
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
        'score': 'mean'
    }).reset_index()
    
    ping_stats['kd_ratio'] = ping_stats['kills'] / ping_stats['deaths'].replace(0, 1)
    
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
            y=ping_stats['score'],
            mode='lines+markers',
            name='Avg Score',
            yaxis='y2',
            line=dict(color='red')
        )
    ])
    
    fig.update_layout(
        title='Ping Impact on Performance',
        xaxis_title='Ping Range',
        yaxis_title='K/D Ratio',
        yaxis2=dict(
            title='Avg Score',
            overlaying='y',
            side='right'
        ),
        height=400,
        showlegend=True
    )
    
    return fig 