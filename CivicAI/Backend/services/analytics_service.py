"""
Analytics and Calculation Service for CivicAI.

Handles community health scores, issue filtering, dataframes aggregation
for Plotly, duplicate detection, and geospatial proximity matching.
"""

import datetime
from difflib import SequenceMatcher
import logging
import math
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from services import gemini_service as gemini

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("analytics_service")

# Configuration Constants
DUPLICATE_DIST_THRESHOLD_METERS = 100.0
DUPLICATE_DESC_SIMILARITY_THRESHOLD = 0.6
VERIFICATION_THRESHOLD = 5


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the approximate distance in meters between two GPS coordinates
    using a flat-earth projection.
    """
    lat_dist = (lat1 - lat2) * 111139.0
    avg_lat_rad = math.radians((lat1 + lat2) / 2.0)
    lon_dist = (lon1 - lon2) * 111139.0 * math.cos(avg_lat_rad)
    return math.sqrt(lat_dist**2 + lon_dist**2)


def find_duplicate_issue(
    new_issue: Dict[str, Any],
    existing_issues: List[Dict[str, Any]],
    dist_threshold: float = DUPLICATE_DIST_THRESHOLD_METERS,
    similarity_threshold: float = DUPLICATE_DESC_SIMILARITY_THRESHOLD
) -> Optional[Dict[str, Any]]:
    """
    Scans existing issues for potential duplicate reports.
    """
    new_lat = new_issue.get("latitude")
    new_lon = new_issue.get("longitude")
    new_cat = str(new_issue.get("category", "")).strip().lower()
    new_desc = str(new_issue.get("impact", "")).strip().lower()

    if new_lat is None or new_lon is None or not new_cat:
        return None

    for issue in existing_issues:
        est_lat = issue.get("latitude")
        est_lon = issue.get("longitude")
        est_cat = str(issue.get("category", "")).strip().lower()
        est_desc = str(issue.get("impact", "")).strip().lower()

        if est_lat is None or est_lon is None:
            continue

        if new_cat != est_cat:
            continue

        distance = calculate_distance(new_lat, new_lon, est_lat, est_lon)
        if distance > dist_threshold:
            continue

        ratio = SequenceMatcher(None, new_desc, est_desc).ratio()
        if ratio >= similarity_threshold:
            logger.info(
                "Duplicate detected! Match ID: %s. Distance: %.1fm. Similarity: %.2f",
                issue.get("doc_id"), distance, ratio
            )
            return issue

    return None


def calculate_community_health_score(issues: List[Dict[str, Any]]) -> Tuple[int, str]:
    """
    Calculates the Community Health Score dynamically.
    """
    active_high = 0
    active_medium = 0

    for issue in issues:
        status = str(issue.get("status", "")).lower()
        severity = str(issue.get("severity", "")).lower()
        
        if status not in ("resolved", "rejected"):
            if severity == "high":
                active_high += 1
            elif severity == "medium":
                active_medium += 1

    health_score = max(0, 100 - (active_high * 5 + active_medium * 2))
    
    if health_score >= 80:
        status_str = "🟢 Good"
    elif health_score >= 60:
        status_str = "🟠 Fair"
    else:
        status_str = "🔴 Poor"

    return health_score, status_str


def filter_issues(
    issues: List[Dict[str, Any]],
    status_filter: str,
    severity_filter: str,
    category_filter: str
) -> List[Dict[str, Any]]:
    """
    Applies filters to the list of issues for presentation.
    """
    filtered = []
    for issue in issues:
        if status_filter != "All" and issue.get("status", "") != status_filter:
            continue
        if severity_filter != "All" and issue.get("severity", "") != severity_filter:
            continue
        if category_filter != "All" and issue.get("category", "") != category_filter:
            continue
        filtered.append(issue)
    return filtered


def get_plotly_analytics_data(issues: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    """
    Processes Firestore issues to prepare pandas DataFrames for Plotly rendering.
    """
    data_cats = pd.DataFrame(columns=["Category", "Count"])
    data_sevs = pd.DataFrame(columns=["Severity", "Count"])
    data_deps = pd.DataFrame(columns=["Department", "Count"])
    data_status = pd.DataFrame(columns=["Status Type", "Count"])
    data_trend = pd.DataFrame(columns=["Month", "Count"])

    if not issues:
        return {
            "category": data_cats,
            "severity": data_sevs,
            "department": data_deps,
            "status": data_status,
            "trend": data_trend
        }

    df = pd.DataFrame(issues)

    if "category" in df.columns:
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        data_cats = cat_counts

    if "severity" in df.columns:
        sev_counts = df["severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        sev_counts["Severity"] = pd.Categorical(sev_counts["Severity"], categories=["High", "Medium", "Low"], ordered=True)
        data_sevs = sev_counts.sort_values("Severity")

    if "department" in df.columns:
        dep_counts = df["department"].value_counts().reset_index()
        dep_counts.columns = ["Department", "Count"]
        data_deps = dep_counts

    if "status" in df.columns:
        df["Status Type"] = df["status"].apply(
            lambda s: "Resolved" if str(s).lower() in ("resolved", "rejected") else "Open / Active"
        )
        status_counts = df["Status Type"].value_counts().reset_index()
        status_counts.columns = ["Status Type", "Count"]
        data_status = status_counts

    dates = []
    base_date = datetime.datetime(2026, 6, 25)
    for i, issue in enumerate(issues):
        created_at = issue.get("created_at")
        if created_at:
            try:
                date_parsed = datetime.datetime.fromisoformat(created_at)
                dates.append(date_parsed.strftime("%Y-%m"))
            except ValueError:
                months_ago = (i % 3)
                assigned_date = base_date - datetime.timedelta(days=months_ago * 30)
                dates.append(assigned_date.strftime("%Y-%m"))
        else:
            months_ago = (i % 3)
            assigned_date = base_date - datetime.timedelta(days=months_ago * 30)
            dates.append(assigned_date.strftime("%Y-%m"))

    trend_df = pd.DataFrame({"Month": dates})
    trend_counts = trend_df["Month"].value_counts().reset_index()
    trend_counts.columns = ["Month", "Count"]
    data_trend = trend_counts.sort_values("Month")

    return {
        "category": data_cats,
        "severity": data_sevs,
        "department": data_deps,
        "status": data_status,
        "trend": data_trend
    }


def generate_predictive_insights(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes community issues history to produce predictive insights.
    """
    insights = {
        "risk_score": 0,
        "active_issues_count": 0,
        "top_workload_department": "None",
        "recurring_issues": [],
        "hotspots": [],
        "weekly_new_issues": 0,
        "monthly_new_issues": 0,
        "ai_summary": "No data available."
    }

    if not issues:
        return insights

    df = pd.DataFrame(issues)

    df["status_lower"] = df["status"].astype(str).str.lower()
    df_active = df[~df["status_lower"].isin(["resolved", "rejected"])]
    insights["active_issues_count"] = len(df_active)

    active_high = sum(df_active["severity"].astype(str).str.lower() == "high")
    active_medium = sum(df_active["severity"].astype(str).str.lower() == "medium")
    active_low = sum(df_active["severity"].astype(str).str.lower() == "low")
    insights["risk_score"] = min(100, active_high * 10 + active_medium * 4 + active_low * 1)

    if len(df_active) > 0 and "department" in df_active.columns:
        top_dep = df_active["department"].value_counts().index[0]
        insights["top_workload_department"] = top_dep

    if "category" in df.columns:
        cat_counts = df["category"].value_counts()
        recurring = cat_counts[cat_counts > 1].index.tolist()
        insights["recurring_issues"] = recurring[:3]

    clusters = []
    issues_coords = []
    for issue in issues:
        lat = issue.get("latitude")
        lon = issue.get("longitude")
        if lat is not None and lon is not None:
            issues_coords.append((lat, lon))

    visited = [False] * len(issues_coords)
    for i, coord in enumerate(issues_coords):
        if visited[i]:
            continue
        cluster_members = [coord]
        visited[i] = True
        for j, other in enumerate(issues_coords):
            if not visited[j]:
                dist = calculate_distance(coord[0], coord[1], other[0], other[1])
                if dist <= 200.0:
                    cluster_members.append(other)
                    visited[j] = True
        
        if len(cluster_members) >= 2:
            avg_lat = sum(c[0] for c in cluster_members) / len(cluster_members)
            avg_lon = sum(c[1] for c in cluster_members) / len(cluster_members)
            clusters.append({
                "center": (round(avg_lat, 4), round(avg_lon, 4)),
                "count": len(cluster_members)
            })

    clusters = sorted(clusters, key=lambda x: x["count"], reverse=True)
    insights["hotspots"] = [f"Lat/Lon {c['center']} ({c['count']} issues)" for c in clusters[:3]]

    now = datetime.datetime.now()
    one_week_ago = now - datetime.timedelta(days=7)
    one_month_ago = now - datetime.timedelta(days=30)
    
    weekly_count = 0
    monthly_count = 0
    
    for issue in issues:
        created_at = issue.get("created_at")
        if created_at:
            try:
                date_parsed = datetime.datetime.fromisoformat(created_at)
                if date_parsed >= one_week_ago:
                    weekly_count += 1
                if date_parsed >= one_month_ago:
                    monthly_count += 1
            except ValueError:
                pass

    insights["weekly_new_issues"] = weekly_count
    insights["monthly_new_issues"] = monthly_count

    summary_data = {
        "risk_score": insights["risk_score"],
        "active_issues": insights["active_issues_count"],
        "top_workload_department": insights["top_workload_department"],
        "top_recurring_categories": insights["recurring_issues"],
        "hotspots_count": len(clusters),
        "new_issues_last_7_days": weekly_count
    }
    
    insights["ai_summary"] = gemini.generate_insights_summary(summary_data)

    return insights
