"""python
import os
import google.generativeai as genai

# Read key from environment variable named GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # In dev you may want to log a warning and fall back to a simple rule-based stub to avoid runtime errors.
    # Avoid hardcoding API keys in source code.
    # For now we will use a lightweight fallback so the backend can run without the external API.
    GEMINI_API_KEY = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None  # fallback to internal logic

def analyze_emergency(message: str):
    if model:
        prompt = f'''
You are an AI emergency triage system.

Analyze the message and return ONLY valid JSON:

Message: "{message}"

Format:
{
  "category": "MEDICAL | FIRE | CRIME | DISASTER | INFRASTRUCTURE | WOMEN_SAFETY | CHILD_SAFETY | ACCIDENT | GENERAL",
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "priority": "LOW | MEDIUM | HIGH | CRITICAL",
  "risk": "LOW | MEDIUM | HIGH",
  "required_help": "text"
}
'''
        response = model.generate_content(prompt)
        text = response.text.strip()
        try:
            return eval(text)
        except Exception:
            pass

    # Fallback simple rule-based analyzer (safe default)
    msg = message.lower()
    if any(k in msg for k in ["heart", "bleed", "unconscious"]):
        category = "MEDICAL"
        severity = "CRITICAL"
        priority = "CRITICAL"
    elif any(k in msg for k in ["fire", "burn", "smoke"]):
        category = "FIRE"
        severity = "HIGH"
        priority = "HIGH"
    elif any(k in msg for k in ["robbery", "attack", "gun", "assault"]):
        category = "CRIME"
        severity = "HIGH"
        priority = "HIGH"
    elif any(k in msg for k in ["flood", "earthquake", "collapse"]):
        category = "DISASTER"
        severity = "CRITICAL"
        priority = "CRITICAL"
    else:
        category = "GENERAL"
        severity = "LOW"
        priority = "LOW"

    return {
        "category": category,
        "severity": severity,
        "priority": priority,
        "risk": "HIGH" if severity in ("CRITICAL", "HIGH") else "LOW",
        "required_help": "Dispatch appropriate emergency response"
    }
"""