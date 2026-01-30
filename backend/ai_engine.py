import os
import json
import google.generativeai as genai

# Load API key from Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def analyze_emergency(message: str):
    prompt = f"""
You are an AI emergency triage system.

Analyze the emergency and return STRICT JSON only in this format:

{{
  "category": "MEDICAL | FIRE | DISASTER | CRIME | RESCUE | ACCIDENT | INFRASTRUCTURE | GENERAL",
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "priority": "LOW | MEDIUM | HIGH | CRITICAL",
  "risk": "LOW | MEDIUM | HIGH",
  "required_help": "text description"
}}

Emergency message:
\"\"\"{message}\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean markdown if Gemini adds ```json
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        # Validation fallback
        return {
            "category": data.get("category", "GENERAL"),
            "severity": data.get("severity", "LOW"),
            "priority": data.get("priority", "LOW"),
            "risk": data.get("risk", "LOW"),
            "required_help": data.get("required_help", "General assistance")
        }

    except Exception as e:
        # Safe fallback (never crash system)
        return {
            "category": "GENERAL",
            "severity": "LOW",
            "priority": "LOW",
            "risk": "LOW",
            "required_help": "Manual review required"
        }
