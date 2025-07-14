import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from utils import image_processing

def test_validate_extracted_data_valid():
    data = {
        'players': [
            {'player_name': 'Alice', 'kills': 5, 'deaths': 2, 'score': 100},
            {'player_name': 'Bob', 'kills': 3, 'deaths': 4, 'score': 80}
        ]
    }
    errors = image_processing.validate_extracted_data(data)
    assert errors == []

def test_validate_extracted_data_missing_players():
    data = {}
    errors = image_processing.validate_extracted_data(data)
    assert any('No player data' in e for e in errors)

def test_validate_extracted_data_bad_player():
    data = {'players': ['not_a_dict']}
    errors = image_processing.validate_extracted_data(data)
    assert any('must be a dictionary' in e for e in errors)

def test_format_extracted_data_for_display():
    data = {
        'game_mode': 'FFA',
        'map_name': 'Factory',
        'match_length': 10,
        'players': [
            {'player_name': ' Alice ', 'kills': 5, 'deaths': 2, 'score': 100, 'weapon': 'AR'},
            {'player_name': 'Bob', 'kills': 3, 'deaths': 4, 'score': 80, 'weapon': 'SMG'}
        ]
    }
    formatted = image_processing.format_extracted_data_for_display(data)
    assert formatted['game_mode'] == 'FFA'
    assert formatted['map_name'] == 'Factory'
    assert formatted['match_length'] == 10
    assert formatted['players'][0]['player_name'] == 'Alice'
    assert formatted['players'][1]['player_name'] == 'Bob' 