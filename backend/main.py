from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_engine import analyze_emergency
from routing_engine import route_case

app = FastAPI()

# Allow all origins (demo purpose)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmergencyRequest(BaseModel):
    message: str
    location: str

@app.get("/")
def home():
    return {"status": "NeuralForge PS3.23 AI Emergency System Running"}

@app.post("/api/emergency")
def receive_emergency(data: EmergencyRequest):
    ai_result = analyze_emergency(data.message)
    case = route_case(ai_result, data.location)
    return case
