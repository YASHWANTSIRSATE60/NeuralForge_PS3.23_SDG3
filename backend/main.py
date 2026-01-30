from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_emergency
from authority_engine import resolve_authority
from notify import send_notification

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

    category = ai_result.get("category")
    priority = ai_result.get("priority")

    authority = resolve_authority(category)

    notification = send_notification(
        authority,
        data.message,
        data.location,
        priority
    )

    return {
        "ai_analysis": ai_result,
        "authority": authority,
        "notification": notification,
        "status": "DISPATCHED"
    }
