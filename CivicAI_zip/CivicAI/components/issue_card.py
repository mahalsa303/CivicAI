"""
Issue Card and Dialog Component for CivicAI.

Renders modern civic issue report cards and handles the detailed deep-dive 
interactive modal popups (using st.dialog) containing timelines, AI justifications,
and voting options.
"""

import streamlit as st
from typing import Any, Dict
from services.firebase_service import vote_issue


@st.dialog("📋 Issue Deep-Dive Details", width="large")
def render_issue_dialog(issue: Dict[str, Any]):
    """
    Renders the details modal for a single issue.
    """
    category = issue.get("category", "Civic Issue")
    status = issue.get("status", "Open")
    severity = issue.get("severity", "Low")
    reporter = issue.get("reporter", "Anonymous")
    
    st.write(f"### {category} Details")
    
    # 1. Timeline Indicator
    st.markdown("#### ⏱ Processing Timeline")
    status_steps = ["Open", "Verified", "In Progress", "Resolved"]
    
    # Simple CSS timeline row
    step_cols = st.columns(4)
    current_status_idx = 0
    if status.lower() == "verified":
        current_status_idx = 1
    elif status.lower() == "in progress":
        current_status_idx = 2
    elif status.lower() in ("resolved", "rejected"):
        current_status_idx = 3

    for idx, step in enumerate(status_steps):
        with step_cols[idx]:
            if idx <= current_status_idx:
                badge_style = "background-color: var(--primary-color); color: white; border: 1px solid var(--primary-light);"
                step_prefix = "🟢"
            else:
                badge_style = "background-color: var(--border-color); color: var(--text-muted); border: 1px solid var(--border-color);"
                step_prefix = "⚪"
                
            st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 8px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    {badge_style}
                ">
                    {step_prefix} {step}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 🚨 AI Analysis & Parameters")
        st.write(f"🎯 **AI Confidence Score:** {issue.get('confidence_score', 92)}%")
        st.write(f"📊 **Priority Score:** {issue.get('priority_score', 55)} / 100")
        st.write(f"🏢 **Responsible Department:** {issue.get('department', 'Unassigned')}")
        st.write(f"💰 **Estimated Resolution Cost:** {issue.get('estimated_resolution_cost', 'Unknown')}")
        st.write(f"⏱ **Est. Resolution Time:** {issue.get('resolution_time', 'Unknown')}")
        st.write(f"📝 **Suggested Action:** {issue.get('suggested_action', 'None')}")
        
        st.markdown("---")
        st.markdown("#### 👤 Reporter Metadata")
        st.write(f"👤 **Filed By:** {reporter}")
        st.write(f"📍 **Coordinates:** {issue.get('latitude', 16.435)}, {issue.get('longitude', 81.521)}")
        st.write(f"📅 **Submitted At:** {issue.get('created_at', 'Recently')}")

    with col_right:
        # Explain AI Decision block (Explainable AI)
        st.markdown("#### 🧠 Explain AI Decision")
        cat_expl = issue.get("category_explanation", f"AI matched keyword patterns in description to classify this as {category}.")
        dep_expl = issue.get("department_explanation", f"Routed to {issue.get('department')} because the issue falls under their operational jurisdiction.")
        pri_expl = issue.get("priority_explanation", "Priority level assigned based on calculated public health, safety risks, and spatial coordinates proximity density.")
        
        st.info(f"**Category Routing:** {cat_expl}")
        st.warning(f"**Department Assignment:** {dep_expl}")
        st.success(f"**Priority Calculation:** {pri_expl}")

        st.markdown("---")
        st.markdown("#### 🤝 Community Verification")
        st.write(f"👍 **Upvotes (Verify):** {issue.get('upvotes', 0)} / 5 required to verify.")
        st.write(f"👎 **Downvotes (Incorrect):** {issue.get('downvotes', 0)}")


