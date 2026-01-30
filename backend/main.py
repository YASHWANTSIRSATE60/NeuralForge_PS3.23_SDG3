from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_engine import analyze_emergency
from routing_engine import route_case
from team_engine import assign_team

app = FastAPI()

# Add CORS middleware so browser JS (localhost or deployed frontend) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # add your frontend deploy URL(s) here, or use "*" for quick testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Emergency(BaseModel):
    message: str
    location: str

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    ai_result = analyze_emergency(data.message)

    category = ai_result.get("category", "GENERAL")
    priority = ai_result.get("priority", "LOW")

    route = route_case(category, priority)
    team = assign_team(category)

    return {
        "ai_analysis": ai_result,
        "routing_decision": route,
        "assigned_team": team,
        "location": data.location,
        "status": "DISPATCHED"
    }