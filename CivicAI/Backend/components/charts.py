"""
Plotly Charts Component for CivicAI.

Renders high-quality responsive visualisations for category distribution,
severity distributions, department workloads, status ratios, and intake trends.
"""

import streamlit as st
import plotly.express as px
import pandas as pd


def update_plotly_layout(fig, title_text: str):
    """
    Applies custom theme variables to the Plotly figure layouts.
    Makes the figure backgrounds transparent and sets colors matching the theme.
    """
    dark_mode = st.session_state.get("dark_mode", False)
    text_color = "#F8FAFC" if dark_mode else "#0F172A"
    grid_color = "#334155" if dark_mode else "#E2E8F0"
    
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=15, color=text_color, family="Outfit, sans-serif")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color, family="Inter, sans-serif"),
        margin=dict(l=15, r=15, t=45, b=15),
        legend=dict(font=dict(color=text_color)),
        showlegend=True
    )
    
    # Update axes styling if they exist
    fig.update_xaxes(
        gridcolor=grid_color, 
        linecolor=grid_color, 
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color)
    )
    fig.update_yaxes(
        gridcolor=grid_color, 
        linecolor=grid_color, 
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color)
    )
    return fig


def render_category_distribution(df: pd.DataFrame):
    """
    Renders a Pie chart showing reports distribution by category.
    """
    if df.empty:
        st.info("No category data available to plot.")
        return
    fig = px.pie(
        df, 
        names="Category", 
        values="Count", 
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    update_plotly_layout(fig, "Reports by Category")
    st.plotly_chart(fig, use_container_width=True)


def render_severity_distribution(df: pd.DataFrame):
    """
    Renders a Bar chart showing counts by severity level.
    """
    if df.empty:
        st.info("No severity data available to plot.")
        return
    fig = px.bar(
        df,
        x="Severity",
        y="Count",
        color="Severity",
        color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
    )
    update_plotly_layout(fig, "Severity Breakdown")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_department_workload(df: pd.DataFrame):
    """
    Renders a Horizontal Bar chart showing issues per department.
    """
    if df.empty:
        st.info("No department workload data available to plot.")
        return
    fig = px.bar(
        df,
        x="Count",
        y="Department",
        orientation='h',
        color="Count",
        color_continuous_scale="Purples"
    )
    update_plotly_layout(fig, "Department Workload Distribution")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def render_status_proportion(df: pd.DataFrame):
    """
    Renders a Donut chart showing open vs resolved ratios.
    """
    if df.empty:
        st.info("No status data available to plot.")
        return
    fig = px.pie(
        df,
        names="Status Type",
        values="Count",
        hole=0.4,
        color_discrete_sequence=["#3B82F6", "#10B981"]
    )
    update_plotly_layout(fig, "Open vs Resolved Ratios")
    st.plotly_chart(fig, use_container_width=True)


def render_monthly_trend(df: pd.DataFrame):
    """
    Renders a Line chart of issue intake trend over time.
    """
    if df.empty:
        st.info("No monthly trend data available to plot.")
        return
    fig = px.line(
        df,
        x="Month",
        y="Count",
        markers=True,
        line_shape="linear",
        color_discrete_sequence=["#8B5CF6"]
    )
    update_plotly_layout(fig, "Monthly Incident Intake")
    st.plotly_chart(fig, use_container_width=True)

