"""
Announcement Card Component for CivicAI.

Renders city bulletins, municipal alerts, and upcoming community events.
"""

import streamlit as st
from typing import List, Dict, Any


def get_default_announcements() -> List[Dict[str, Any]]:
    """
    Returns a predefined list of local city announcements.
    """
    return [
        {
            "title": "Clean City Drive 🧹",
            "date": "June 28, 2026",
            "category": "Community",
            "desc": "Join our weekend volunteer clean-up drive at SVEC Public Park. Bins and gear provided.",
            "badge": "New"
        },
        {
            "title": "Water Supply Maintenance 🚰",
            "date": "June 30, 2026",
            "category": "Utility",
            "desc": "Scheduled pipeline upgrades. Low water pressure expected between 9 AM and 4 PM in Hostel area.",
            "badge": "Important"
        },
        {
            "title": "Traffic Diversion Alert 🚧",
            "date": "July 02, 2026",
            "category": "Traffic",
            "desc": "Road reconstruction near Main Gate. Heavy vehicles diverted via Bypass road.",
            "badge": "Warning"
        }
    ]


def render_announcements_panel():
    """
    Renders announcements as cards in a sidebar panel.
    """
    announcements = [
        {
            "title": "Clean City Drive",
            "date": "May 18, 2025",
            "badge": "New",
            "desc": "Join us this Sunday for a mega cleaning drive in all wards.",
            "img": "https://images.unsplash.com/photo-1542362567-b07eac79094d?w=80&h=80&fit=crop",
            "bg": "rgba(59, 130, 246, 0.15)",
            "color": "#3B82F6"
        },
        {
            "title": "Water Supply Maintenance",
            "date": "May 20, 2025",
            "badge": "Alert",
            "desc": "Water supply will be interrupted in some areas on May 20.",
            "img": "https://images.unsplash.com/photo-1542013936693-8848e574047a?w=80&h=80&fit=crop",
            "bg": "rgba(239, 68, 68, 0.15)",
            "color": "#EF4444"
        },
        {
            "title": "Traffic Diversion",
            "date": "May 22, 2025",
            "badge": "Update",
            "desc": "Diversion SVEC Main gate road for pipeline work from May 22.",
            "img": "https://images.unsplash.com/photo-1508349937151-22b68b72d5b1?w=80&h=80&fit=crop",
            "bg": "rgba(245, 158, 11, 0.15)",
            "color": "#F59E0B"
        }
    ]

    ann_html = ""
    for idx, ann in enumerate(announcements):
        ann_html += f"""
            <div style="display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-bottom: {'' if idx == 2 else '1px solid var(--border-color)'};">
                <img src="{ann['img']}" style="width: 48px; height: 48px; border-radius: 8px; object-fit: cover; flex-shrink: 0;" />
                <div style="flex-grow: 1; min-width: 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                        <span style="font-size: 13px; font-weight: 700; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{ann['title']}</span>
                        <span style="font-size: 8px; font-weight: bold; background-color: {ann['bg']}; color: {ann['color']}; padding: 1px 4px; border-radius: 3px; text-transform: uppercase; flex-shrink: 0;">{ann['badge']}</span>
                    </div>
                    <p style="font-size: 11px; color: var(--text-muted); margin: 0 0 4px 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 30px;">
                        {ann['desc']}
                    </p>
                    <div style="font-size: 9.5px; color: var(--text-muted); opacity: 0.8;">📅 {ann['date']}</div>
                </div>
            </div>
        """
        
    st.markdown(f"""
        <div class="saas-card" style="margin-bottom: 20px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="margin: 0; font-weight: 700;">Announcements</h4>
                <a href="/Announcements" target="_self" style="font-size: 12px; color: var(--primary-light); text-decoration: none; font-weight: 600;">View All</a>
            </div>
            {ann_html}
        </div>
    """, unsafe_allow_html=True)
