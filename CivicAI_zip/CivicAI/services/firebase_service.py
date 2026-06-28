"""
Firebase Database Service for CivicAI.

Handles connection to Firebase Firestore to read, write, update issues,
and manage contributor points and leaderboards. Supports toggleable local Demo Mode.
"""

import datetime
import logging
import os
import streamlit as st
from typing import Any, Dict, List
import firebase_admin
from firebase_admin import credentials, firestore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("firebase_service")

KEY_PATH = "firebase-key.json"
VERIFICATION_THRESHOLD = 5

if not os.path.exists(KEY_PATH):
    raise FileNotFoundError(
        f"{KEY_PATH} not found.\n"
        "Download your Firebase credentials:\n"
        "1. Go to Firebase Console\n"
        "2. Project Settings > Service Accounts\n"
        "3. Generate New Private Key\n"
        "4. Save as 'firebase-key.json' in the CivicAI folder"
    )

try:
    cred = credentials.Certificate(KEY_PATH)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    logger.error("Failed to initialize Firebase app: %s", e)
    raise RuntimeError("Firebase initialization failed. Verify your credentials.") from e


def calculate_verification_score(upvotes: int, downvotes: int) -> int:
    return upvotes - downvotes


def adjust_user_points(username: str, points_delta: int, stat_to_increment: str = None) -> None:
    if not username or username.strip().lower() == "anonymous":
        return

    name_clean = username.strip()
    try:
        user_ref = db.collection("users").document(name_clean)
        user_doc = user_ref.get()

        if user_doc.exists:
            data = user_doc.to_dict() or {}
            current_points = int(data.get("points", 0))
            new_points = max(0, current_points + points_delta)
            updates = {"points": new_points}

            if stat_to_increment:
                updates[stat_to_increment] = int(data.get(stat_to_increment, 0)) + 1

            user_ref.update(updates)
            logger.info("Updated user %s points by %d. New total: %d", name_clean, points_delta, new_points)
        else:
            initial_points = max(0, points_delta)
            user_data = {
                "name": name_clean,
                "points": initial_points,
                "verified_reports": 1 if stat_to_increment == "verified_reports" else 0,
                "resolved_reports": 1 if stat_to_increment == "resolved_reports" else 0,
                "bad_reports": 1 if stat_to_increment == "bad_reports" else 0,
            }
            user_ref.set(user_data)
            logger.info("Created new contributor profile for %s with initial points %d", name_clean, initial_points)
    except Exception as e:
        logger.error("Error adjusting points for user %s: %s", name_clean, e)


def save_issue(issue: Dict[str, Any]) -> str:
    try:
        issue_data = issue.copy()
        issue_data.setdefault("status", "Open")
        issue_data.setdefault("upvotes", 0)
        issue_data.setdefault("downvotes", 0)
        issue_data.setdefault("verification_score", 0)
        issue_data.setdefault("latitude", 16.435)
        issue_data.setdefault("longitude", 81.521)
        issue_data.setdefault("reporter", "Anonymous")
        issue_data.setdefault("created_at", datetime.datetime.now().isoformat())

        _, doc_ref = db.collection("issues").add(issue_data)
        logger.info("Successfully saved issue to Firestore with ID: %s", doc_ref.id)

        adjust_user_points(issue_data["reporter"], 5)

        return doc_ref.id
    except Exception as e:
        logger.error("Error writing issue to Firestore: %s", e)
        raise RuntimeError("Failed to save issue to Firestore.") from e


