from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import google.generativeai as genai
from datetime import datetime

# Initialize FastAPI
app = FastAPI(title="AI Emergency Response System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for incidents
incidents_db = []
next_id = 1

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Pydantic models
class EmergencyRequest(BaseModel):
    message: str
    location: str

class EmergencyAnalysis(BaseModel):
    category: str
    priority: str
    severity: str
    risk: str
    required_help: str
    authority: str

class Incident(EmergencyAnalysis):
    id: int
    message: str
    location: str
    assigned_team: str
    status: str = "pending"
    timestamp: str

# Helper function to safely parse AI response
def parse_ai_response(response_text: str) -> Optional[EmergencyAnalysis]:
    """Parse AI response and return structured analysis"""
    try:
        # Clean response - remove markdown code blocks
        cleaned = response_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1]
        if "```" in cleaned:
            cleaned = cleaned.split("```")[0]
        
        # Parse JSON
        data = json.loads(cleaned)
        
        # Validate required fields
        required_fields = ["category", "priority", "severity", "risk", "required_help", "authority"]
        for field in required_fields:
            if field not in data:
                return None
        
        return EmergencyAnalysis(**data)
    except:
        return None

# Helper function to get AI analysis
def get_ai_analysis(message: str, location: str) -> EmergencyAnalysis:
    """Use Gemini AI to analyze emergency"""
    prompt = f"""
    Analyze this emergency report and return ONLY valid JSON without any markdown, explanations, or additional text.
    
    Emergency Message: {message}
    Location: {location}
    
    Return JSON with these exact fields:
    - "category": one of ["medical", "fire", "disaster", "crime", "rescue", "accident"]
    - "priority": one of ["low", "medium", "high", "critical"]
    - "severity": one of ["low", "medium", "high", "critical"]
    - "risk": one of ["low", "medium", "high", "critical"]
    - "required_help": string describing required assistance
    - "authority": one of ["police", "ambulance", "fire_brigade", "disaster_response", "rescue_team"]
    
    Example response:
    {{
        "category": "medical",
        "priority": "high",
        "severity": "high",
        "risk": "medium",
        "required_help": "Emergency medical assistance required for heart attack patient",
        "authority": "ambulance"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        analysis = parse_ai_response(response.text)
        
        if analysis:
            return analysis
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
    
    # Fallback analysis based on keywords
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["fire", "burning", "smoke"]):
        return EmergencyAnalysis(
            category="fire",
            priority="high",
            severity="high",
            risk="high",
            required_help="Fire containment and rescue",
            authority="fire_brigade"
        )
    elif any(word in message_lower for word in ["heart", "medical", "injured", "bleeding", "accident"]):
        return EmergencyAnalysis(
            category="medical",
            priority="high",
            severity="high",
            risk="medium",
            required_help="Emergency medical assistance",
            authority="ambulance"
        )
    elif any(word in message_lower for word in ["crime", "robbery", "attack", "violent"]):
        return EmergencyAnalysis(
            category="crime",
            priority="high",
            severity="high",
            risk="high",
            required_help="Law enforcement intervention",
            authority="police"
        )
    else:
        return EmergencyAnalysis(
            category="rescue",
            priority="medium",
            severity="medium",
            risk="medium",
            required_help="General emergency assistance",
            authority="rescue_team"
        )

# Helper function to assign team based on authority
def assign_team(authority: str, location: str) -> str:
    """Assign appropriate response team"""
    teams = {
        "police": ["SWAT Team Alpha", "Patrol Unit Bravo", "Rapid Response Charlie"],
        "ambulance": ["Medic Team Red", "Emergency Medical Gold", "Critical Care Unit"],
        "fire_brigade": ["Fire Engine 101", "Rescue Squad 202", "Hazmat Unit 303"],
        "disaster_response": ["Disaster Team A", "Crisis Response B", "Emergency Unit C"],
        "rescue_team": ["Rescue Team One", "Search & Rescue Two", "Emergency Response Three"]
    }
    
    import hashlib
    # Deterministic team assignment based on location
    hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
    team_list = teams.get(authority, ["Emergency Response Unit"])
    team_index = hash_val % len(team_list)
    
    return team_list[team_index]

# API Endpoints
@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/api/emergency", response_model=Incident)
async def report_emergency(request: EmergencyRequest):
    """Report a new emergency"""
    global next_id
    
    # Get AI analysis
    analysis = get_ai_analysis(request.message, request.location)
    
    # Assign team
    assigned_team = assign_team(analysis.authority, request.location)
    
    # Create incident
    incident = Incident(
        id=next_id,
        message=request.message,
        location=request.location,
        assigned_team=assigned_team,
        timestamp=datetime.now().isoformat(),
        **analysis.dict()
    )
    
    # Store in memory
    incidents_db.append(incident)
    next_id += 1
    
    return incident

@app.get("/api/incidents", response_model=List[Incident])
async def get_incidents():
    """Get all incidents"""
    return incidents_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
