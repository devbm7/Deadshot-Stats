import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from utils import supabase_client
import types


class DummyClient:
    def table(self, *args, **kwargs):
        class DummyTable:
            def select(self, *a, **k):
                class DummyResponse:
                    data = []

                return DummyResponse()

            def insert(self, *a, **k):
                class DummyResponse:
                    data = True

                return DummyResponse()

            def delete(self, *a, **k):
                class DummyResponse:
                    data = True

                return DummyResponse()

        return DummyTable()


def test_get_supabase_client_missing_secrets(monkeypatch):
    monkeypatch.setattr("streamlit.secrets", {}, raising=False)
    with pytest.raises(ValueError):
        supabase_client.get_supabase_client()


def test_load_match_data_from_supabase_empty(monkeypatch):
    # Patch get_supabase_client to return dummy client
    monkeypatch.setattr(supabase_client, "get_supabase_client", lambda: DummyClient())
    df = supabase_client.load_match_data_from_supabase()
    assert df.empty
