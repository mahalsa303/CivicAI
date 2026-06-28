"""
Notification Service for CivicAI.

Manages mock and database-triggered alerts and notification recommendations.
"""

from typing import List, Dict, Any
import datetime


def get_notifications() -> List[Dict[str, Any]]:
    """
    Returns a list of recent system notifications and recommendations.
    """
    return [
        {
            "id": 1,
            "title": "Road Repair Scheduled",
            "message": "Public Works scheduled repair work for potholes near SVEC Main gate.",
            "timestamp": "2 hours ago",
            "type": "info"
        },
        {
            "id": 2,
            "title": "Issue Verified",
            "message": "Water leakage report in Hostel Road reached 5 verifications.",
            "timestamp": "4 hours ago",
            "type": "success"
        },
        {
            "id": 3,
            "title": "Water Department Update",
            "message": "Pipeline inspection completed near Block A. Status updated to resolved.",
            "timestamp": "1 day ago",
            "type": "info"
        },
        {
            "id": 4,
            "title": "Complaint Closed",
            "message": "Garbage dump report near Park entrance resolved by sanitation department.",
            "timestamp": "2 days ago",
            "type": "success"
        }
    ]
