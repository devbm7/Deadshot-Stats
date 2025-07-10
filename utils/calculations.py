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
    
    # Normalize all datetimes to tz-naive for sorting
    match_stats['datetime'] = pd.to_datetime(match_stats['datetime'], errors='coerce')
    if hasattr(match_stats['datetime'].dt, 'tz_localize'):
        if match_stats['datetime'].dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in match_stats['datetime'] if pd.notnull(x)):
            match_stats['datetime'] = match_stats['datetime'].dt.tz_localize(None)
    
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
    # Normalize all datetimes to tz-naive for comparison (robust to mixed tz-aware/tz-naive)
    datetimes = pd.to_datetime(df['datetime'], errors='coerce')
    if hasattr(datetimes.dt, 'tz_localize'):
        # Remove timezone if any values are tz-aware
        if datetimes.dt.tz is not None or any(getattr(x, 'tzinfo', None) is not None for x in datetimes if pd.notnull(x)):
            datetimes = datetimes.dt.tz_localize(None)
    recent_date = datetimes.max() - pd.Timedelta(days=days)
    recent_data = df[datetimes >= recent_date]
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

def get_team_chemistry_matrix(df):
    """Analyze which players work best together in team matches"""
    if df.empty:
        return {}
    
    team_matches = df[df['game_mode'] == 'Team']
    if team_matches.empty:
        return {}
    
    # Get all unique players who played team matches
    team_players = team_matches['player_name'].unique()
    chemistry_matrix = {}
    
    for player1 in team_players:
        chemistry_matrix[player1] = {}
        for player2 in team_players:
            if player1 != player2:
                # Find matches where both players were on the same team
                player1_matches = team_matches[team_matches['player_name'] == player1]
                player2_matches = team_matches[team_matches['player_name'] == player2]
                
                # Find common matches
                common_matches = set(player1_matches['match_id']).intersection(set(player2_matches['match_id']))
                
                if common_matches:
                    # Calculate team performance when both players are together
                    team_performance = []
                    for match_id in common_matches:
                        match_data = team_matches[team_matches['match_id'] == match_id]
                        player1_team = match_data[match_data['player_name'] == player1]['team'].iloc[0]
                        player2_team = match_data[match_data['player_name'] == player2]['team'].iloc[0]
                        
                        if player1_team == player2_team:
                            # They're on the same team
                            team_score = match_data[match_data['team'] == player1_team]['score'].sum()
                            other_teams = match_data[match_data['team'] != player1_team]
                            
                            if not other_teams.empty:
                                other_team_scores = other_teams.groupby('team')['score'].sum()
                                max_other_score = other_team_scores.max()
                                won = team_score > max_other_score
                                team_performance.append(won)
                    
                    if team_performance:
                        win_rate = sum(team_performance) / len(team_performance) * 100
                        chemistry_matrix[player1][player2] = {
                            'matches_together': len(team_performance),
                            'win_rate': round(win_rate, 1),
                            'chemistry_score': round(win_rate / 100, 2)  # Normalized 0-1
                        }
                    else:
                        chemistry_matrix[player1][player2] = None
                else:
                    chemistry_matrix[player1][player2] = None
    
    return chemistry_matrix

def get_player_role_analysis(df):
    """Analyze player roles based on their playing style"""
    if df.empty:
        return {}
    
    players = df['player_name'].unique()
    role_analysis = {}
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            # Calculate role indicators
            kd_ratio = player_stats['kd_ratio']
            kills_per_min = player_stats['kills_per_minute']
            assists_per_min = player_stats['assists_per_minute']
            deaths_per_min = player_stats['deaths_per_minute']
            win_rate = player_stats['win_rate']
            
            # Determine primary role
            if kd_ratio > 1.5 and kills_per_min > 0.8:
                primary_role = "Killer"
                role_description = "High K/D ratio and kill rate - primary damage dealer"
            elif assists_per_min > 0.3 and deaths_per_min < 0.5:
                primary_role = "Support"
                role_description = "High assist rate with low deaths - team support player"
            elif kd_ratio < 0.8 and deaths_per_min > 0.8:
                primary_role = "Aggressive"
                role_description = "High death rate - aggressive but risky playstyle"
            elif win_rate > 60 and kd_ratio > 1.0:
                primary_role = "Leader"
                role_description = "High win rate with good K/D - team leader"
            else:
                primary_role = "Balanced"
                role_description = "Well-rounded player with balanced stats"
            
            # Calculate role strengths
            role_strengths = {
                'killing_power': min(kd_ratio / 2.0, 1.0),  # Normalized 0-1
                'support_value': min(assists_per_min / 0.5, 1.0),  # Normalized 0-1
                'survival_rate': max(1 - deaths_per_min / 1.0, 0.0),  # Normalized 0-1
                'winning_ability': win_rate / 100.0,  # Normalized 0-1
                'consistency': min(player_stats['total_matches'] / 20.0, 1.0)  # Based on match count
            }
            
            role_analysis[player] = {
                'primary_role': primary_role,
                'role_description': role_description,
                'role_strengths': role_strengths,
                'stats': {
                    'kd_ratio': kd_ratio,
                    'kills_per_minute': kills_per_min,
                    'assists_per_minute': assists_per_min,
                    'deaths_per_minute': deaths_per_min,
                    'win_rate': win_rate
                }
            }
    
    return role_analysis

