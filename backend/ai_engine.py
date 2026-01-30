import os
import google.generativeai as genai
import json

# Load API key from Render Environment Variables
GEMINI_API_KEY = os.getenv("AIzaSyC2duxKFeQ9STHv83NbPbU4HElPGybHsH0")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def analyze_emergency(message: str):
    prompt = f"""
You are an AI emergency classification system.

Analyze the emergency message and return ONLY JSON in this format:

{{
  "category": "DISASTER | MEDICAL | FIRE | CRIME | ACCIDENT | FLOOD | EARTHQUAKE | INFRASTRUCTURE | OTHER",
  "severity": "LOW | MEDIUM | HIGH | EXTREME",
  "priority": "LOW | MEDIUM | HIGH | CRITICAL",
  "confidence": 0.0-1.0
}}

Rules:
- No explanation
- No text
- No markdown
- Only valid JSON

Emergency message:
\"\"\"{message}\"\"\"
"""

    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        data = json.loads(text)
        return data
    except Exception as e:
        # fallback safety
        return {
            "category": "OTHER",
            "severity": "LOW",
            "priority": "LOW",
            "confidence": 0.1
        }
