from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn
import logging
from ai_engine import analyze_emergency

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NeuralForge PS3.23")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class EmergencyRequest(BaseModel):
    message: str
    location: str

# Routes
@app.get("/healthz")
async def health_check():
    return {"status": "ok", "system": "NeuralForge PS3.23"}

@app.post("/api/emergency")
async def report_emergency(request: EmergencyRequest):
    logger.info(f"Received emergency: {request.message} at {request.location}")
    try:
        analysis = await analyze_emergency(request.message, request.location)
        return analysis
    except Exception as e:
        logger.error(f"Error processing emergency: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend
# Ensure frontend directory exists
if not os.path.exists("frontend"):
    os.makedirs("frontend", exist_ok=True)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
