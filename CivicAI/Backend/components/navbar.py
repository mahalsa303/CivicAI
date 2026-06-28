"""
Navbar Component for CivicAI.

Provides a unified premium top navigation bar with logo taglines, search inputs,
location selector, notification badges, dark mode toggle, and profile initials avatar.
"""

import streamlit as st
from services.notification_service import get_notifications


def render_navbar():
    """
    Renders the consistent top navbar.
    """
    # 1. Load active theme and inject JavaScript to update DOM attributes
    dark_mode = st.session_state.get("dark_mode", True)
    theme_val = "dark" if dark_mode else "light"
    
    st.markdown(f"""
        <script>
        const doc = window.parent.document.documentElement;
        doc.setAttribute('data-theme', '{theme_val}');
        </script>
    """, unsafe_allow_html=True)

    # 2. Render Navbar Columns Grid (Left: 3.5, Center: 4.5, Right: 4.0)
    col_left, col_center, col_right = st.columns([3.5, 4.5, 4.0])

    with col_left:
        # Left Anchor & Logo Block
        st.markdown('<div class="logo-anchor"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 28px;">🚨</span>
                <div style="display: flex; flex-direction: column; line-height: 1.1;">
                    <span style="font-size: 20px; font-weight: 800; color: var(--text-main); font-family: 'Outfit', sans-serif;">CivicAI</span>
                    <span style="font-size: 10.5px; color: var(--text-muted); font-weight: 500; letter-spacing: 0.2px;">AI Powered Civic Intelligence</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_center:
        # Center Anchor & Pill Search Input
        st.markdown('<div class="search-anchor"></div>', unsafe_allow_html=True)
        search_query = st.text_input(
            "Search reports...",
            value=st.session_state.get("search_term", ""),
            placeholder="Search issues, departments, locations...",
            label_visibility="collapsed"
        )
        st.session_state["search_term"] = search_query

    with col_right:
        # Nest columns within Right section for Loc, Notif, Theme, Profile
        sub_col_loc, sub_col_notif, sub_col_theme, sub_col_profile = st.columns([2, 0.8, 0.8, 1])
        
        with sub_col_loc:
            st.markdown('<div class="loc-anchor"></div>', unsafe_allow_html=True)
            st.selectbox(
                "Active Location",
                ["📍 Bhimavaram, AP", "📍 SVEC Gate 1", "📍 Hostel Block A"],
                key="active_location",
                label_visibility="collapsed"
            )

        with sub_col_notif:
            st.markdown('<div class="notif-anchor"></div>', unsafe_allow_html=True)
            notifications = get_notifications()
            unread_count = len(notifications)
            
            # Popover displays only a bell icon with dynamic badge count overlayed via JS
            with st.popover("🔔", use_container_width=True):
                st.subheader("🔔 Notifications")
                st.markdown("<hr style='border:0; border-top:1px solid var(--border-color); margin: 8px 0;'>", unsafe_allow_html=True)
                for notif in notifications:
                    type_icon = "🟢" if notif["type"] == "success" else "🔵"
                    st.markdown(f"**{type_icon} {notif['title']}**")
                    st.caption(f"{notif['message']} • *{notif['timestamp']}*")
                    st.markdown("<hr style='border:0; border-top:1px solid var(--border-color); margin: 8px 0;'>", unsafe_allow_html=True)
            
            # Inject JS to set data-badge attribute on the popover button
            st.markdown(f"""
                <script>
                setTimeout(() => {{
                    const btns = window.parent.document.querySelectorAll('div:has(.notif-anchor) div[data-testid="stPopover"] button');
                    btns.forEach(btn => {{
                        if (btn) btn.setAttribute('data-badge', '{unread_count}');
                    }});
                }}, 100);
                </script>
            """, unsafe_allow_html=True)

        with sub_col_theme:
            st.markdown('<div class="theme-anchor"></div>', unsafe_allow_html=True)
            theme_icon = "☀️" if dark_mode else "🌙"
            if st.button(theme_icon, key="theme_toggle_btn", help="Toggle Light/Dark Mode", use_container_width=True):
                st.session_state["dark_mode"] = not dark_mode
                st.rerun()

        with sub_col_profile:
            st.markdown('<div class="profile-anchor"></div>', unsafe_allow_html=True)
            username = st.session_state.get("reporter_name", "Anonymous")
            initials = username[0].upper() if username else "A"
            
            # Circular Profile Avatar popover acting as menu
            with st.popover(initials, use_container_width=True):
                st.markdown(f"#### 👤 {username}")
                st.caption("Active Citizen Profile")
                st.markdown("🏆 Contributor Level: **Bronze**")
                st.markdown("💎 Point Accruals: **125 pts**")
                st.markdown("<hr style='border:0; border-top:1px solid var(--border-color); margin: 8px 0;'>", unsafe_allow_html=True)
                
                # Navigate suggestions message
                st.markdown("*Use the sidebar links to modify Settings or view leaderboard badges.*")

