"""
Quick Actions Component for CivicAI.

Renders a panel of shortcuts using native Streamlit page links for seamless navigation.
"""

import streamlit as st


def render_quick_actions():
    """
    Renders the Quick Actions container.
    """
    st.markdown('<div class="quick-actions-anchor"></div>', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top:0; color: var(--text-main); font-weight:700; margin-bottom: 15px;">⚡ Quick Actions</h4>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link("pages/report_issue.py", label="Report Issue", icon="📝", use_container_width=True)
        st.page_link("pages/announcements.py", label="Announcements", icon="📢", use_container_width=True)
    with col2:
        st.page_link("pages/community_map.py", label="Community Map", icon="🗺", use_container_width=True)
        st.page_link("pages/my_reports.py", label="My Reports", icon="📂", use_container_width=True)
    with col3:
        st.page_link("pages/analytics.py", label="Analytics", icon="📊", use_container_width=True)
        st.page_link("pages/leaderboard.py", label="Leaderboard", icon="🏆", use_container_width=True)
