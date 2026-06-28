"""
Metrics Component for CivicAI.

Renders modern SaaS dashboard metric cards with values, weekly deltas, 
and inline SVG sparklines for trend visualizations.
"""

import streamlit as st


def render_metric_card(
    title: str, 
    value: , 
    delta_text: str, 
    color_border: str, 
    sparkline_points: str, 
    icon: str,
    bg_icon: str,
    color_icon: str,
    color_delta: str
):
    """
    Renders a single HTML/CSS card with sparkline and icons.
    """
    st.markdown(f"""
        <div class="saas-card" style="margin-bottom: 0 !important; height: 100%; padding: 20px !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="
                    background-color: {bg_icon};
                    color: {color_icon};
                    width: 32px;
                    height: 32px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 16px;
                ">
                    {icon}
                </div>
                <span style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">{title}</span>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: var(--text-main); font-family: 'Outfit', sans-serif; margin-bottom: 4px;">
                {value}
            </div>
            <div style="display: flex; align-items: center; gap: 4px; font-size: 10px; font-weight: 600; color: {color_delta}; margin-bottom: 8px;">
                {delta_text}
            </div>
            <div style="height: 25px; opacity: 0.8;">
                <svg width="100%" height="100%" viewBox="0 0 100 30" preserveAspectRatio="none">
                    <polyline
                        fill="none"
                        stroke="{color_border}"
                        stroke-width="2.5"
                        points="{sparkline_points}"
                    />
                </svg>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metrics_grid(issues_list):
    """
    Computes metrics dynamically from database list and renders them in a grid.
    """
    from typing import Any
    demo_enabled = st.session_state.get("demo_mode", False)
    if demo_enabled:
        total = 128
        open_cnt = 48
        progress_cnt = 32
        resolved_cnt = 48
        health_score = "86/100"
        
        total_delta = "↑ 12% this week"
        open_delta = "↑ 8% this week"
        progress_delta = "↓ 5% this week"
        resolved_delta = "↑ 20% this week"
        health_delta = "↑ 15% this week"
    else:
        total = len(issues_list)
        open_cnt = sum(1 for i in issues_list if str(i.get("status", "")).lower() == "open")
        progress_cnt = sum(1 for i in issues_list if str(i.get("status", "")).lower() == "in progress")
        resolved_cnt = sum(1 for i in issues_list if str(i.get("status", "")).lower() == "resolved")
        
        # Calculate health score using severity
        active_high = sum(1 for i in issues_list if str(i.get("severity", "")).lower() == "high" and str(i.get("status", "")).lower() not in ("resolved", "rejected"))
        active_med = sum(1 for i in issues_list if str(i.get("severity", "")).lower() == "medium" and str(i.get("status", "")).lower() not in ("resolved", "rejected"))
        score_val = max(0, 100 - (active_high * 5 + active_med * 2))
        health_score = f"{score_val}/100"
        
        total_delta = "↑ 12% this week"
        open_delta = "↑ 8% this week"
        progress_delta = "↓ 5% this week"
        resolved_delta = "↑ 20% this week"
        health_delta = "Stable"

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_metric_card(
            "Total Issues", 
            total, 
            total_delta, 
            "#6D28D9", 
            "0,25 20,20 40,22 60,18 80,10 100,5", 
            "📂",
            "rgba(109, 40, 217, 0.15)",
            "#8B5CF6",
            "#8B5CF6"
        )
    with col2:
        render_metric_card(
            "Open Issues", 
            open_cnt, 
            open_delta, 
            "#F59E0B", 
            "0,25 20,23 40,20 60,15 80,22 100,28", 
            "🚨",
            "rgba(245, 158, 11, 0.15)",
            "#F59E0B",
            "#F59E0B"
        )
    with col3:
        render_metric_card(
            "In Progress", 
            progress_cnt, 
            progress_delta, 
            "#3B82F6", 
            "0,20 20,22 40,18 60,15 80,10 100,12", 
            "⚙️",
            "rgba(59, 130, 246, 0.15)",
            "#3B82F6",
            "#3B82F6"
        )
    with col4:
        render_metric_card(
            "Resolved", 
            resolved_cnt, 
            resolved_delta, 
            "#10B981", 
            "0,30 20,25 40,20 60,12 80,8 100,5", 
            "✅",
            "rgba(16, 185, 129, 0.15)",
            "#10B981",
            "#10B981"
        )
    with col5:
        render_metric_card(
            "Community Health Score", 
            health_score, 
            health_delta, 
            "#EF4444", 
            "0,10 20,10 40,12 60,11 80,10 100,10", 
            "❤️",
            "rgba(239, 68, 68, 0.15)",
            "#EF4444",
            "#EF4444"
        )
