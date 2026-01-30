from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import re
import google.generativeai as genai
from typing import Dict

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# Stable fast model
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = FastAPI(title="NeuralForge PS3.23 Backend", version="2.0")

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
    return {"status": "ok", "service": "NeuralForge Backend", "ai": "Gemini Active"}

# -----------------------------
# UTILS
# -----------------------------
def extract_json(text: str) -> Dict:
    """
    Safely extract JSON from Gemini output
    """
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in AI response")

    return json.loads(match.group())

# -----------------------------
# AI ENGINE
# -----------------------------
def ai_analyze(message: str) -> Dict:
    prompt = f"""
You are an AI emergency triage system for real-world emergency response.

Analyze the message and return ONLY valid JSON in this EXACT format:

{{
  "category": "medical/fire/disaster/crime/rescue/accident",
  "priority": "low/medium/high/critical",
  "severity": "low/medium/high/critical",
  "risk": "low/medium/high/critical",
  "required_help": "short clear action instruction",
  "authority": "police/ambulance/fire_brigade/disaster_response/rescue_team"
}}

Rules:
- Do NOT add explanation
- Do NOT add markdown
- Do NOT add extra text
- Output JSON only

Emergency message:
"{message}"
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        ai_json = extract_json(raw_text)
        return ai_json

    except Exception as e:
        # Hard fallback (never crash system)
        return {
            "category": "unknown",
            "priority": "medium",
            "severity": "medium",
            "risk": "medium",
            "required_help": "Manual verification required",
            "authority": "manual_review"
        }

# -----------------------------
# ROUTE
# -----------------------------
@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    try:
        ai_result = ai_analyze(data.message)

        routing_map = {
            "police": "Police Control Room",
            "ambulance": "Emergency Medical Services",
            "fire_brigade": "Fire Department",
            "disaster_response": "Disaster Response Force",
            "rescue_team": "Rescue Operations Unit",
            "manual_review": "Human Operator Review"
        }

        assigned_team = routing_map.get(
            ai_result.get("authority", "manual_review"),
            "Human Operator Review"
        )

        return {
            "success": True,
            "ai_analysis": ai_result,
            "routing_decision": ai_result.get("authority"),
            "assigned_team": assigned_team,
            "location": data.location,
            "status": "DISPATCHED"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
