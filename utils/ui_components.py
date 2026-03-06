import streamlit as st
import pandas as pd
from datetime import datetime


def create_metric_card(title, value, subtitle="", icon="", color="primary"):
    """Create a styled metric card with neon glow effects"""
    colors = {
        "primary": "#00f5ff",
        "success": "#00ff88",
        "warning": "#ff6b35",
        "error": "#ff3366",
        "info": "#0099ff",
    }

    glows = {
        "primary": "rgba(0, 245, 255, 0.4)",
        "success": "rgba(0, 255, 136, 0.4)",
        "warning": "rgba(255, 107, 53, 0.4)",
        "error": "rgba(255, 51, 102, 0.4)",
        "info": "rgba(0, 153, 255, 0.4)",
    }

    selected_color = colors.get(color, colors["primary"])
    selected_glow = glows.get(color, glows["primary"])

    return f"""
    <div class="metric-card" style="border-color: {selected_glow};">
        <h3 style="color: #a8b2d1; display: flex; align-items: center; gap: 0.5rem;">
            {f'<span style="font-size: 1.1rem; filter: drop-shadow(0 0 8px {selected_glow});">{icon}</span>' if icon else ''}
            {title}
        </h3>
        <h2 style="background: linear-gradient(135deg, {selected_color}, #b537ff);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   filter: drop-shadow(0 0 10px {selected_glow});">
            {value}
        </h2>
        {f'<p style="color: #6b7791; font-size: 0.85rem; margin: 0.5rem 0 0 0; font-weight: 500;">{subtitle}</p>' if subtitle else ''}
    </div>
    """


