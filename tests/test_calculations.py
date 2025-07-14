import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
from utils import calculations

def test_calculate_kd_ratio():
    assert calculations.calculate_kd_ratio(10, 2) == 5.0
    assert calculations.calculate_kd_ratio(0, 0) == 0
    assert calculations.calculate_kd_ratio(5, 0) == 5
    assert calculations.calculate_kd_ratio(7, 7) == 1.0

def test_get_player_stats_basic():
    df = pd.DataFrame({
        'match_id': [1, 1, 2, 2],
        'player_name': ['Alice', 'Bob', 'Alice', 'Bob'],
        'kills': [5, 3, 7, 2],
        'deaths': [2, 4, 1, 3],
        'assists': [1, 0, 2, 1],
        'score': [100, 80, 150, 90],
        'coins': [10, 5, 15, 7],
        'tags': [2, 1, 3, 0],
        'match_length': [10, 10, 12, 12],
        'game_mode': ['FFA', 'FFA', 'FFA', 'FFA'],
        'weapon': ['AR', 'SMG', 'AR', 'SMG'],
        'ping': [50, 60, 55, 65]
    })
    stats = calculations.get_player_stats(df, 'Alice')
    assert stats['total_matches'] == 2
    assert stats['total_kills'] == 12
    assert stats['total_deaths'] == 3
    assert stats['total_assists'] == 3
    assert stats['total_score'] == 250
    assert stats['total_coins'] == 25
    assert stats['total_tags'] == 5
    assert stats['total_minutes'] == 22
    assert stats['avg_kills_per_match'] == 6.0
    assert stats['kd_ratio'] == pytest.approx(4.0)

def test_get_leaderboard_data():
    df = pd.DataFrame({
        'match_id': [1, 1, 2, 2],
        'player_name': ['Alice', 'Bob', 'Alice', 'Bob'],
        'kills': [5, 3, 7, 2],
        'deaths': [2, 4, 1, 3],
        'assists': [1, 0, 2, 1],
        'score': [100, 80, 150, 90],
        'coins': [10, 5, 15, 7],
        'tags': [2, 1, 3, 0],
        'match_length': [10, 10, 12, 12],
        'game_mode': ['FFA', 'FFA', 'FFA', 'FFA'],
        'weapon': ['AR', 'SMG', 'AR', 'SMG'],
        'ping': [50, 60, 55, 65]
    })
    leaderboard = calculations.get_leaderboard_data(df)
    assert not leaderboard.empty
    assert set(leaderboard['player_name']) == {'Alice', 'Bob'}
    assert 'kd_ratio' in leaderboard.columns 