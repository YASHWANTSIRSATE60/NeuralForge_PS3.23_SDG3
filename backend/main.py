from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

# --------------------
# CONFIG
# --------------------
GEMINI_API_KEY = os.getenv("AIzaSyC2duxKFeQ9STHv83NbPbU4HElPGybHsH0")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

app = FastAPI()

# --------------------
# MODELS
# --------------------
class Emergency(BaseModel):
    message: str
    location: str

# --------------------
# HEALTH CHECK
# --------------------
@app.get("/healthz")
def health():
    return {"status": "ok"}

# --------------------
# AI ANALYSIS
# --------------------
def ai_analyze(message: str):
    prompt = f"""
    You are an emergency classification AI.

    Classify this emergency into:
    category: (medical, fire, disaster, crime, rescue, accident)
    priority: (low, medium, high, critical)
    authority: (police, ambulance, fire_brigade, disaster_response, rescue_team)

    Message: {message}

    Return JSON only.
    """

    response = model.generate_content(prompt)
    return response.text

# --------------------
# ROUTE
# --------------------
@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    ai_raw = ai_analyze(data.message)

    return {
        "ai_raw": ai_raw,
        "location": data.location,
        "status": "DISPATCHED"
    }
