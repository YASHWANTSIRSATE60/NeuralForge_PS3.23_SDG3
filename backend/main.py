from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_emergency
from routing_engine import route_case
from team_engine import assign_team

app = FastAPI()

class Emergency(BaseModel):
    message: str
    location: str

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    ai_result = analyze_emergency(data.message)

    category = ai_result["category"]
    priority = ai_result["priority"]

    route = route_case(category, priority)
    team = assign_team(category)

    return {
        "ai_analysis": ai_result,
        "routing_decision": route,
        "assigned_team": team,
        "location": data.location,
        "status": "DISPATCHED"
    }
