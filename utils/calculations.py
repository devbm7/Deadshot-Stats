import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def calculate_kd_ratio(kills, deaths):
    """Calculate K/D ratio"""
    if deaths == 0:
        return kills if kills > 0 else 0
    return round(kills / deaths, 2)

def get_player_evolution_timeline(df, player_name):
    """Get player evolution data over time with trend analysis"""
    if df.empty or not player_name:
        return {}
    
    player_data = df[df['player_name'] == player_name].copy()
    if player_data.empty:
        return {}
    
    # Group by match and calculate per-minute stats
    match_stats = player_data.groupby('match_id').agg({
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'score': 'sum',
        'datetime': 'first',
        'match_length': 'first'
    }).reset_index()
    
    # Calculate per-minute metrics
    match_stats['kd_ratio'] = match_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    match_stats['kills_per_minute'] = match_stats['kills'] / match_stats['match_length']
    match_stats['deaths_per_minute'] = match_stats['deaths'] / match_stats['match_length']
    match_stats['assists_per_minute'] = match_stats['assists'] / match_stats['match_length']
    match_stats['score_per_minute'] = match_stats['score'] / match_stats['match_length']
    
    # Sort by datetime
    match_stats = match_stats.sort_values('datetime')
    
    # Calculate moving averages for trend analysis
    match_stats['kd_trend'] = match_stats['kd_ratio'].rolling(window=3, min_periods=1).mean()
    match_stats['kills_trend'] = match_stats['kills_per_minute'].rolling(window=3, min_periods=1).mean()
    match_stats['score_trend'] = match_stats['score_per_minute'].rolling(window=3, min_periods=1).mean()
    
    return match_stats.to_dict('records')

def get_performance_clusters(df, n_clusters=3):
    """Group players by similar playing styles using clustering"""
    if df.empty:
        return {}
    
    # Get player stats for clustering
    players = df['player_name'].unique()
    player_features = []
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            features = {
                'player_name': player,
                'kd_ratio': player_stats['kd_ratio'],
                'kills_per_minute': player_stats['kills_per_minute'],
                'deaths_per_minute': player_stats['deaths_per_minute'],
                'assists_per_minute': player_stats['assists_per_minute'],
                'score_per_minute': player_stats['score_per_minute'],
                'win_rate': player_stats['win_rate'],
                'total_matches': player_stats['total_matches']
            }
            player_features.append(features)
    
    if len(player_features) < n_clusters:
        return {}
    
    # Create feature matrix for clustering
    feature_df = pd.DataFrame(player_features)
    feature_matrix = feature_df[['kd_ratio', 'kills_per_minute', 'deaths_per_minute', 
                               'assists_per_minute', 'score_per_minute', 'win_rate']].values
    
    # Standardize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_matrix)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_features)
    
    # Add cluster labels to player data
    feature_df['cluster'] = clusters
    
    # Calculate cluster characteristics
    cluster_stats = {}
    for cluster_id in range(n_clusters):
        cluster_players = feature_df[feature_df['cluster'] == cluster_id]
        cluster_stats[cluster_id] = {
            'players': cluster_players['player_name'].tolist(),
            'avg_kd_ratio': round(cluster_players['kd_ratio'].mean(), 2),
            'avg_kills_per_min': round(cluster_players['kills_per_minute'].mean(), 2),
            'avg_assists_per_min': round(cluster_players['assists_per_minute'].mean(), 2),
            'avg_win_rate': round(cluster_players['win_rate'].mean(), 1),
            'cluster_size': len(cluster_players)
        }
    
    return cluster_stats

