import google.generativeai as genai
import os
import json
import logging
from routing_engine import determine_routing

logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

async def analyze_emergency(message: str, location: str):
    if not api_key:
        raise ValueError("Server configuration error: GEMINI_API_KEY missing.")

    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        ACT AS AN EMERGENCY TRIAGE AI SYSTEM.
        Analyze the following emergency situation.
        
        SITUATION: "{message}"
        REPORTED LOCATION: "{location}"
        
        TASK:
        1. Auto-detect the language of the SITUATION.
        2. Categorize the emergency.
        3. Determine priority (Critical, High, Medium, Low).
        4. Rate severity 0-10.
        5. Assess immediate risks.
        6. Identify required resources.
        7. Route to appropriate authority: [police, ambulance, fire_brigade, disaster_response, rescue_team].
        8. Provide a confidence score (0.0 to 1.0).

        RETURN ONLY VALID JSON:
        {{
            "category": "string",
            "priority": "string",
            "severity": "string",
            "risk": "string",
            "required_help": "string",
            "authority": "string",
            "detected_language": "string",
            "confidence_score": number
        }}
        """
        
        response = model.generate_content(prompt)
        text_response = response.text
        
        # Clean response
        cleaned = text_response.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error(f"JSON Parse Error. Raw: {text_response}")
            # Fallback
            data = {
                "category": "Unknown",
                "priority": "High",
                "severity": "5",
                "risk": "Analysis failed, manual review needed",
                "required_help": "General Emergency Response",
                "authority": "police",
                "detected_language": "Unknown",
                "confidence_score": 0.5
            }

        # Apply routing
        data["routing_info"] = determine_routing(data.get("authority", "police"))
        return data

    except Exception as e:
        logger.error(f"AI Engine Error: {str(e)}")
        raise e
