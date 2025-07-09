import pandas as pd
import numpy as np

def calculate_kd_ratio(kills, deaths):
    """Calculate K/D ratio"""
    if deaths == 0:
        return kills if kills > 0 else 0
    return round(kills / deaths, 2)

def calculate_accuracy(kills, deaths):
    """Calculate accuracy (kills / (kills + deaths))"""
    total = kills + deaths
    if total == 0:
        return 0
    return round((kills / total) * 100, 1)

def get_player_stats(df, player_name=None):
    """Get comprehensive player statistics"""
    if df.empty:
        return {}
    
    if player_name:
        player_df = df[df['player_name'] == player_name]
    else:
        player_df = df
    
    if player_df.empty:
        return {}
    
    stats = {
        'total_matches': len(player_df['match_id'].unique()),
        'total_kills': int(player_df['kills'].sum()),
        'total_deaths': int(player_df['deaths'].sum()),
        'total_assists': int(player_df['assists'].sum()) if 'assists' in player_df.columns else 0,
        'total_score': int(player_df['score'].sum()),
        'total_coins': int(player_df['coins'].sum()) if 'coins' in player_df.columns else 0,
        'avg_kills_per_match': round(player_df.groupby('match_id')['kills'].sum().mean(), 1),
        'avg_deaths_per_match': round(player_df.groupby('match_id')['deaths'].sum().mean(), 1),
        'avg_score_per_match': round(player_df.groupby('match_id')['score'].sum().mean(), 1),
        'kd_ratio': calculate_kd_ratio(player_df['kills'].sum(), player_df['deaths'].sum()),
        'accuracy': calculate_accuracy(player_df['kills'].sum(), player_df['deaths'].sum()),
        'best_match_kills': int(player_df.groupby('match_id')['kills'].sum().max()),
        'best_match_score': int(player_df.groupby('match_id')['score'].sum().max()),
        'favorite_weapon': player_df['weapon'].mode().iloc[0] if not player_df['weapon'].mode().empty else 'Unknown',
        'avg_ping': round(player_df['ping'].mean(), 1) if 'ping' in player_df.columns and not player_df['ping'].isna().all() else None
    }
    
    return stats

def get_team_stats(df):
    """Get team performance statistics"""
    if df.empty or 'team' not in df.columns:
        return {}
    
    team_df = df[df['team'].notna()]
    if team_df.empty:
        return {}
    
    team_stats = {}
    
    for team in team_df['team'].unique():
        team_data = team_df[team_df['team'] == team]
        matches = team_data['match_id'].unique()
        
        team_wins = 0
        team_losses = 0
        
        for match_id in matches:
            match_data = team_data[team_data['match_id'] == match_id]
            other_teams = team_df[(team_df['match_id'] == match_id) & (team_df['team'] != team)]
            
            if not other_teams.empty:
                team_score = match_data['score'].sum()
                other_score = other_teams['score'].sum()
                
                if team_score > other_score:
                    team_wins += 1
                else:
                    team_losses += 1
        
        team_stats[team] = {
            'matches': len(matches),
            'wins': team_wins,
            'losses': team_losses,
            'win_rate': round((team_wins / (team_wins + team_losses)) * 100, 1) if (team_wins + team_losses) > 0 else 0,
            'total_kills': int(team_data['kills'].sum()),
            'total_deaths': int(team_data['deaths'].sum()),
            'total_score': int(team_data['score'].sum()),
            'avg_score_per_match': round(team_data.groupby('match_id')['score'].sum().mean(), 1)
        }
    
    return team_stats

def get_leaderboard_data(df, metric='kd_ratio'):
    """Get leaderboard data for various metrics"""
    if df.empty:
        return pd.DataFrame()
    
    players = df['player_name'].unique()
    leaderboard_data = []
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            leaderboard_data.append({
                'player_name': player,
                'kd_ratio': player_stats['kd_ratio'],
                'accuracy': player_stats['accuracy'],
                'total_kills': player_stats['total_kills'],
                'avg_kills_per_match': player_stats['avg_kills_per_match'],
                'total_score': player_stats['total_score'],
                'total_coins': player_stats['total_coins'],
                'total_matches': player_stats['total_matches']
            })
    
    if leaderboard_data:
        leaderboard_df = pd.DataFrame(leaderboard_data)
        return leaderboard_df.sort_values(metric, ascending=False)
    
    return pd.DataFrame()

def get_weapon_stats(df):
    """Get weapon usage and performance statistics"""
    if df.empty:
        return {}
    
    weapon_stats = {}
    
    for weapon in df['weapon'].unique():
        weapon_data = df[df['weapon'] == weapon]
        
        weapon_stats[weapon] = {
            'usage_count': len(weapon_data),
            'total_kills': int(weapon_data['kills'].sum()),
            'total_deaths': int(weapon_data['deaths'].sum()),
            'avg_kills_per_use': round(weapon_data['kills'].mean(), 1),
            'kd_ratio': calculate_kd_ratio(weapon_data['kills'].sum(), weapon_data['deaths'].sum()),
            'accuracy': calculate_accuracy(weapon_data['kills'].sum(), weapon_data['deaths'].sum()),
            'avg_score': round(weapon_data['score'].mean(), 1)
        }
    
    return weapon_stats

def get_map_stats(df):
    """Get map performance statistics"""
    if df.empty:
        return {}
    
    map_stats = {}
    
    for map_name in df['map_name'].unique():
        map_data = df[df['map_name'] == map_name]
        
        map_stats[map_name] = {
            'matches_played': len(map_data['match_id'].unique()),
            'total_kills': int(map_data['kills'].sum()),
            'total_deaths': int(map_data['deaths'].sum()),
            'avg_kills_per_match': round(map_data.groupby('match_id')['kills'].sum().mean(), 1),
            'avg_score_per_match': round(map_data.groupby('match_id')['score'].sum().mean(), 1)
        }
    
    return map_stats

def get_recent_activity(df, days=7):
    """Get recent activity summary"""
    if df.empty:
        return {}
    
    recent_date = df['datetime'].max() - pd.Timedelta(days=days)
    recent_data = df[df['datetime'] >= recent_date]
    
    return {
        'recent_matches': len(recent_data['match_id'].unique()),
        'recent_players': len(recent_data['player_name'].unique()),
        'recent_kills': int(recent_data['kills'].sum()),
        'most_active_player': recent_data['player_name'].mode().iloc[0] if not recent_data['player_name'].mode().empty else 'None',
        'recent_weapons': recent_data['weapon'].value_counts().head(3).to_dict()
    }

def get_match_summary(df, match_id):
    """Get detailed summary for a specific match"""
    if df.empty:
        return {}
    
    match_data = df[df['match_id'] == match_id]
    if match_data.empty:
        return {}
    
    match_info = match_data.iloc[0]
    
    summary = {
        'match_id': match_id,
        'datetime': match_info['datetime'],
        'game_mode': match_info['game_mode'],
        'map_name': match_info['map_name'],
        'total_players': len(match_data),
        'total_kills': int(match_data['kills'].sum()),
        'total_deaths': int(match_data['deaths'].sum()),
        'total_score': int(match_data['score'].sum()),
        'winner': match_data.loc[match_data['score'].idxmax(), 'player_name'] if match_data['score'].max() > 0 else 'None',
        'top_killer': match_data.loc[match_data['kills'].idxmax(), 'player_name'] if match_data['kills'].max() > 0 else 'None',
        'players': match_data[['player_name', 'kills', 'deaths', 'assists', 'score', 'weapon']].to_dict('records')
    }
    
    return summary 