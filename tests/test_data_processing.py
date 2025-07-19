import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import data_processing


def test_get_unique_players():
    df = pd.DataFrame({"player_name": ["Alice", "Bob", "Alice"]})
    assert data_processing.get_unique_players(df) == ["Alice", "Bob"]
    assert data_processing.get_unique_players(pd.DataFrame()) == []


def test_get_unique_weapons(tmp_path, monkeypatch):
    # Create a mock Guns directory with images
    guns_dir = tmp_path / "data" / "Images" / "Guns"
    guns_dir.mkdir(parents=True)
    (guns_dir / "AR.png").touch()
    (guns_dir / "SMG.png").touch()
    df = pd.DataFrame({"weapon": ["AR", "Sniper"]})
    monkeypatch.setattr(os.path, "exists", lambda p: True)
    monkeypatch.setattr(os, "listdir", lambda p: ["AR.png", "SMG.png"])
    weapons = data_processing.get_unique_weapons(df)
    assert set(weapons) == {"AR", "SMG", "Sniper"}


def test_get_unique_maps(tmp_path, monkeypatch):
    # Create a mock Maps directory with images
    maps_dir = tmp_path / "data" / "Images" / "Maps"
    maps_dir.mkdir(parents=True)
    (maps_dir / "Factory.png").touch()
    (maps_dir / "Forest.png").touch()
    df = pd.DataFrame({"map_name": ["Factory", "Refinery"]})
    monkeypatch.setattr(os.path, "exists", lambda p: True)
    monkeypatch.setattr(os, "listdir", lambda p: ["Factory.png", "Forest.png"])
    maps = data_processing.get_unique_maps(df)
    assert set(maps) == {"Factory", "Forest", "Refinery"}


def test_validate_match_data():
    match_data = [
        {
            "player_name": "Alice",
            "kills": 5,
            "deaths": 2,
            "score": 100,
            "weapon": "AR",
            "match_length": 10,
        },
        {
            "player_name": "Bob",
            "kills": 3,
            "deaths": 4,
            "score": 80,
            "weapon": "SMG",
            "match_length": 10,
        },
    ]
    errors = data_processing.validate_match_data(match_data)
    assert errors == []
    # Missing required field
    bad_data = [
        {"player_name": "Alice", "kills": 5, "deaths": 2, "score": 100, "weapon": "AR"}
    ]
    errors = data_processing.validate_match_data(bad_data)
    assert any("match_length" in e for e in errors)