def get_team_formation_performance(df):
    """Analyze performance of different team combinations"""
    if df.empty:
        return {}
    
    team_matches = df[df['game_mode'] == 'Team']
    if team_matches.empty:
        return {}
    
    formation_stats = {}
    
    # Group by match and analyze team formations
    for match_id in team_matches['match_id'].unique():
        match_data = team_matches[team_matches['match_id'] == match_id]
        teams = match_data['team'].unique()
        
        for team in teams:
            team_players = match_data[match_data['team'] == team]['player_name'].tolist()
            team_players.sort()  # Sort for consistent key generation
            formation_key = tuple(team_players)
            
            if len(formation_key) >= 2:  # Only consider formations with 2+ players
                if formation_key not in formation_stats:
                    formation_stats[formation_key] = {
                        'matches': 0,
                        'wins': 0,
                        'total_kills': 0,
                        'total_score': 0,
                        'players': list(formation_key)
                    }
                
                formation_stats[formation_key]['matches'] += 1
                formation_stats[formation_key]['total_kills'] += match_data[match_data['team'] == team]['kills'].sum()
                formation_stats[formation_key]['total_score'] += match_data[match_data['team'] == team]['score'].sum()
                
                # Determine if team won
                team_score = match_data[match_data['team'] == team]['score'].sum()
                other_teams = match_data[match_data['team'] != team]
                
                if not other_teams.empty:
                    other_team_scores = other_teams.groupby('team')['score'].sum()
                    max_other_score = other_team_scores.max()
                    if team_score > max_other_score:
                        formation_stats[formation_key]['wins'] += 1
    
    # Calculate win rates and performance metrics
    for formation_key, stats in formation_stats.items():
        if stats['matches'] > 0:
            stats['win_rate'] = round((stats['wins'] / stats['matches']) * 100, 1)
            stats['avg_kills_per_match'] = round(stats['total_kills'] / stats['matches'], 1)
            stats['avg_score_per_match'] = round(stats['total_score'] / stats['matches'], 1)
            stats['formation_size'] = len(stats['players'])
    
    # Sort by win rate and filter for formations with multiple matches
    sorted_formations = {k: v for k, v in formation_stats.items() if v['matches'] >= 2}
    sorted_formations = dict(sorted(sorted_formations.items(), 
                                   key=lambda x: x[1]['win_rate'], reverse=True))
    
    return sorted_formations 

def get_battle_royale_rankings(df):
    """Create battle royale style tournament bracket rankings"""
    if df.empty:
        return {}
    
    # Get player stats for ranking
    players = df['player_name'].unique()
    player_rankings = []
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            # Calculate ranking score (weighted combination of stats)
            ranking_score = (
                player_stats['kd_ratio'] * 0.3 +
                player_stats['win_rate'] * 0.3 +
                player_stats['kills_per_minute'] * 0.2 +
                player_stats['total_matches'] * 0.1 +
                player_stats['assists_per_minute'] * 0.1
            )
            
            player_rankings.append({
                'player_name': player,
                'ranking_score': ranking_score,
                'kd_ratio': player_stats['kd_ratio'],
                'win_rate': player_stats['win_rate'],
                'kills_per_minute': player_stats['kills_per_minute'],
                'total_matches': player_stats['total_matches'],
                'assists_per_minute': player_stats['assists_per_minute'],
                'total_kills': player_stats['total_kills'],
                'total_score': player_stats['total_score']
            })
    
    # Sort by ranking score
    player_rankings.sort(key=lambda x: x['ranking_score'], reverse=True)
    
    # Assign tiers
    tiers = {
        'Champion': player_rankings[:1] if player_rankings else [],
        'Elite': player_rankings[1:3] if len(player_rankings) > 1 else [],
        'Veteran': player_rankings[3:6] if len(player_rankings) > 3 else [],
        'Rookie': player_rankings[6:10] if len(player_rankings) > 6 else [],
        'Novice': player_rankings[10:] if len(player_rankings) > 10 else []
    }
    
    return {
        'rankings': player_rankings,
        'tiers': tiers,
        'total_players': len(player_rankings)
    }

