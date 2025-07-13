import streamlit as st
import pandas as pd
from datetime import datetime

def create_metric_card(title, value, subtitle="", icon="", color="primary"):
    """Create a styled metric card"""
    colors = {
        "primary": "#6366f1",
        "success": "#10b981", 
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    return f"""
    <div class="metric-card" style="border-left-color: {colors.get(color, colors['primary'])};">
        <h3>{icon} {title}</h3>
        <h2>{value}</h2>
        {f'<p style="color: #cbd5e1; font-size: 0.8rem; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """

def create_status_card(title, message, status="info"):
    """Create a status card with different styles"""
    status_classes = {
        "success": "status-success",
        "warning": "status-warning", 
        "error": "status-error",
        "info": "status-info"
    }
    
    return f"""
    <div class="status-card {status_classes.get(status, 'status-info')}">
        <h4>{title}</h4>
        <p>{message}</p>
    </div>
    """

def create_progress_bar(label, value, max_value=100, color="success"):
    """Create a custom progress bar"""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    return f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #f8fafc; font-weight: 600;">{label}</span>
            <span style="color: #cbd5e1;">{value}/{max_value}</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%;"></div>
        </div>
    </div>
    """

def create_achievement_badge(name, description, unlocked=True, progress=0):
    """Create an achievement badge"""
    if unlocked:
        return f"""
        <div class="achievement-badge" style="background: linear-gradient(135deg, #f59e0b, #f97316);">
            ✅ {name}
        </div>
        """
    else:
        return f"""
        <div class="achievement-badge" style="background: linear-gradient(135deg, #6b7280, #9ca3af); opacity: 0.6;">
            🔄 {name} ({progress:.0f}%)
        </div>
        """

def create_player_card(player_name, stats, rank=None):
    """Create a player card with stats"""
    rank_emoji = ""
    if rank == 1:
        rank_emoji = "🥇"
    elif rank == 2:
        rank_emoji = "🥈"
    elif rank == 3:
        rank_emoji = "🥉"
    elif rank:
        rank_emoji = f"#{rank}"
    
    return f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3>{rank_emoji} {player_name}</h3>
            <span style="font-size: 0.8rem; color: #cbd5e1;">K/D: {stats.get('kd_ratio', 0):.2f}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1rem;">
            <div>
                <small style="color: #cbd5e1;">Kills/Min</small>
                <div style="font-weight: 600;">{stats.get('kills_per_minute', 0):.2f}</div>
            </div>
            <div>
                <small style="color: #cbd5e1;">Win Rate</small>
                <div style="font-weight: 600;">{stats.get('win_rate', 0):.1f}%</div>
            </div>
        </div>
    </div>
    """

def create_timeline_item(date, title, description, icon="📅"):
    """Create a timeline item"""
    return f"""
    <div style="display: flex; align-items: start; margin: 1rem 0; padding: 1rem; background: var(--card-bg); border-radius: 0.75rem; border: 1px solid var(--border-color);">
        <div style="margin-right: 1rem; font-size: 1.5rem;">{icon}</div>
        <div style="flex: 1;">
            <div style="font-weight: 600; color: var(--text-primary);">{title}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">{date}</div>
            <div style="color: var(--text-secondary); margin-top: 0.5rem;">{description}</div>
        </div>
    </div>
    """

def create_loading_spinner():
    """Create a loading spinner"""
    return """
    <div style="display: flex; justify-content: center; align-items: center; padding: 2rem;">
        <div class="loading-spinner"></div>
        <span style="margin-left: 1rem; color: var(--text-secondary);">Loading...</span>
    </div>
    """

def create_empty_state(title, description, icon="📊"):
    """Create an empty state component"""
    return f"""
    <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">{title}</h3>
        <p style="color: var(--text-secondary);">{description}</p>
    </div>
    """

def create_filter_section(title, filters):
    """Create a filter section with multiple filters"""
    st.markdown(f"### 🔍 {title}")
    
    cols = st.columns(len(filters))
    filter_values = {}
    
    for i, (filter_name, filter_config) in enumerate(filters.items()):
        with cols[i]:
            if filter_config['type'] == 'selectbox':
                filter_values[filter_name] = st.selectbox(
                    filter_config['label'],
                    options=filter_config['options'],
                    help=filter_config.get('help', '')
                )
            elif filter_config['type'] == 'multiselect':
                filter_values[filter_name] = st.multiselect(
                    filter_config['label'],
                    options=filter_config['options'],
                    help=filter_config.get('help', '')
                )
            elif filter_config['type'] == 'date_input':
                filter_values[filter_name] = st.date_input(
                    filter_config['label'],
                    value=filter_config.get('value', datetime.now()),
                    help=filter_config.get('help', '')
                )
    
    return filter_values

def create_stats_grid(stats_data, columns=4):
    """Create a responsive stats grid"""
    cols = st.columns(columns)
    
    for i, (title, value, subtitle, icon, color) in enumerate(stats_data):
        with cols[i % columns]:
            st.markdown(create_metric_card(title, value, subtitle, icon, color), unsafe_allow_html=True)

def create_comparison_table(data1, data2, labels):
    """Create a comparison table between two datasets"""
    comparison_data = []
    
    for label in labels:
        if label in data1 and label in data2:
            val1 = data1[label]
            val2 = data2[label]
            
            # Determine winner
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                if val1 > val2:
                    winner = "data1"
                elif val2 > val1:
                    winner = "data2"
                else:
                    winner = "tie"
            else:
                winner = "tie"
            
            comparison_data.append({
                'Metric': label,
                'Value 1': val1,
                'Value 2': val2,
                'Winner': winner
            })
    
    return pd.DataFrame(comparison_data)

def create_tooltip(text, icon="ℹ️"):
    """Create a tooltip component"""
    return f"""
    <div style="position: relative; display: inline-block;">
        <span style="cursor: help;">{icon}</span>
        <div style="position: absolute; bottom: 125%; left: 50%; transform: translateX(-50%); 
                    background: var(--card-bg); color: var(--text-primary); padding: 0.5rem; 
                    border-radius: 0.5rem; border: 1px solid var(--border-color); 
                    white-space: nowrap; z-index: 1000; opacity: 0; transition: opacity 0.3s;">
            {text}
        </div>
    </div>
    """ 