def render_issue_card_widget(issue: Dict[str, Any], key_suffix: str = ""):
    """
    Renders a single SaaS card for an issue in the reports list grid.
    """
    category = issue.get("category", "Civic Issue")
    status = issue.get("status", "Open")
    severity = issue.get("severity", "Low")
    reporter = issue.get("reporter", "Anonymous")
    upvotes = issue.get("upvotes", 0)
    priority = issue.get("priority_score", 50)
    
    # Dynamic badges based on severity
    sev_badge = f'<span class="badge-low">🟢 Low</span>'
    if str(severity).lower() == "high":
        sev_badge = f'<span class="badge-high">🔴 High</span>'
    elif str(severity).lower() == "medium":
        sev_badge = f'<span class="badge-medium">🟡 Medium</span>'

    # Status color
    status_color = "#3B82F6" if status.lower() == "open" else "#10B981" if status.lower() == "verified" else "#F59E0B" if status.lower() == "in progress" else "#64748B"

    # Card Render
    st.markdown(f"""
        <div class="saas-card" style="margin-bottom: 16px !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 11px; font-weight: bold; color: {status_color}; text-transform: uppercase; background-color: {status_color}1A; padding: 2px 6px; border-radius: 4px;">{status}</span>
                {sev_badge}
            </div>
            <h4 style="margin-top: 0; margin-bottom: 6px; color: var(--text-main); font-weight: bold; font-size: 16px;">{category}</h4>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px; line-height: 1.4; height: 36px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                {issue.get('impact', 'No impact description provided.')}
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-muted); margin-bottom: 12px;">
                <span>👤 {reporter}</span>
                <span>🔥 Priority: {priority}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-muted);">
                <span>👍 {upvotes} votes</span>
                <span>📅 {str(issue.get('created_at', 'Recently'))[:10]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_t1, col_v1 = st.columns(2)
    with col_t1:
        # Open detailed dialog popup modal
        if st.button("Track Issue 🔍", key=f"track_btn_{issue['doc_id']}_{key_suffix}", use_container_width=True):
            render_issue_dialog(issue)
            
    with col_v1:
        # Community verify quick voting
        if st.button("👍 Verify", key=f"vote_btn_{issue['doc_id']}_{key_suffix}", use_container_width=True):
            try:
                vote_issue(issue["doc_id"], "up")
                st.success("Upvoted!")
                st.rerun()
            except Exception as e:
                st.error(f"Error voting: {e}")


def render_recent_issues_dashboard(issues: list[Dict[str, Any]]):
    """
    Renders a unified SaaS card containing a list of recent issues with thumbnails.
    """
    st.markdown("""
        <div class="saas-card" style="margin-bottom: 20px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="margin: 0; font-weight: 700; font-family: 'Outfit', sans-serif;">Recent Issues</h4>
                <a href="/Report_Issue" target="_self" style="font-size: 12px; color: var(--primary-light); text-decoration: none; font-weight: 600;">View All</a>
            </div>
    """, unsafe_allow_html=True)
    
    if not issues:
        st.markdown("""
            <div style="text-align: center; padding: 30px;">
                <span style="font-size: 30px;">🎉</span>
                <p style="font-size: 13px; color: var(--text-muted); margin: 8px 0 0 0;">No active reports found.</p>
            </div>
            </div>
        """, unsafe_allow_html=True)
        return

    # Render up to 3 issues
    for idx, iss in enumerate(issues[:3]):
        category = iss.get("category", "Other")
        severity = iss.get("severity", "Low")
        status = iss.get("status", "Open")
        title = iss.get("official_complaint_summary", "Civic Issue Alert")
        if "OFFICIAL COMPLAINT:" in title:
            title = title.replace("OFFICIAL COMPLAINT:", "").strip()
            
        location = "Bhimavaram Main Road" if idx == 0 else "SITA Park Area" if idx == 1 else "Railway Station Road"
        reporter = iss.get("reporter", "Anonymous")
        votes = iss.get("upvotes", 0)
        priority = iss.get("priority_score", 50)
        time_text = "2h ago" if idx == 0 else "4h ago" if idx == 1 else "6h ago"
        
        # Colors mapping
        cat_color = "#6D28D9" # roads/purple
        if category.lower() in ("water supply", "water"):
            cat_color = "#3B82F6"
        elif category.lower() in ("street lighting", "electricity"):
            cat_color = "#F59E0B"
            
        sev_color = "#EF4444" if severity.lower() == "high" else "#F59E0B" if severity.lower() == "medium" else "#10B981"
        status_color = "#3B82F6" if status.lower() == "open" else "#10B981" if status.lower() == "verified" else "#F59E0B" if status.lower() == "in progress" else "#64748B"
        
        # Image URL mapping
        if "road" in category.lower() or "traffic" in category.lower() or idx == 0:
            img_url = "https://images.unsplash.com/photo-1515162305285-0293e4767cc2?w=80&h=80&fit=crop"
        elif "water" in category.lower() or idx == 1:
            img_url = "https://images.unsplash.com/photo-1584267326895-d88985f7190a?w=80&h=80&fit=crop"
        else:
            img_url = "https://images.unsplash.com/photo-1509024644558-2f56ce76c490?w=80&h=80&fit=crop"

        st.markdown(f"""
            <div style="display: flex; gap: 12px; align-items: center; padding: 12px 0; border-bottom: {'' if idx == 2 else '1px solid var(--border-color)'};">
                <img src="{img_url}" style="width: 44px; height: 44px; border-radius: 8px; object-fit: cover;" />
                <div style="flex-grow: 1; min-width: 0;">
                    <div style="font-size: 13.5px; font-weight: 700; color: var(--text-main); margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{title}</div>
                    <div style="display: flex; gap: 4px; margin-bottom: 4px; flex-wrap: wrap;">
                        <span style="font-size: 8px; font-weight: bold; color: white; background-color: {cat_color}; padding: 1px 4px; border-radius: 3px; text-transform: uppercase;">{category[:12]}</span>
                        <span style="font-size: 8px; font-weight: bold; color: white; background-color: {sev_color}; padding: 1px 4px; border-radius: 3px; text-transform: uppercase;">{severity}</span>
                        <span style="font-size: 8px; font-weight: bold; color: white; background-color: {status_color}; padding: 1px 4px; border-radius: 3px; text-transform: uppercase;">{status}</span>
                    </div>
                    <div style="font-size: 10.5px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">📍 {location} &bull; {time_text} by {reporter}</div>
                </div>
                <div style="text-align: center; padding: 0 8px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; align-items: center; min-width: 25px;">
                    <span style="font-size: 10px; color: var(--text-muted); line-height: 1; margin-bottom: -2px;">▲</span>
                    <span style="font-size: 11.5px; font-weight: 700; color: var(--text-main);">{votes}</span>
                </div>
                <div style="text-align: center; padding-left: 8px; min-width: 45px;">
                    <div style="font-size: 15px; font-weight: 800; color: var(--text-main); line-height: 1;">{priority}</div>
                    <div style="font-size: 8px; color: var(--text-muted); text-transform: uppercase; margin-top: 2px;">Priority</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)