def get_achievement_badges(df):
    """Generate achievement badges for players"""
    if df.empty:
        return {}
    
    players = df['player_name'].unique()
    achievements = {}
    
    # Define achievement criteria
    achievement_criteria = {
        'Sharpshooter': {'metric': 'kd_ratio', 'threshold': 2.0, 'description': 'K/D ratio above 2.0'},
        'Kill Master': {'metric': 'total_kills', 'threshold': 100, 'description': '100+ total kills'},
        'Survivor': {'metric': 'deaths_per_minute', 'threshold': 0.3, 'description': 'Less than 0.3 deaths per minute', 'reverse': True},
        'Support Hero': {'metric': 'assists_per_minute', 'threshold': 0.5, 'description': '0.5+ assists per minute'},
        'Winner': {'metric': 'win_rate', 'threshold': 70, 'description': '70%+ win rate'},
        'Veteran': {'metric': 'total_matches', 'threshold': 20, 'description': '20+ matches played'},
        'Speed Demon': {'metric': 'kills_per_minute', 'threshold': 1.0, 'description': '1.0+ kills per minute'},
        'Consistent': {'metric': 'total_matches', 'threshold': 10, 'description': '10+ matches played'},
        'Elite': {'metric': 'ranking_score', 'threshold': 80, 'description': 'Elite tier ranking'},
        'Champion': {'metric': 'ranking_score', 'threshold': 90, 'description': 'Champion tier ranking'}
    }
    
    for player in players:
        player_stats = get_player_stats(df, player)
        if player_stats:
            player_achievements = []
            
            # Calculate ranking score for elite/champion badges
            ranking_score = (
                player_stats['kd_ratio'] * 0.3 +
                player_stats['win_rate'] * 0.3 +
                player_stats['kills_per_minute'] * 0.2 +
                player_stats['total_matches'] * 0.1 +
                player_stats['assists_per_minute'] * 0.1
            )
            player_stats['ranking_score'] = ranking_score
            
            for badge_name, criteria in achievement_criteria.items():
                metric_value = player_stats.get(criteria['metric'], 0)
                threshold = criteria['threshold']
                
                if criteria.get('reverse', False):
                    # For metrics where lower is better (like deaths per minute)
                    if metric_value <= threshold:
                        player_achievements.append({
                            'name': badge_name,
                            'description': criteria['description'],
                            'unlocked': True,
                            'progress': 100
                        })
                    else:
                        progress = max(0, min(100, (threshold / metric_value) * 100))
                        player_achievements.append({
                            'name': badge_name,
                            'description': criteria['description'],
                            'unlocked': False,
                            'progress': progress
                        })
                else:
                    # For metrics where higher is better
                    if metric_value >= threshold:
                        player_achievements.append({
                            'name': badge_name,
                            'description': criteria['description'],
                            'unlocked': True,
                            'progress': 100
                        })
                    else:
                        progress = max(0, min(100, (metric_value / threshold) * 100))
                        player_achievements.append({
                            'name': badge_name,
                            'description': criteria['description'],
                            'unlocked': False,
                            'progress': progress
                        })
            
            achievements[player] = {
                'achievements': player_achievements,
                'unlocked_count': sum(1 for a in player_achievements if a['unlocked']),
                'total_achievements': len(player_achievements)
            }
    
    return achievements

