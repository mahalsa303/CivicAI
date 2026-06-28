"""
AI Command Center Component for CivicAI.

Renders the dynamic Gemini-powered community digest, outlining new report metrics,
priority issues, department responses, and recommended municipal actions.
"""

import streamlit as st
from typing import Any, Dict, List
from services.analytics_service import generate_predictive_insights


def render_ai_command_center(issues: List[Dict[str, Any]]):
    """
    Renders the AI Community Digest brief card.
    """
    if not issues:
        st.info("AI Command Center is initializing. Seed data or report issues to view insights.")
        return

    insights = generate_predictive_insights(issues)

    st.markdown(f"""
        <div class="saas-card" style="
            background: linear-gradient(135deg, #1E1B4B 0%, #1e1b4b99 100%) !important;
            border: 1px solid #4C1D95 !important;
            padding: 20px !important;
            height: 100%;
        ">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 20px;">🤖</span>
                <h4 style="margin: 0; color: white; font-weight: 800; font-family: 'Outfit', sans-serif;">AI Command Center <span style="font-size:9px; background: #6D28D9; padding: 2px 6px; border-radius: 9999px; margin-left: 5px; vertical-align: middle;">Beta</span></h4>
            </div>
            <h5 style="color: #A78BFA; font-weight: 700; margin-top: 0; margin-bottom: 8px; font-size:13.5px;">Today's AI Community Digest</h5>
            <div style="font-size: 12px; line-height: 1.5; color: #E9D5FF; margin-bottom: 0;">
                {insights.get('ai_summary', 'No summary generated yet.')}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_ai_smart_insights(issues: List[Dict[str, Any]]):
    """
    Renders the AI Predictive Insights details card.
    """
    if not issues:
        return

    insights = generate_predictive_insights(issues)

    st.markdown(f"""
        <div class="saas-card" style="
            background: linear-gradient(135deg, #311042 0%, #31104299 100%) !important;
            border: 1px solid #701A75 !important;
            padding: 20px !important;
            height: 100%;
        ">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 20px;">🔮</span>
                <h4 style="margin: 0; color: white; font-weight: 800; font-family: 'Outfit', sans-serif;">AI Smart Insights <span style="font-size:9px; background: #C084FC; color:#311042; padding: 2px 6px; border-radius: 9999px; margin-left: 5px; vertical-align: middle;">Beta</span></h4>
            </div>
            <h5 style="color: #F472B6; font-weight: 700; margin-top: 0; margin-bottom: 12px; font-size:13.5px;">Municipal Risk & Metrics</h5>
            <div style="display: grid; grid-template-columns: 1fr; gap: 8px; font-size: 11.5px; color: #F5D0FE;">
                <div>📦 <b>Active Backlog:</b> {insights.get('active_issues_count', 0)} reports</div>
                <div>🏢 <b>Top Workload:</b> {insights.get('top_workload_department', 'N/A')}</div>
                <div>🔥 <b>Community Risk:</b> {insights.get('risk_score', 0)} / 100</div>
                <div>📅 <b>Weekly Intake:</b> {insights.get('weekly_new_issues', 0)} new</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
