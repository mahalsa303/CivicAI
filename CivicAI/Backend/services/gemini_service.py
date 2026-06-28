"""
Gemini AI Service Module for CivicAI.

Handles connection to the Gemini API, provides few-shot structured prompting
to analyze civic issues, and generates natural language narrative forecasts.
"""

import json
import logging
import os
from typing import Any, Dict, Tuple, Optional
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from utils.storage import save_issue

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini_service")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    logger.error("GEMINI_API_KEY environment variable is missing.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT_TEMPLATE = """
You are an expert civic issue detection and analysis AI.
Analyze the provided description and/or image of a community issue.
Classify the issue and return ONLY a valid, raw JSON object (without any markdown wrapping or additional text).

Your JSON output MUST follow this schema:
{{
    "category": "Category name",
    "severity": "High" | "Medium" | "Low",
    "priority_score": 0-100,
    "department": "Public Works" | "Sanitation" | "Water Supply" | "Electricity" | "Traffic & Roads" | "Public Health" | "Environment",
    "impact": "Detailed explanation of community impact",
    "suggested_action": "Recommended immediate action for civic authorities",
    "resolution_time": "Estimated resolution time (e.g., '2-4 days')",
    "confidence_score": 0-100,
    "duplicate_probability": 0-100,
    "estimated_resolution_cost": "Estimated cost range (e.g., '$200 - $500')",
    "official_complaint_summary": "A formal, professionally formatted official complaint summary describing the issue",
    "category_explanation": "Explain why this specific category was selected based on the keywords/description.",
    "department_explanation": "Explain why it was routed to this specific department.",
    "priority_explanation": "Explain why this priority score was assigned based on safety/health risks."
}}

Here are examples of expected outputs:

---
Example 1:
Input Issue: "Large open pothole in the middle of SVEC college main road causing traffic delays and two-wheelers to slip."
Output JSON:
{{
    "category": "Road Damage",
    "severity": "High",
    "priority_score": 85,
    "department": "Public Works",
    "impact": "High accident risk for motorists and significant traffic congestion on a major road.",
    "suggested_action": "Barricade the pothole immediately and fill it with asphalt repair mix within 24 hours.",
    "resolution_time": "1-2 days",
    "confidence_score": 95,
    "duplicate_probability": 10,
    "estimated_resolution_cost": "$200 - $400",
    "official_complaint_summary": "OFFICIAL COMPLAINT: Hazardous road defect. A large, uncovered pothole on SVEC college main road is posing immediate traffic safety hazards and causing vehicle accidents.",
    "category_explanation": "Categorised as Road Damage due to explicit mentions of a 'pothole' and 'road' defects.",
    "department_explanation": "Routed to Public Works as they are responsible for municipal road paving and repairs.",
    "priority_explanation": "High priority assigned because an open pothole in a main campus road is an active, immediate safety hazard for commuters."
}}

Example 2:
Input Issue: "Streetlight has been flickering and mostly off for the last 3 nights near the park entrance, making it very dark and unsafe at night."
Output JSON:
{{
    "category": "Street Lighting",
    "severity": "Medium",
    "priority_score": 60,
    "department": "Electricity",
    "impact": "Reduced visibility at night near park entrance, raising safety concerns for pedestrians and increasing minor crime risks.",
    "suggested_action": "Inspect the streetlight bulb and wiring assembly, replacing components as needed.",
    "resolution_time": "3-5 days",
    "confidence_score": 90,
    "duplicate_probability": 5,
    "estimated_resolution_cost": "$50 - $100",
    "official_complaint_summary": "OFFICIAL COMPLAINT: Inoperable public lighting. Flickering streetlight near the park entrance has created unsafe conditions for residents after dark.",
    "category_explanation": "Categorised as Street Lighting due to keywords 'streetlight' and 'dark at night'.",
    "department_explanation": "Routed to Electricity department to check light bulb and wiring hardware details.",
    "priority_explanation": "Medium priority assigned as it creates pedestrian safety issues but doesn't block traffic or cause immediate physical injury."
}}
---

Analyze this issue and return ONLY the JSON representation:
Issue:
{description}
"""


def _normalize_response(response_text: str) -> str:
    """
    Cleans raw response text from the Gemini model to extract a valid JSON substring.
    """
    if not response_text:
        return ""
    
    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]

    return text


def analyze_issue(description: str, image: Optional[Tuple[str, bytes]] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Calls the Gemini API to analyze a civic issue.
    """
    if not api_key:
        logger.error("Cannot analyze issue: Gemini API key is missing.")
        return "Gemini API key is not configured.", None

    if not description:
        description = "No text description provided. Please analyze the attached image."

    prompt = PROMPT_TEMPLATE.format(description=description)
    content = {"parts": []}

    if image is not None:
        mime_type, image_bytes = image
        content["parts"].append(
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_bytes,
                }
            }
        )

    content["parts"].append({"text": prompt})

    try:
        logger.info("Sending request to Gemini API (gemini-2.5-flash)...")
        response = model.generate_content(content)
        raw_text = response.text
        logger.info("Received response from Gemini API.")
    except Exception as e:
        logger.error("Gemini API generation failed: %s", e)
        return f"Gemini API request failed: {e}", None

    normalized_text = _normalize_response(raw_text)

    parsed = None
    try:
        parsed = json.loads(normalized_text)
    except json.JSONDecodeError as e:
        logger.warning("Failed to decode JSON from normalized response: %s", e)
        parsed = None

    if parsed:
        parsed["status"] = "Open"
        try:
            save_issue(parsed)
        except Exception as e:
            logger.error("Error writing backup to storage.py: %s", e)

    return raw_text, parsed


def generate_insights_summary(insights_data: Dict[str, Any]) -> str:
    """
    Calls the Gemini API to generate a natural language predictive summary.
    """
    if st.session_state.get("demo_mode", False):
        logger.info("Demo Mode: Serving pre-seeded predictive AI digest.")
        return (
            "CivicAI Analysis: Active backlog is centered around Public Works (Road Damage) and Water Supply. "
            "Recent reports indicate a cluster of infrastructure concerns near the SVEC hostel campus area. "
            "Recommend prioritizing immediate road barrier placements and sewer drainage inspections."
        )

    if not api_key:
        logger.error("Cannot generate insights: Gemini API key is missing.")
        return "Gemini API key is not configured. Predictive AI summary is unavailable."

    prompt = f"""
    You are a professional civic data scientist.
    Analyze the following aggregated local community metrics and provide a concise,
    professional 2-to-3 sentence predictive forecast and action plan for local authorities.

    Metrics:
    {json.dumps(insights_data, indent=2)}

    Format your response as a professional brief (maximum 100 words). Do not repeat the data rows directly; provide actionable forward-looking insights.
    """

    try:
        logger.info("Generating predictive insights narrative using Gemini...")
        response = model.generate_content(prompt)
        logger.info("Successfully generated insights narrative.")
        return response.text.strip()
    except Exception as e:
        logger.error("Failed to generate insights narrative from Gemini: %s", e)
        return "AI forecast is currently unavailable. Please verify connectivity or check system logs."


@st.cache_data(show_spinner=False)
def cached_analysis(description: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Caches Gemini issue analysis response for text-only descriptions.
    """
    return analyze_issue(description)
