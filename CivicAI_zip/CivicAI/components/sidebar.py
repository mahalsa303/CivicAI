"""
Sidebar Component for CivicAI.

Provides filters for Status, Severity, and Category, visible in the sidebar across pages.
"""

import streamlit as st
from typing import Any, Dict, List, Tuple


def render_sidebar(issues: List[Dict[str, Any]]) -> Tuple[str, str, str]:
    """
    Renders the sidebar filter panel with dynamic categories loaded from Firestore.

    Args:
        issues: Raw list of issues to extract unique categories.

    Returns:
        Tuple[str, str, str]: (selected_status, selected_severity, selected_category)
    """
    st.sidebar.image("https://img.icons8.com/color/96/city.png", width=80)
    st.sidebar.title("🚨 CivicAI Control Panel")
    st.sidebar.write("Configure dynamic filters for reports, maps, and analytics.")

    # Dynamic Category List
    categories = sorted(list(set(
        str(issue.get("category", "Unknown")) for issue in issues if issue.get("category")
    )))

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    
    status_filter = st.sidebar.selectbox(
        "Status",
        ["All", "Open", "Verified", "In Progress", "Resolved", "Rejected"],
        help="Filter reports by their current lifecycle status"
    )
    
    severity_filter = st.sidebar.selectbox(
        "Severity",
        ["All", "High", "Medium", "Low"],
        help="Filter reports by AI severity assessment"
    )
    
    category_filter = st.sidebar.selectbox(
        "Category",
        ["All"] + categories,
        help="Filter reports by issue category"
    )

    st.sidebar.markdown("---")
    
    # Render active configuration states
    demo_enabled = st.session_state.get("demo_mode", False)
    if demo_enabled:
        st.sidebar.success("💡 Demo Mode: Active")
    else:
        st.sidebar.info("🌐 Firestore Live Feed")

    return status_filter, severity_filter, category_filter