def _get_demo_issues() -> List[Dict[str, Any]]:
    """
    Generates 35 pre-seeded mock issues representing Bhimavaram, AP community data.
    """
    mock_reports = []
    categories_pool = [
        ("Road Damage", "Public Works", "Pothole on college main road.", "High", 85, "$200 - $400", "1-2 days"),
        ("Street Lighting", "Electricity", "Flickering street lamp near park.", "Medium", 60, "$50 - $100", "3-5 days"),
        ("Water Supply", "Water Supply", "Water main pipe burst on Hostel road.", "High", 90, "$500 - $1000", "1 day"),
        ("Sanitation", "Sanitation", "Accumulating garbage pile attracting rodents.", "High", 75, "$100 - $200", "2 days"),
        ("Traffic & Roads", "Public Works", "Damaged manhole cover in junction.", "High", 80, "$150 - $300", "1-2 days"),
        ("Environment", "Environment", "Uprooted tree blocking pedestrian pavement.", "Low", 40, "$80 - $150", "2-3 days"),
        ("Public Health", "Public Health", "Stagnant open sewage water drain leaking.", "High", 88, "$300 - $600", "2-3 days")
    ]
    
    statuses = ["Open", "Verified", "In Progress", "Resolved"]
    reporters = ["Ananya Sen", "Ravi Teja", "Sandeep K.", "Priyanka Roy", "Venkatesh P.", "Manoj Kumar"]

    # Bhimavaram SVEC Gate center coordinates
    base_lat = 16.435
    base_lon = 81.521

    for idx in range(35):
        # Determine parameters deterministically based on index
        cat_info = categories_pool[idx % len(categories_pool)]
        category, department, desc, severity, priority, cost, res_time = cat_info
        
        status = statuses[idx % len(statuses)]
        reporter = reporters[idx % len(reporters)]
        
        # Distribute coordinates slightly around center
        lat_offset = ((idx * 7) % 21 - 10) * 0.0007
        lon_offset = ((idx * 11) % 21 - 10) * 0.0007
        
        upvotes = (idx * 3) % 8
        # If upvotes >= 5, set status to Verified at least
        if upvotes >= 5 and status == "Open":
            status = "Verified"
            
        downvotes = (idx * 2) % 3
        
        # Distribute created dates over last 3 months
        months_ago = idx % 3
        created_date = datetime.datetime(2026, 6 - months_ago, (idx * 5 % 28) + 1, 10, 30)

        mock_reports.append({
            "doc_id": f"demo_doc_{idx}",
            "category": category,
            "severity": severity,
            "priority_score": priority,
            "department": department,
            "impact": f"A local {desc.lower()} affecting residents daily.",
            "suggested_action": f"Alert nearest municipal crew to resolve this {category.lower()} issue.",
            "resolution_time": res_time,
            "confidence_score": 90 + (idx % 10),
            "duplicate_probability": (idx * 4) % 30,
            "estimated_resolution_cost": cost,
            "official_complaint_summary": f"OFFICIAL COMPLAINT: {category} defect reported near Bhimavaram sector.",
            "category_explanation": "Categorised automatically based on semantic description match.",
            "department_explanation": f"Routed to {department} as they hold jurisdiction over {category.lower()}.",
            "priority_explanation": "Priority assigned based on risk factor and proximity coordinates.",
            "status": status,
            "upvotes": upvotes,
            "downvotes": downvotes,
            "verification_score": upvotes - downvotes,
            "latitude": base_lat + lat_offset,
            "longitude": base_lon + lon_offset,
            "reporter": reporter,
            "created_at": created_date.isoformat()
        })
        
    return mock_reports


def get_issues() -> List[Dict[str, Any]]:
    # Check if Demo Mode is toggled on in settings session state
    if st.session_state.get("demo_mode", False):
        logger.info("Serving 35 pre-seeded issues from Demo Mode memory feed.")
        return _get_demo_issues()

    try:
        docs = db.collection("issues").stream()
        issues = []
        for doc in docs:
            data = doc.to_dict()
            data["doc_id"] = doc.id
            issues.append(data)
        logger.info("Successfully fetched %d issues from Firestore", len(issues))
        return issues
    except Exception as e:
        logger.error("Error streaming issues from Firestore: %s", e)
        return []


