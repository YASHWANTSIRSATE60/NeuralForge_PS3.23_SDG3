from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import os

# Internal engines
from ai_engine import analyze_emergency
from routing_engine import route_emergency
from team_engine import assign_team
from notify import send_notification   # if not created yet, we will add next

app = FastAPI(title="NeuralForge PS3.23 - AI Emergency Backend")

# -----------------------------
# Models
# -----------------------------

class Emergency(BaseModel):
    message: str
    location: str


class AIResult(BaseModel):
    category: str
    severity: str
    priority: str
    confidence: float


# -----------------------------
# Health Check (REQUIRED FOR RENDER)
# -----------------------------

@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "neuralforge-backend"}


# -----------------------------
# Core API
# -----------------------------

@app.post("/api/emergency")
def handle_emergency(data: Emergency):
    """
    Full AI Emergency Pipeline:
    User Message
        ↓
    AI Classification
        ↓
    Category + Severity + Priority
        ↓
    Authority Routing
        ↓
    Team Assignment
        ↓
    Notification Dispatch
        ↓
    Structured Response
    """

    # 1️⃣ AI ANALYSIS
    ai_result: Dict = analyze_emergency(data.message)

    """
    Expected ai_result format:
    {
        "category": "DISASTER",
        "severity": "HIGH",
        "priority": "CRITICAL",
        "confidence": 0.92
    }
    """

    category = ai_result.get("category", "UNKNOWN")
    severity = ai_result.get("severity", "LOW")
    priority = ai_result.get("priority", "LOW")
    confidence = ai_result.get("confidence", 0.0)

    # 2️⃣ ROUTING
    authority = route_emergency(category)

    # 3️⃣ TEAM ASSIGNMENT
    team = assign_team(category, severity)

    # 4️⃣ NOTIFICATION
    notification_status = send_notification(
        authority=authority,
        team=team,
        message=data.message,
        location=data.location,
        priority=priority
    )

    # 5️⃣ RESPONSE
    return {
        "status": "DISPATCHED",
        "ai_analysis": {
            "category": category,
            "severity": severity,
            "priority": priority,
            "confidence": confidence
        },
        "routing": {
            "authority": authority,
            "team": team
        },
        "notification": notification_status
    }


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():
    return {
        "service": "NeuralForge PS3.23 AI Emergency System",
        "status": "running",
        "docs": "/docs",
        "health": "/healthz"
    }