def get_gaming_session_analysis(df):
    """Analyze performance patterns over time and gaming sessions"""
    if df.empty:
        return {}
    
    # Group by date and analyze daily patterns
    df['date'] = df['datetime'].dt.date
    daily_stats = df.groupby('date').agg({
        'match_id': 'nunique',
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'score': 'sum',
        'player_name': 'nunique'
    }).reset_index()
    
    # Calculate daily performance metrics
    daily_stats['kd_ratio'] = daily_stats.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    daily_stats['avg_score_per_match'] = daily_stats['score'] / daily_stats['match_id']
    daily_stats['avg_kills_per_match'] = daily_stats['kills'] / daily_stats['match_id']
    
    # Identify gaming sessions (consecutive days with matches)
    daily_stats = daily_stats.sort_values('date')
    daily_stats['session_id'] = 0
    session_id = 0
    
    for i in range(len(daily_stats)):
        if i == 0:
            session_id += 1
        else:
            days_diff = (daily_stats.iloc[i]['date'] - daily_stats.iloc[i-1]['date']).days
            if days_diff > 1:  # Gap of more than 1 day starts new session
                session_id += 1
        daily_stats.iloc[i, daily_stats.columns.get_loc('session_id')] = session_id
    
    # Analyze session patterns
    session_analysis = {}
    for session_id in daily_stats['session_id'].unique():
        session_data = daily_stats[daily_stats['session_id'] == session_id]
        
        session_analysis[session_id] = {
            'start_date': session_data['date'].min(),
            'end_date': session_data['date'].max(),
            'duration_days': (session_data['date'].max() - session_data['date'].min()).days + 1,
            'total_matches': session_data['match_id'].sum(),
            'total_kills': session_data['kills'].sum(),
            'avg_kd_ratio': session_data['kd_ratio'].mean(),
            'avg_score_per_match': session_data['avg_score_per_match'].mean(),
            'peak_performance_day': session_data.loc[session_data['kd_ratio'].idxmax(), 'date'],
            'peak_kd_ratio': session_data['kd_ratio'].max()
        }
    
    # Calculate time-based patterns
    df['hour'] = df['datetime'].dt.hour
    hourly_performance = df.groupby('hour').agg({
        'kills': 'mean',
        'deaths': 'mean',
        'score': 'mean',
        'match_id': 'count'
    }).reset_index()
    
    hourly_performance['kd_ratio'] = hourly_performance.apply(
        lambda row: row['kills'] / row['deaths'] if row['deaths'] > 0 else row['kills'], axis=1
    )
    
    return {
        'daily_stats': daily_stats.to_dict('records'),
        'session_analysis': session_analysis,
        'hourly_performance': hourly_performance.to_dict('records'),
        'total_sessions': len(session_analysis),
        'avg_session_duration': sum(s['duration_days'] for s in session_analysis.values()) / len(session_analysis) if session_analysis else 0
    } 

def get_player_comparison_data(df, player1, player2):
    """Get detailed comparison data between two players"""
    if df.empty or not player1 or not player2:
        return {}
    
    player1_stats = get_player_stats(df, player1)
    player2_stats = get_player_stats(df, player2)
    
    if not player1_stats or not player2_stats:
        return {}
    
    # Calculate comparison metrics
    comparison_data = {
        'player1': {
            'name': player1,
            'stats': player1_stats
        },
        'player2': {
            'name': player2,
            'stats': player2_stats
        },
        'comparison': {
            'kd_ratio_diff': player1_stats['kd_ratio'] - player2_stats['kd_ratio'],
            'win_rate_diff': player1_stats['win_rate'] - player2_stats['win_rate'],
            'kills_per_min_diff': player1_stats['kills_per_minute'] - player2_stats['kills_per_minute'],
            'assists_per_min_diff': player1_stats['assists_per_minute'] - player2_stats['assists_per_minute'],
            'total_matches_diff': player1_stats['total_matches'] - player2_stats['total_matches'],
            'total_kills_diff': player1_stats['total_kills'] - player2_stats['total_kills']
        }
    }
    
    # Determine winner in each category
    comparison_data['winners'] = {
        'kd_ratio': player1 if player1_stats['kd_ratio'] > player2_stats['kd_ratio'] else player2,
        'win_rate': player1 if player1_stats['win_rate'] > player2_stats['win_rate'] else player2,
        'kills_per_min': player1 if player1_stats['kills_per_minute'] > player2_stats['kills_per_minute'] else player2,
        'assists_per_min': player1 if player1_stats['assists_per_minute'] > player2_stats['assists_per_minute'] else player2,
        'total_matches': player1 if player1_stats['total_matches'] > player2_stats['total_matches'] else player2,
        'total_kills': player1 if player1_stats['total_kills'] > player2_stats['total_kills'] else player2
    }
    
    return comparison_data

