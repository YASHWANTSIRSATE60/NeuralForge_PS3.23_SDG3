import os
import json
import re
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# Stable fast model (2025)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# -----------------------------
# AI ANALYSIS ENGINE
# -----------------------------
def analyze_emergency(message: str) -> dict:
    """
    Analyzes emergency text using Gemini AI.
    Always returns valid structured JSON.
    Never crashes the backend.
    """

    prompt = f"""
You are an AI emergency triage system for real-world emergency response.

Return ONLY valid JSON in this EXACT format:

{{
  "category": "medical/fire/disaster/crime/rescue/accident",
  "priority": "low/medium/high/critical",
  "severity": "low/medium/high/critical",
  "risk": "low/medium/high/critical",
  "required_help": "short clear action instruction",
  "authority": "police/ambulance/fire_brigade/disaster_response/rescue_team"
}}

Rules:
- JSON only
- No markdown
- No explanation
- No extra text
- No comments

Emergency message:
"{message}"
"""

    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError("Empty Gemini response")

        raw_text = response.text.strip()

        # Cleanup markdown if Gemini adds it
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError("JSON not found in Gemini output")

        ai_json = json.loads(match.group())

        # Validate required fields
        required_keys = [
            "category", "priority", "severity",
            "risk", "required_help", "authority"
        ]

        for key in required_keys:
            if key not in ai_json:
                raise ValueError(f"Missing key: {key}")

        return ai_json

    except Exception as e:
        print("❌ Gemini AI Engine Error:", str(e))

        # 🔥 FAIL-SAFE FALLBACK (system never crashes)
        return {
            "category": "emergency",
            "priority": "high",
            "severity": "high",
            "risk": "high",
            "required_help": "Immediate human operator intervention required",
            "authority": "manual_review"
        }
