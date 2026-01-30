import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("AIzaSyC2duxKFeQ9STHv83NbPbU4HElPGybHsH0")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def analyze_emergency(message: str):
    prompt = f"""
You are an AI emergency triage system.

Analyze the message and return ONLY valid JSON:

Message: "{message}"

Format:
{{
  "category": "MEDICAL | FIRE | CRIME | DISASTER | INFRASTRUCTURE | WOMEN_SAFETY | CHILD_SAFETY | ACCIDENT | GENERAL",
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "priority": "LOW | MEDIUM | HIGH | CRITICAL",
  "risk": "LOW | MEDIUM | HIGH",
  "required_help": "text"
}}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    try:
        return eval(text)
    except:
        return {
            "category": "GENERAL",
            "severity": "LOW",
            "priority": "LOW",
            "risk": "LOW",
            "required_help": "General Assistance"
        }
