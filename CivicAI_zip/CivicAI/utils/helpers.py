"""
Helper Utilities for CivicAI.

Provides general utility methods like distance calculations, validation checks,
and UI helper methods.
"""

import math
import logging

logger = logging.getLogger("helpers")


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the approximate distance in meters between two GPS coordinates
    using flat-earth projection.
    """
    try:
        lat_dist = (lat1 - lat2) * 111139.0
        avg_lat_rad = math.radians((lat1 + lat2) / 2.0)
        lon_dist = (lon1 - lon2) * 111139.0 * math.cos(avg_lat_rad)
        return math.sqrt(lat_dist**2 + lon_dist**2)
    except Exception as e:
        logger.error("Error calculating coordinate distance: %s", e)
        return 999999.0
