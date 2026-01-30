from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_emergency
from authority_engine import resolve_authority
from notify import send_notification

app = FastAPI()

class Emergency(BaseModel):
    message: str
    location: str

@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    ai_result = analyze_emergency(data.message)

    # Example parsed output (you parse JSON from AI in real system)
    category = "DISASTER"
    priority = "CRITICAL"

    authority = resolve_authority(category)

    notification = send_notification(authority, data.message, data.location, priority)

    return {
        "ai_analysis": ai_result,
        "authority": authority,
        "notification": notification,
        "status": "DISPATCHED"
    }