def get_player_streaks(df, player_name):
    """Analyze win/loss streaks and performance patterns"""
    if df.empty or not player_name:
        return {}
    
    player_matches = df[df['player_name'] == player_name]['match_id'].unique()
    match_results = []
    
    for match_id in player_matches:
        match_data = df[df['match_id'] == match_id]
        game_mode = match_data.iloc[0]['game_mode']
        
        # Determine if player won this match
        if game_mode == 'Team':
            player_team = match_data[match_data['player_name'] == player_name]['team'].iloc[0]
            team_score = match_data[match_data['team'] == player_team]['score'].sum()
            other_teams = match_data[match_data['team'] != player_team]
            
            if not other_teams.empty:
                other_team_scores = other_teams.groupby('team')['score'].sum()
                max_other_score = other_team_scores.max()
                won = team_score > max_other_score
            else:
                won = False
        else:
            # FFA match
            player_score = match_data[match_data['player_name'] == player_name]['score'].iloc[0]
            max_score = match_data['score'].max()
            won = player_score == max_score
        
        match_results.append({
            'match_id': match_id,
            'won': won,
            'datetime': match_data.iloc[0]['datetime']
        })
    
    # Sort by datetime
    match_results.sort(key=lambda x: x['datetime'])
    
    # Calculate streaks
    current_streak = 0
    max_win_streak = 0
    max_loss_streak = 0
    current_win_streak = 0
    current_loss_streak = 0
    win_streaks = []
    loss_streaks = []
    
    for result in match_results:
        if result['won']:
            current_win_streak += 1
            current_loss_streak = 0
            if current_win_streak > max_win_streak:
                max_win_streak = current_win_streak
        else:
            current_loss_streak += 1
            current_win_streak = 0
            if current_loss_streak > max_loss_streak:
                max_loss_streak = current_loss_streak
    
    # Calculate current streak
    if match_results:
        current_streak = current_win_streak if match_results[-1]['won'] else -current_loss_streak
    
    # Calculate win rate in recent matches
    recent_matches = match_results[-10:] if len(match_results) >= 10 else match_results
    recent_win_rate = sum(1 for r in recent_matches if r['won']) / len(recent_matches) * 100
    
    return {
        'current_streak': current_streak,
        'max_win_streak': max_win_streak,
        'max_loss_streak': max_loss_streak,
        'recent_win_rate': round(recent_win_rate, 1),
        'total_matches': len(match_results),
        'total_wins': sum(1 for r in match_results if r['won']),
        'total_losses': sum(1 for r in match_results if not r['won'])
    }

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
    
    # Calculate total time played
    total_minutes = player_df['match_length'].sum()
    
    stats = {
        'total_matches': len(player_df['match_id'].unique()),
        'total_kills': int(player_df['kills'].sum()),
        'total_deaths': int(player_df['deaths'].sum()),
        'total_assists': int(player_df['assists'].sum()) if 'assists' in player_df.columns and not player_df['assists'].isna().all() else 0,
        'total_score': int(player_df['score'].sum()),
        'total_coins': int(player_df['coins'].sum()) if 'coins' in player_df.columns else 0,
        'total_minutes': int(total_minutes),
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'avg_kills_per_match': round(player_df.groupby('match_id')['kills'].sum().mean(), 1),
        'avg_deaths_per_match': round(player_df.groupby('match_id')['deaths'].sum().mean(), 1),
        'avg_assists_per_match': round(player_df.groupby('match_id')['assists'].sum().mean(), 1) if 'assists' in player_df.columns and not player_df['assists'].isna().all() else 0,
        'avg_score_per_match': round(player_df.groupby('match_id')['score'].sum().mean(), 1),
        'kills_per_minute': round(player_df['kills'].sum() / total_minutes, 2) if total_minutes > 0 else 0,
        'deaths_per_minute': round(player_df['deaths'].sum() / total_minutes, 2) if total_minutes > 0 else 0,
        'assists_per_minute': round(player_df['assists'].sum() / total_minutes, 2) if 'assists' in player_df.columns and not player_df['assists'].isna().all() and total_minutes > 0 else 0,
        'score_per_minute': round(player_df['score'].sum() / total_minutes, 2) if total_minutes > 0 else 0,
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