def update_issue_status(doc_id: str, new_status: str) -> None:
    # Disable updates on demo records to keep sandbox state intact
    if doc_id.startswith("demo_doc_"):
        st.warning("Demo Mode: State modifications are simulated locally.")
        return

    try:
        doc_ref = db.collection("issues").document(doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            logger.warning("Document %s not found. Cannot update status.", doc_id)
            return

        data = doc.to_dict() or {}
        old_status = data.get("status", "Open")
        reporter = data.get("reporter", "Anonymous")

        if old_status != new_status:
            doc_ref.update({
                "status": new_status
            })
            logger.info("Updated issue %s status from '%s' to '%s'", doc_id, old_status, new_status)

            if new_status == "Verified" and old_status == "Open":
                adjust_user_points(reporter, 10, "verified_reports")
            elif new_status == "Resolved" and old_status != "Resolved":
                adjust_user_points(reporter, 20, "resolved_reports")
            elif new_status == "Rejected" and old_status != "Rejected":
                adjust_user_points(reporter, -10, "bad_reports")

    except Exception as e:
        logger.error("Error updating status for doc %s: %s", doc_id, e)
        raise RuntimeError(f"Failed to update status for issue {doc_id}.") from e


def vote_issue(doc_id: str, vote_type: str, threshold: int = VERIFICATION_THRESHOLD) -> None:
    if vote_type not in ("up", "down"):
        raise ValueError("vote_type must be either 'up' or 'down'")

    # Disable updates on demo records
    if doc_id.startswith("demo_doc_"):
        st.warning("Demo Mode: Votes are simulated locally.")
        return

    try:
        doc_ref = db.collection("issues").document(doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            logger.warning("Issue document %s does not exist", doc_id)
            return

        data = doc.to_dict() or {}
        upvotes = int(data.get("upvotes", 0))
        downvotes = int(data.get("downvotes", 0))
        reporter = data.get("reporter", "Anonymous")
        old_status = data.get("status", "Open")

        updates: Dict[str, Any] = {}
        if vote_type == "up":
            upvotes += 1
            updates["upvotes"] = upvotes
            if upvotes >= threshold and old_status.lower() == "open":
                updates["status"] = "Verified"
                logger.info("Issue %s automatically verified (upvotes reached %d)", doc_id, upvotes)
                adjust_user_points(reporter, 10, "verified_reports")
        elif vote_type == "down":
            downvotes += 1
            updates["downvotes"] = downvotes

        updates["verification_score"] = calculate_verification_score(upvotes, downvotes)
        doc_ref.update(updates)
        logger.info("Updated issue %s votes: up=%d, down=%d, score=%d", doc_id, upvotes, downvotes, updates["verification_score"])
    except Exception as e:
        logger.error("Error recording vote for doc %s: %s", doc_id, e)
        raise RuntimeError(f"Failed to register vote for issue {doc_id}.") from e


def get_leaderboard() -> List[Dict[str, Any]]:
    # Mock Leaderboard when Demo Mode is active
    if st.session_state.get("demo_mode", False):
        logger.info("Serving mock rankings from Demo Mode memory feed.")
        return [
            {"name": "Ananya Sen", "points": 125, "verified_reports": 8, "resolved_reports": 4, "bad_reports": 0},
            {"name": "Ravi Teja", "points": 95, "verified_reports": 5, "resolved_reports": 3, "bad_reports": 0},
            {"name": "Sandeep K.", "points": 65, "verified_reports": 4, "resolved_reports": 2, "bad_reports": 0},
            {"name": "Priyanka Roy", "points": 45, "verified_reports": 3, "resolved_reports": 1, "bad_reports": 0},
            {"name": "Venkatesh P.", "points": 30, "verified_reports": 2, "resolved_reports": 1, "bad_reports": 0},
            {"name": "Manoj Kumar", "points": 15, "verified_reports": 1, "resolved_reports": 0, "bad_reports": 0}
        ]

    try:
        docs = db.collection("users").order_by("points", direction=firestore.Query.DESCENDING).stream()
        users = []
        for doc in docs:
            users.append(doc.to_dict())
        logger.info("Successfully fetched %d users from Firestore", len(users))
        return users
    except Exception as e:
        logger.error("Error streaming users for leaderboard: %s", e)
        return []
