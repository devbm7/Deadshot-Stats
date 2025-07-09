import pandas as pd
import numpy as np

def calculate_kd_ratio(kills, deaths):
    """Calculate K/D ratio"""
    if deaths == 0:
        return kills if kills > 0 else 0
    return round(kills / deaths, 2)

def calculate_player_wins(df, player_name):
    """Calculate wins for a player"""
    if df.empty:
        return 0, 0, 0.0
    
    player_matches = df[df['player_name'] == player_name]['match_id'].unique()
    wins = 0
    losses = 0
    
    for match_id in player_matches:
        match_data = df[df['match_id'] == match_id]
        game_mode = match_data.iloc[0]['game_mode']
        
        if game_mode == 'Team':
            # For team matches, determine winner by team score
            player_team = match_data[match_data['player_name'] == player_name]['team'].iloc[0]
            team_score = match_data[match_data['team'] == player_team]['score'].sum()
            other_teams = match_data[match_data['team'] != player_team]
            
            if not other_teams.empty:
                other_team_scores = other_teams.groupby('team')['score'].sum()
                max_other_score = other_team_scores.max()
                
                if team_score > max_other_score:
                    wins += 1
                elif team_score < max_other_score:
                    losses += 1
                # If equal, it's a draw (no change to wins/losses)
        else:
            # For FFA matches, determine winner by individual score
            player_score = match_data[match_data['player_name'] == player_name]['score'].iloc[0]
            max_score = match_data['score'].max()
            
            if player_score == max_score:
                wins += 1
            else:
                losses += 1
    
    win_rate = round((wins / (wins + losses)) * 100, 1) if (wins + losses) > 0 else 0.0
    return wins, losses, win_rate

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
    
    # Calculate wins/losses for the player
    wins, losses, win_rate = calculate_player_wins(df, player_name)
    
    stats = {
        'total_matches': len(player_df['match_id'].unique()),
        'total_kills': int(player_df['kills'].sum()),
        'total_deaths': int(player_df['deaths'].sum()),
        'total_assists': int(player_df['assists'].sum()) if 'assists' in player_df.columns and not player_df['assists'].isna().all() else 0,
        'total_score': int(player_df['score'].sum()),
        'total_coins': int(player_df['coins'].sum()) if 'coins' in player_df.columns else 0,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'avg_kills_per_match': round(player_df.groupby('match_id')['kills'].sum().mean(), 1),
        'avg_deaths_per_match': round(player_df.groupby('match_id')['deaths'].sum().mean(), 1),
        'avg_assists_per_match': round(player_df.groupby('match_id')['assists'].sum().mean(), 1) if 'assists' in player_df.columns and not player_df['assists'].isna().all() else 0,
        'avg_score_per_match': round(player_df.groupby('match_id')['score'].sum().mean(), 1),
        'kd_ratio': calculate_kd_ratio(player_df['kills'].sum(), player_df['deaths'].sum()),
        'best_match_kills': int(player_df.groupby('match_id')['kills'].sum().max()),
        'best_match_score': int(player_df.groupby('match_id')['score'].sum().max()),
        'best_match_assists': int(player_df.groupby('match_id')['assists'].sum().max()) if 'assists' in player_df.columns and not player_df['assists'].isna().all() else 0,
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
                other_team_scores = other_teams.groupby('team')['score'].sum()
                max_other_score = other_team_scores.max()
                
                if team_score > max_other_score:
                    team_wins += 1
                elif team_score < max_other_score:
                    team_losses += 1
                # If equal, it's a draw (no change to wins/losses)
        
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
                'total_kills': player_stats['total_kills'],
                'total_assists': player_stats['total_assists'],
                'wins': player_stats['wins'],
                'losses': player_stats['losses'],
                'win_rate': player_stats['win_rate'],
                'avg_kills_per_match': player_stats['avg_kills_per_match'],
                'avg_assists_per_match': player_stats['avg_assists_per_match'],
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
    game_mode = match_info['game_mode']
    
    # Determine winner
    if game_mode == 'Team':
        team_scores = match_data.groupby('team')['score'].sum()
        winning_team = team_scores.idxmax()
        winner = f"Team {winning_team}"
    else:
        # FFA match
        winner = match_data.loc[match_data['score'].idxmax(), 'player_name']
    
    summary = {
        'match_id': match_id,
        'datetime': match_info['datetime'],
        'game_mode': game_mode,
        'map_name': match_info['map_name'],
        'total_players': len(match_data),
        'total_kills': int(match_data['kills'].sum()),
        'total_deaths': int(match_data['deaths'].sum()),
        'total_score': int(match_data['score'].sum()),
        'winner': winner,
        'top_killer': match_data.loc[match_data['kills'].idxmax(), 'player_name'] if match_data['kills'].max() > 0 else 'None',
        'players': match_data[['player_name', 'kills', 'deaths', 'assists', 'score', 'weapon']].to_dict('records')
    }
    
    return summary 