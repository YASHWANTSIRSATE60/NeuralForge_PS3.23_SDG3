from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_engine import analyze_emergency   # AI logic file

app = FastAPI(title="NeuralForge PS3.23 Backend")

# -----------------------
# CORS (Frontend Access)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow GitHub Pages / any frontend
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
        "service": "NeuralForge PS3.23 AI Emergency System",
        "status": "running",
        "health": "/healthz",
        "api": "/api/emergency"
    }

# -----------------------
# Main API
# -----------------------
@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    """
    Flow:
    Frontend → Backend → AI → Classification → Response
    """

    # AI analysis
    ai_result = analyze_emergency(data.message)

    # Example ai_result expected format:
    # {
    #   "category": "DISASTER",
    #   "severity": "HIGH",
    #   "priority": "CRITICAL",
    #   "risk": "HIGH",
    #   "required_help": "Rescue + Medical"
    # }

    # Authority mapping
    authority_map = {
        "MEDICAL": {"name": "Health Services", "team": "Ambulance Unit"},
        "FIRE": {"name": "Fire Department", "team": "Fire Response Unit"},
        "CRIME": {"name": "Police Department", "team": "Police Unit"},
        "DISASTER": {"name": "Disaster Response Force", "team": "NDRF/SDRF Team"},
        "INFRASTRUCTURE": {"name": "Municipal Corporation", "team": "Municipal Emergency Team"},
        "WOMEN_SAFETY": {"name": "Women Safety Cell", "team": "Women Protection Unit"},
        "CHILD_SAFETY": {"name": "Child Protection Services", "team": "Child Rescue Unit"},
        "ACCIDENT": {"name": "Rescue Services", "team": "Rescue + Ambulance"},
        "GENERAL": {"name": "Local Control Room", "team": "General Response Team"}
    }

    category = ai_result.get("category", "GENERAL")
    authority = authority_map.get(category, authority_map["GENERAL"])

    return {
        "ai_analysis": ai_result,
        "authority": authority,
        "location": data.location,
        "status": "DISPATCHED"
    }