def simulate_team_scenario(df, team_composition, opponent_composition=None):
    """Simulate team performance with different compositions"""
    if df.empty:
        return {}
    
    # Get player stats for the team
    team_stats = {}
    for player in team_composition:
        player_stats = get_player_stats(df, player)
        if player_stats:
            team_stats[player] = player_stats
    
    if not team_stats:
        return {}
    
    # Calculate team performance metrics
    team_performance = {
        'total_kd_ratio': sum(stats['kd_ratio'] for stats in team_stats.values()),
        'avg_kd_ratio': sum(stats['kd_ratio'] for stats in team_stats.values()) / len(team_stats),
        'total_win_rate': sum(stats['win_rate'] for stats in team_stats.values()) / len(team_stats),
        'total_kills_per_min': sum(stats['kills_per_minute'] for stats in team_stats.values()),
        'total_assists_per_min': sum(stats['assists_per_minute'] for stats in team_stats.values()),
        'total_matches': max(stats['total_matches'] for stats in team_stats.values()),
        'team_size': len(team_stats)
    }
    
    # Calculate team synergy score (based on complementary roles)
    role_analysis = get_player_role_analysis(df)
    synergy_score = 0
    roles = []
    
    for player in team_composition:
        if player in role_analysis:
            roles.append(role_analysis[player]['primary_role'])
    
    # Bonus for diverse roles
    unique_roles = len(set(roles))
    synergy_score += unique_roles * 10
    
    # Bonus for specific role combinations
    if 'Killer' in roles and 'Support' in roles:
        synergy_score += 20  # Good balance
    if 'Leader' in roles:
        synergy_score += 15  # Leadership bonus
    
    team_performance['synergy_score'] = min(synergy_score, 100)
    
    # Simulate win probability based on team stats
    base_win_prob = min(team_performance['avg_kd_ratio'] * 25 + team_performance['total_win_rate'] * 0.5, 95)
    synergy_bonus = team_performance['synergy_score'] * 0.3
    team_performance['predicted_win_rate'] = min(base_win_prob + synergy_bonus, 95)
    
    # If opponent composition is provided, calculate head-to-head prediction
    if opponent_composition:
        opponent_stats = {}
        for player in opponent_composition:
            player_stats = get_player_stats(df, player)
            if player_stats:
                opponent_stats[player] = player_stats
        
        if opponent_stats:
            opponent_performance = {
                'avg_kd_ratio': sum(stats['kd_ratio'] for stats in opponent_stats.values()) / len(opponent_stats),
                'total_win_rate': sum(stats['win_rate'] for stats in opponent_stats.values()) / len(opponent_stats)
            }
            
            # Calculate win probability in head-to-head
            team_strength = team_performance['predicted_win_rate']
            opponent_strength = min(opponent_performance['avg_kd_ratio'] * 25 + opponent_performance['total_win_rate'] * 0.5, 95)
            
            # Adjust based on relative strength
            strength_diff = team_strength - opponent_strength
            head_to_head_win_rate = 50 + (strength_diff * 0.8)  # Base 50% + adjustment
            team_performance['head_to_head_win_rate'] = max(min(head_to_head_win_rate, 95), 5)
    
    return team_performance

def get_optimal_team_composition(df, available_players, team_size=3):
    """Find optimal team composition from available players"""
    if df.empty or len(available_players) < team_size:
        return {}
    
    from itertools import combinations
    
    # Get all possible team combinations
    possible_teams = list(combinations(available_players, team_size))
    
    best_team = None
    best_score = 0
    team_analysis = {}
    
    for team in possible_teams:
        team_performance = simulate_team_scenario(df, list(team))
        if team_performance:
            # Calculate overall team score
            team_score = (
                team_performance['predicted_win_rate'] * 0.4 +
                team_performance['synergy_score'] * 0.3 +
                team_performance['avg_kd_ratio'] * 10 * 0.3
            )
            
            team_analysis[team] = {
                'performance': team_performance,
                'score': team_score
            }
            
            if team_score > best_score:
                best_score = team_score
                best_team = team
    
    return {
        'best_team': list(best_team) if best_team else [],
        'best_score': best_score,
        'all_teams': team_analysis,
        'total_combinations': len(possible_teams)
    } 