def create_status_card(title, message, status="info"):
    """Create a status card with different styles"""
    status_classes = {
        "success": "status-success",
        "warning": "status-warning",
        "error": "status-error",
        "info": "status-info",
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
    """Create a player card with stats and premium styling"""
    rank_emoji = ""
    rank_color = "#00f5ff"
    if rank == 1:
        rank_emoji = "🥇"
        rank_color = "#FFD700"
    elif rank == 2:
        rank_emoji = "🥈"
        rank_color = "#C0C0C0"
    elif rank == 3:
        rank_emoji = "🥉"
        rank_color = "#CD7F32"
    elif rank:
        rank_emoji = f"#{rank}"

    return f"""
    <div class="metric-card" style="position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 1.1rem;">
                <span style="font-size: 1.5rem; filter: drop-shadow(0 0 10px {rank_color});">{rank_emoji}</span>
                <span style="background: linear-gradient(135deg, #00f5ff, #b537ff);
                             -webkit-background-clip: text;
                             -webkit-text-fill-color: transparent;
                             background-clip: text;
                             font-weight: 800;">{player_name}</span>
            </h3>
            <span style="font-size: 0.9rem; color: #a8b2d1; background: rgba(0, 245, 255, 0.1);
                         padding: 0.25rem 0.75rem; border-radius: 1rem; border: 1px solid rgba(0, 245, 255, 0.3);
                         font-weight: 600;">K/D: {stats.get('kd_ratio', 0):.2f}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div style="background: rgba(0, 245, 255, 0.05); padding: 0.75rem; border-radius: 0.5rem;
                        border: 1px solid rgba(0, 245, 255, 0.2);">
                <small style="color: #6b7791; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 1px;">Kills/Min</small>
                <div style="font-weight: 700; font-size: 1.25rem; color: #00ff88; margin-top: 0.25rem;">{stats.get('kills_per_minute', 0):.2f}</div>
            </div>
            <div style="background: rgba(181, 55, 255, 0.05); padding: 0.75rem; border-radius: 0.5rem;
                        border: 1px solid rgba(181, 55, 255, 0.2);">
                <small style="color: #6b7791; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 1px;">Win Rate</small>
                <div style="font-weight: 700; font-size: 1.25rem; color: #b537ff; margin-top: 0.25rem;">{stats.get('win_rate', 0):.1f}%</div>
            </div>
        </div>
    </div>
    """


def create_timeline_item(date, title, description, icon="📅"):
    """Create a timeline item with modern styling"""
    return f"""
    <div style="display: flex; align-items: start; margin: 1rem 0; padding: 1.25rem;
                background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px);
                border-radius: 1rem; border: 1px solid rgba(0, 245, 255, 0.2);
                transition: all 0.3s ease; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 3px; height: 100%;
                    background: linear-gradient(180deg, #00f5ff, #b537ff);"></div>
        <div style="margin-right: 1rem; font-size: 1.75rem; filter: drop-shadow(0 0 8px rgba(0, 245, 255, 0.4));">{icon}</div>
        <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #ffffff; font-family: 'Outfit', sans-serif;">{title}</div>
            <div style="color: #6b7791; font-size: 0.85rem; margin-top: 0.25rem; font-weight: 500;">{date}</div>
            <div style="color: #a8b2d1; margin-top: 0.75rem; line-height: 1.6;">{description}</div>
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
    """Create an empty state component with modern styling"""
    return f"""
    <div style="text-align: center; padding: 4rem 2rem;
                background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px);
                border-radius: 1.5rem; border: 2px dashed rgba(0, 245, 255, 0.3);
                margin: 2rem 0;">
        <div style="font-size: 5rem; margin-bottom: 1.5rem;
                    filter: drop-shadow(0 0 20px rgba(0, 245, 255, 0.4));
                    animation: float 3s ease-in-out infinite;">
            {icon}
        </div>
        <h3 style="color: #ffffff; margin-bottom: 0.75rem; font-size: 1.5rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
            {title}
        </h3>
        <p style="color: #a8b2d1; font-size: 1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
            {description}
        </p>
    </div>
    """


def create_filter_section(title, filters):
    """Create a filter section with multiple filters"""
    st.markdown(f"### 🔍 {title}")

    cols = st.columns(len(filters))
    filter_values = {}

    for i, (filter_name, filter_config) in enumerate(filters.items()):
        with cols[i]:
            if filter_config["type"] == "selectbox":
                filter_values[filter_name] = st.selectbox(
                    filter_config["label"],
                    options=filter_config["options"],
                    help=filter_config.get("help", ""),
                )
            elif filter_config["type"] == "multiselect":
                filter_values[filter_name] = st.multiselect(
                    filter_config["label"],
                    options=filter_config["options"],
                    help=filter_config.get("help", ""),
                )
            elif filter_config["type"] == "date_input":
                filter_values[filter_name] = st.date_input(
                    filter_config["label"],
                    value=filter_config.get("value", datetime.now()),
                    help=filter_config.get("help", ""),
                )

    return filter_values


def create_stats_grid(stats_data, columns=4):
    """Create a responsive stats grid"""
    cols = st.columns(columns)

    for i, (title, value, subtitle, icon, color) in enumerate(stats_data):
        with cols[i % columns]:
            st.markdown(
                create_metric_card(title, value, subtitle, icon, color),
                unsafe_allow_html=True,
            )


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

            comparison_data.append(
                {"Metric": label, "Value 1": val1, "Value 2": val2, "Winner": winner}
            )

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


def create_section_header(title, subtitle="", icon=""):
    """Create a modern section header with gradient styling"""
    return f"""
    <div style="margin: 3rem 0 2rem 0; position: relative;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            {f'<span style="font-size: 2rem; filter: drop-shadow(0 0 10px rgba(0, 245, 255, 0.5));">{icon}</span>' if icon else ''}
            <h2 style="font-size: 2rem; font-weight: 800; font-family: \'Outfit\', sans-serif; margin: 0;
                       background: linear-gradient(135deg, #00f5ff, #b537ff);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;">
                {title}
            </h2>
        </div>
        {f'<p style="color: #6b7791; font-size: 1rem; margin: 0.5rem 0 0 0; padding-left: {3.5 if icon else 0}rem;">{subtitle}</p>' if subtitle else ''}
        <div style="height: 2px; width: 100%; max-width: 200px; margin-top: 1rem;
                    background: linear-gradient(90deg, #00f5ff, #b537ff, transparent);
                    box-shadow: 0 0 10px rgba(0, 245, 255, 0.5);"></div>
    </div>
    """


def create_content_container(content, title="", padding="2rem"):
    """Create a glassmorphic content container"""
    header_html = (
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; padding-bottom: 1rem;
                    border-bottom: 1px solid rgba(0, 245, 255, 0.2);">
            <h3 style="font-size: 1.25rem; font-weight: 700; font-family: 'Outfit', sans-serif; margin: 0; color: #ffffff;">
                {title}
            </h3>
        </div>
    """
        if title
        else ""
    )

    return f"""
    <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px);
                border-radius: 1.25rem; border: 1px solid rgba(0, 245, 255, 0.2);
                padding: {padding}; margin: 1.5rem 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
        {header_html}
        {content}
    </div>
    """


def create_stats_row(stats_data, columns=4):
    """Create a responsive row of stat cards"""
    # This will be used within Streamlit columns, so we return instructions
    return stats_data


def create_section_divider(style="gradient"):
    """Create a decorative section divider"""
    if style == "gradient":
        return """
        <div style="margin: 3rem 0; height: 1px;
                    background: linear-gradient(90deg, transparent, #00f5ff, #b537ff, transparent);
                    box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);"></div>
        """
    elif style == "dots":
        return """
        <div style="margin: 3rem 0; text-align: center;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%;
                         background: #00f5ff; margin: 0 0.5rem; box-shadow: 0 0 10px rgba(0, 245, 255, 0.5);"></span>
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%;
                         background: #b537ff; margin: 0 0.5rem; box-shadow: 0 0 10px rgba(181, 55, 255, 0.5);"></span>
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%;
                         background: #ff2e97; margin: 0 0.5rem; box-shadow: 0 0 10px rgba(255, 46, 151, 0.5);"></span>
        </div>
        """
    else:
        return """
        <div style="margin: 3rem 0; height: 1px; background: rgba(100, 115, 150, 0.2);"></div>
        """


def create_page_header(title, subtitle="", icon=""):
    """Create a premium page header with animation"""
    return f"""
    <div style="text-align: center; margin: 0 0 3rem 0; padding: 2rem 0; position: relative;">
        <!-- Animated background glow -->
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    width: 300px; height: 300px;
                    background: radial-gradient(circle, rgba(0, 245, 255, 0.15), transparent 70%);
                    filter: blur(60px); pointer-events: none; z-index: 0;"></div>

        <div style="position: relative; z-index: 1;">
            {f'<div style="font-size: 4rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px rgba(0, 245, 255, 0.6)); animation: float 3s ease-in-out infinite;">{icon}</div>' if icon else ''}
            <h1 style="font-size: 3.5rem; font-weight: 900; font-family: \'Outfit\', sans-serif; margin: 0; line-height: 1.2;
                       background: linear-gradient(135deg, #00f5ff, #b537ff, #ff2e97);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;
                       text-shadow: 0 0 40px rgba(0, 245, 255, 0.3);">
                {title}
            </h1>
            {f'<p style="color: #a8b2d1; font-size: 1.1rem; margin: 1rem 0 0 0; font-weight: 500;">{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """


def create_info_card(title, items, icon="", color="primary"):
    """Create an info card with a list of items"""
    colors = {
        "primary": "#00f5ff",
        "success": "#00ff88",
        "warning": "#ff6b35",
        "error": "#ff3366",
        "purple": "#b537ff",
    }

    selected_color = colors.get(color, colors["primary"])

    items_html = "".join(
        [f'<li style="margin: 0.5rem 0; color: #a8b2d1;">{item}</li>' for item in items]
    )

    return f"""
    <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px);
                border-radius: 1rem; border: 1px solid rgba(0, 245, 255, 0.2);
                padding: 1.5rem; margin: 1rem 0;
                border-left: 4px solid {selected_color};
                box-shadow: -4px 0 20px rgba(0, 245, 255, 0.2);">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            {f'<span style="font-size: 1.5rem; filter: drop-shadow(0 0 8px {selected_color});">{icon}</span>' if icon else ''}
            <h4 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #ffffff; font-family: \'Outfit\', sans-serif;">
                {title}
            </h4>
        </div>
        <ul style="margin: 0; padding-left: 1.5rem; list-style-type: none;">
            {items_html}
        </ul>
    </div>
    """
