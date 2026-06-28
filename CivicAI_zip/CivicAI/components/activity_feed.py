"""
Activity Feed Component for CivicAI.

Generates and displays a real-world activity log representing recent citizen reports,
verification upgrades, and departmental resolutions.
"""

import streamlit as st
from typing import Any, Dict, List
import datetime


def render_activity_feed(issues: List[Dict[str, Any]]):
    """
    Renders the Activity Feed list.
    """
    demo_enabled = st.session_state.get("demo_mode", False)
    
    # Process issues to extract real activities
    activities = []
    if demo_enabled:
        activities = [
            ("🟢", "rgba(16, 185, 129, 0.15)", "#10B981", "Road repair completed", "Muncipal Corp. • 2h ago"),
            ("💧", "rgba(59, 130, 246, 0.15)", "#3B82F6", "Water leakage verified", "Water Department • 3h ago"),
            ("➕", "rgba(109, 40, 217, 0.15)", "#8B5CF6", "New issue reported", "Ravi K. • 4h ago"),
            ("⚡", "rgba(245, 158, 11, 0.15)", "#F59E0B", "Street light fixed", "Electricity Dept. • 6h ago"),
            ("🗑", "rgba(16, 185, 129, 0.15)", "#10B981", "Garbage cleared", "Sanitation Dept. • 8h ago")
        ]
    else:
        icons_map = {
            "open": ("➕", "rgba(109, 40, 217, 0.15)", "#8B5CF6"),
            "verified": ("👍", "rgba(245, 158, 11, 0.15)", "#F59E0B"),
            "in progress": ("⚙️", "rgba(59, 130, 246, 0.15)", "#3B82F6"),
            "resolved": ("🟢", "rgba(16, 185, 129, 0.15)", "#10B981"),
            "rejected": ("❌", "rgba(239, 68, 68, 0.15)", "#EF4444")
        }
        for iss in issues[:5]:
            status = str(iss.get("status", "Open")).lower()
            category = iss.get("category", "Issue")
            reporter = iss.get("reporter", "Anonymous")
            dept = iss.get("department", "Department")
            
            icon, bg, color = icons_map.get(status, ("⚙️", "rgba(59, 130, 246, 0.15)", "#3B82F6"))
            
            if status == "open":
                title_text = f"New report: {category}"
                desc_text = f"Reported by {reporter}"
            elif status == "resolved":
                title_text = f"{category} resolved"
                desc_text = f"{dept} completed repair"
            elif status == "verified":
                title_text = f"{category} verified"
                desc_text = f"Community upvoted"
            elif status == "in progress":
                title_text = f"{category} in progress"
                desc_text = f"Assigned to {dept}"
            else:
                title_text = f"{category} closed"
                desc_text = f"Status updated to {status.title()}"
                
            activities.append((icon, bg, color, title_text, desc_text))

    items_html = ""
    for idx, (icon, bg, color, title_text, desc_text) in enumerate(activities[:5]):
        items_html += f"""
            <div style="display: flex; gap: 12px; align-items: center; padding: 10px 0; border-bottom: {'' if idx == 4 else '1px solid var(--border-color)'};">
                <div style="
                    background-color: {bg};
                    color: {color};
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 13px;
                    flex-shrink: 0;
                ">
                    {icon}
                </div>
                <div style="flex-grow: 1; min-width: 0;">
                    <div style="font-size: 13.5px; font-weight: 700; color: var(--text-main); margin-bottom: 2px;">{title_text}</div>
                    <div style="font-size: 11px; color: var(--text-muted);">{desc_text}</div>
                </div>
            </div>
        """

    st.markdown(f"""
        <div class="saas-card" style="margin-bottom: 20px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="margin: 0; font-weight: 700;">Recent Activity</h4>
                <a href="/Analytics" target="_self" style="font-size: 12px; color: var(--primary-light); text-decoration: none; font-weight: 600;">View All</a>
            </div>
            {items_html}
        </div>
    """, unsafe_allow_html=True)
