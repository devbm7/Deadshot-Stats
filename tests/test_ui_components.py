import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import ui_components


def test_create_metric_card():
    html = ui_components.create_metric_card(
        "Kills", 10, subtitle="Total", icon="🔫", color="success"
    )
    assert "Kills" in html
    assert "10" in html
    assert "Total" in html
    assert "🔫" in html
    assert "background" in html or "metric-card" in html


def test_create_status_card():
    html = ui_components.create_status_card("Status", "All good", status="success")
    assert "Status" in html
    assert "All good" in html
    assert "status-success" in html
