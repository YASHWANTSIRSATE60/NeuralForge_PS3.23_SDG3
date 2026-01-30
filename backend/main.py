from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Working Gemini model (2025)
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = FastAPI(title="NeuralForge PS3.23 Backend", version="1.0")

# -----------------------------
# MODELS
# -----------------------------
class Emergency(BaseModel):
    message: str
    location: str

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/healthz")
def health():
    return {"status": "ok"}

# -----------------------------
# AI ENGINE
# -----------------------------
def ai_analyze(message: str):
    prompt = f"""
You are an AI emergency triage system.

Analyze the emergency message and return ONLY valid JSON in this format:

{{
  "category": "medical/fire/disaster/crime/rescue/accident",
  "priority": "low/medium/high/critical",
  "severity": "low/medium/high/critical",
  "risk": "low/medium/high/critical",
  "required_help": "short clear instruction",
  "authority": "police/ambulance/fire_brigade/disaster_response/rescue_team"
}}

Emergency message:
"{message}"
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Safety cleanup
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {
            "category": "unknown",
            "priority": "unknown",
            "severity": "unknown",
            "risk": "unknown",
            "required_help": "AI parsing failed",
            "authority": "manual_review"
        }

# -----------------------------
# ROUTE
# -----------------------------
@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    ai_result = ai_analyze(data.message)

    routing_map = {
        "police": "Police Control Room",
        "ambulance": "Emergency Medical Services",
        "fire_brigade": "Fire Department",
        "disaster_response": "Disaster Response Force",
        "rescue_team": "Rescue Operations Unit",
        "manual_review": "Human Operator Review"
    }

    assigned_team = routing_map.get(ai_result.get("authority"), "Manual Review")

    return {
        "ai_analysis": ai_result,
        "routing_decision": ai_result.get("authority"),
        "assigned_team": assigned_team,
        "location": data.location,
        "status": "DISPATCHED"
    }
