"""
Local JSON File Storage Helper for CivicAI.

Provides basic file-based backup / read and write operations for issues.
"""

import json
import logging
import os
from typing import Any, Dict, List

# Configure logger
logger = logging.getLogger("storage")

FILE_PATH = "data/issues.json"


def load_issues() -> List[Dict[str, Any]]:
    """
    Loads all saved issues from the local JSON storage file.
    """
    if not os.path.exists(FILE_PATH):
        logger.info("Local storage file %s does not exist yet. Returning empty list.", FILE_PATH)
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                logger.warning("Local storage content is not a list. Resetting to empty list.")
                return []
            return data
    except (json.JSONDecodeError, IOError) as e:
        logger.error("Error reading issues from local file %s: %s", FILE_PATH, e)
        return []


def save_issue(issue: Dict[str, Any]) -> None:
    """
    Appends a new issue dictionary to the local JSON storage file.
    """
    try:
        parent_dir = os.path.dirname(FILE_PATH)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        issues = load_issues()
        issues.append(issue)

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(issues, f, indent=4)
        logger.info("Successfully appended issue to local storage: %s", FILE_PATH)
    except IOError as e:
        logger.error("Error saving issue to local file %s: %s", FILE_PATH, e)
