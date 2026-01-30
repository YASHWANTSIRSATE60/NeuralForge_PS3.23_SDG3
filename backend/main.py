from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_engine import analyze_emergency

app = FastAPI(title="NeuralForge PS3.23 AI Emergency System")

# -----------------------
# CORS (Frontend Access)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # GitHub Pages / any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Models
# -----------------------
class Emergency(BaseModel):
    message: str
    location: str

# -----------------------
# Health Check
# -----------------------
@app.get("/healthz")
def health():
    return {"status": "ok", "service": "NeuralForge Backend"}

# -----------------------
# Root
# -----------------------
@app.get("/")
def root():
    return {
        "service": "NeuralForge PS3.23",
        "system": "AI Emergency Triage Platform",
        "api": "/api/emergency",
        "status": "running"
    }

# -----------------------
# Authority Mapping
# -----------------------
AUTHORITY_MAP = {
    "MEDICAL": {"name": "Health Services", "team": "Ambulance Unit"},
    "FIRE": {"name": "Fire Department", "team": "Fire Response Unit"},
    "CRIME": {"name": "Police Department", "team": "Police Unit"},
    "DISASTER": {"name": "Disaster Response Force", "team": "NDRF/SDRF Team"},
    "RESCUE": {"name": "Rescue Services", "team": "Search & Rescue Unit"},
    "ACCIDENT": {"name": "Emergency Response", "team": "Rescue + Ambulance"},
    "INFRASTRUCTURE": {"name": "Municipal Corporation", "team": "Municipal Emergency Team"},
    "GENERAL": {"name": "Local Control Room", "team": "General Response Team"}
}

# -----------------------
# Main API
# -----------------------
@app.post("/api/emergency")
def handle_emergency(data: Emergency):

    # AI Intelligence
    ai_result = analyze_emergency(data.message)

    category = ai_result.get("category", "GENERAL")

    # Authority Resolution
    authority = AUTHORITY_MAP.get(category, AUTHORITY_MAP["GENERAL"])

    # Dispatch Simulation
    dispatch_packet = {
        "ai_analysis": ai_result,
        "authority": authority,
        "location": data.location,
        "dispatch_status": "DISPATCHED",
        "system": "NeuralForge AI Core",
        "confidence": "AI-verified"
    }

    return dispatch_packet
